from collections import deque
import random
import math
import discord
from score import ScoreManager
from itembox import ItemBoxManager
from item_greenshell import ItemGreenShell
from item_redshell import ItemRedShell
from item_banana import ItemBanana


class MarioKartLogic:
	
	def __init__(self, client, cfg):
		self.client = client
		self.cfg = cfg
		
		# A dict of Channels -> Message log deques
		self.serverlog = dict()
		
		self.score_mngr = ScoreManager(cfg)
		self.itembox_mngr = ItemBoxManager(cfg)
		
		self.existing_items = list()
		self.held_items = dict()
		
		
	def get_channellog(self, channel):
		return self.serverlog.setdefault(channel, deque())
		
		
	def record_message(self, msg):
		# Add the message to the correct channel log.
		channellog = self.get_channellog(msg.channel)
		channellog.append(msg)
		
		# Cap max log length by removing the oldest messages.
		while len(channellog) > self.cfg.MAX_MESSAGELOG_LENGTH_PER_CHANNEL:
			channellog.popleft()
		
	
	def print_logs(self):
		for c in self.serverlog.values():
			for m in c:
				print("#" + m.channel.name + ": " + m.author.name + ": " + m.content)
				
		print("---")
		
		
	async def handle_message(self, msg):
		if msg.author == self.client.user:
			return
	
		self.record_message(msg)
		
		if not msg.content.startswith("="):
			await self.check_random_banana_hit(msg)
			return
			
		if msg.content.startswith("=bothold"):
			await self.client.delete_message(msg)
			item = ItemBanana(self, None, self.client.user, msg.channel)
			self.hold_item(self.client.user, item)
			return
			
		tokens = msg.content[1:].split()
		
		if len(tokens) < 1:
			return
		
		item = None
		
		commandfn = MarioKartLogic.commandtable.get(tokens[0])
		if commandfn == None:
			return
			
		if commandfn[0] == 1:
			if len(tokens) < 2:
				return
		
			itemfn = MarioKartLogic.itemtable.get(tokens[1])
			if itemfn == None:
				return
				
			item = itemfn(self, msg, msg.author, msg.channel)
			
		await self.client.delete_message(msg)
		await commandfn[1](self, msg, item)
		
		
	async def try_spend_itemboxes(self, msg, item):
		if not self.itembox_mngr.try_use(msg.author, item.cost()):
			reply = self.maketext_user(msg.author)
			reply += ": "
			reply += item.name() + item.emoji() + " "
			reply += "costs " + str(item.cost()) + self.cfg.EMOJI_ITEMBOX
			await self.client.send_message(msg.channel, reply)
			return False
			
		return True
		
		
	async def try_use_item(self, msg, item):
		if not self.can_hold_item(msg.author):
			reply = self.maketext_user(msg.author)
			reply += ": drop your held item first!"
			await self.client.send_message(msg.channel, reply)
			return False
			
		return True
		
		
	async def try_hold_item(self, msg, item):
		if not self.can_hold_item(msg.author):
			reply = self.maketext_user(msg.author)
			reply += ": you're already holding an item!"
			await self.client.send_message(msg.channel, reply)
			return False
			
		if not item.can_hold():
			reply = self.maketext_user(msg.author)
			reply += ": you can't hold a " + item.name() + " " + item.emoji() + "!"
			await self.client.send_message(msg.channel, reply)
			return False
			
		return True
			
		
	async def try_drop_item(self, msg):
		if self.can_hold_item(msg.author):
			reply = self.maketext_user(msg.author)
			reply += ": you're not holding an item!"
			await self.client.send_message(msg.channel, reply)
			return False
			
		return True
			
		
	async def command_use(self, msg, item):
		if not await self.try_use_item(msg, item):
			return
			
		if not await self.try_spend_itemboxes(msg, item):
			return
		
		await item.use()

		
	async def command_hold(self, msg, item):
		if not await self.try_hold_item(msg, item):
			return
		
		if not await self.try_spend_itemboxes(msg, item):
			return
		
		reply = item.text_user + " "
		reply += "held a " + item.name() + item.emoji() + "!"
		await self.client.send_message(item.channel, reply)
		await self.check_random_banana_hit(item.command)
		self.hold_item(item.author, item)

		
	async def command_drop(self, msg, _dummy):
		if not await self.try_drop_item(msg):
			return
			
		item = self.unhold_item(msg.author)
		await item.use()

		
	commandtable = {
		"use": [1, command_use],
		"hold": [1, command_hold],
		"drop": [0, command_drop]
	}

	
	itemtable = {
		"gs": ItemGreenShell,
		"rs": ItemRedShell,
		"b": ItemBanana
	}
	
		
	async def check_random_banana_hit(self, target):
		if target == None:
			return
			
		for item in self.existing_items:
			if isinstance(item, ItemBanana):
				if random.random() < self.cfg.BANANA_RANDOM_HIT_CHANCE:
					await item.hit_random(target)
					return
		
		
	def create_item(self, item):
		self.existing_items.append(item)
		
		
	def destroy_item(self, item):
		self.existing_items.remove(item)
		
		
	def is_holding_item(self, user):
		return self.held_items.get(user) != None
		
		
	def can_hold_item(self, user):
		return not self.is_holding_item(user)
		
		
	def hold_item(self, user, item):
		self.held_items[user] = item
		
		
	def unhold_item(self, user):
		return self.held_items.pop(user)
		
		
	def hit_user(self, text_before, item, target_msg, vr_penalty):
		if self.is_holding_item(target_msg.author):
			held_item = self.unhold_item(target_msg.author)
			
			reply = item.name() + " " + item.emoji() + " :boom: "
			reply += held_item.emoji()
			reply += text_before
			reply += "hit the item held by " + self.maketext_user(target_msg.author) + "! "
			return reply
		
		else:
			reply = item.name() + " " + item.emoji() + " :boom: "
			reply += text_before
			reply += "hit "
			
			if item.author == target_msg.author:
				reply += "**themselves**! "
			else:
				reply += self.maketext_user(target_msg.author) + "! "
			
			reply += "*(" + str(vr_penalty) + " VR)*"
			self.score_mngr.add(target_msg.author, vr_penalty)
			return reply
		
		
	def maketext_user(self, user):
		score = self.score_mngr.get(user)
		itemboxes = self.itembox_mngr.count(user)
		seconds_to_next = self.itembox_mngr.seconds_to_next(user)
	
		text = "**"
		text += self.cfg.EMOJI_YOSHI + " "
		text += user.mention
		
		text += " ("
		text += str(score) + " VR"
		text += ", "
		text += str(itemboxes) + self.cfg.EMOJI_ITEMBOX
		
		#if seconds_to_next != None:
		#	text += " -"
		#	text += str(math.floor(seconds_to_next / 60)) + ":"
		#	text += format(math.floor(seconds_to_next % 60), "02")
		
		text += ")**"
		return text