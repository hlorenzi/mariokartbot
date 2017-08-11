import random
from threading import RLock
from message_log import MessageLogManager
from score import ScoreManager
from itembox import ItemBoxManager
from item_greenshell import ItemGreenShell
from item_redshell import ItemRedShell
from item_banana import ItemBanana


class UserState:
	def __init__(self, user_id, vr, itemboxes):
		self.user_id = user_id
		self.vr = vr
		self.itemboxes = itemboxes


class SimulatedHit:
	HIT_NOTHING = 0
	HIT_USER = 1
	HIT_HELD_ITEM = 2
	
	def __init__(self, kind, held_item = None, user_id = None, vr_penalty = None):
		self.kind = kind
		self.held_item = held_item
		self.user_id = user_id
		self.vr_penalty = vr_penalty


class MarioKartManager:
	def __init__(self, replier, scheduler, cfg):
		self.replier = replier
		self.scheduler = scheduler
		self.cfg = cfg
		self.lock = RLock()
		self.msglog = MessageLogManager(cfg)
		self.score = ScoreManager(cfg)
		self.itemboxes = ItemBoxManager(cfg)
		
		self.held_items = dict()
		self.placed_down_items = list()
		
		
	# Receives a message in a thread-safe manner.
	def receive_msg(self, channel_id, user_id, msg_id, content):
		self.lock.acquire()
		
		if not self.decode_command(channel_id, user_id, msg_id, content):
			self.replier.reply_invalid_command(self.get_user_state(user_id), channel_id, msg_id, content)
			
		self.msglog.record_message(channel_id, user_id, msg_id)
		
		self.lock.release()
		
	
	# Decodes and executes a command from a message.
	# Returns whether the message is a valid command or is not a command at all.
	def decode_command(self, channel_id, user_id, msg_id, content):
		if not content.startswith("="):
			return True
			
		self.replier.delete_msg(channel_id, user_id, msg_id)
	
		tokens = content[1:].split()
		
		if len(tokens) < 1:
			return False
			
		possible_commands = {
			"use":  MarioKartManager.decode_command_use,
			"hold": MarioKartManager.decode_command_hold,
			"drop": MarioKartManager.decode_command_drop
		}
		
		decode_command_fn = possible_commands[tokens[0]]
		if decode_command_fn == None:
			return False
			
		return decode_command_fn(self, channel_id, user_id, msg_id, tokens)
		
		
	# Decodes and executes a "use" command.
	def decode_command_use(self, channel_id, user_id, msg_id, tokens):
		if len(tokens) != 2:
			return False
			
		item_fn = self.decode_item(tokens[1])
		if item_fn == None:
			return False
			
		already_held_item = self.held_items.get(user_id)
		if already_held_item != None:
			self.replier.reply_cant_use_holding_item(self.get_user_state(user_id), channel_id, already_held_item)
			return True
		
		item = item_fn(self.cfg, user_id)
		
		if not self.itemboxes.can_spend(user_id, item.cost()):
			self.replier.reply_insufficient_itemboxes(self.get_user_state(user_id), channel_id, item)
			return True
		
		item.use(self, channel_id, msg_id, False)
		return True
		
		
	# Decodes and executes a "hold" command.
	def decode_command_hold(self, channel_id, user_id, msg_id, tokens):
		if len(tokens) != 2:
			return False
			
		item_fn = self.decode_item(tokens[1])
		if item_fn == None:
			return False
			
		already_held_item = self.held_items.get(user_id)
		if already_held_item != None:
			self.replier.reply_already_holding_item(self.get_user_state(user_id), channel_id, already_held_item)
			return True
		
		item = item_fn(self.cfg, user_id)
		
		if not self.itemboxes.can_spend(user_id, item.cost()):
			self.replier.reply_insufficient_itemboxes(self.get_user_state(user_id), channel_id, item)
			return True
		
		self.held_items[user_id] = item
		self.replier.reply_hold_item(self.get_user_state(user_id), channel_id, item)
		return True
		
		
	# Decodes and executes a "drop" command.
	def decode_command_drop(self, channel_id, user_id, msg_id, tokens):
		if len(tokens) != 1:
			return False
			
		already_held_item = self.held_items.get(user_id)
		if already_held_item == None:
			self.replier.reply_no_held_item(self.get_user_state(user_id), channel_id)
			return True
			
		del self.held_items[user_id]
		already_held_item.use(self, channel_id, msg_id, True)
		return True
		
		
	# Decodes an item name and returns its constructor.
	def decode_item(self, token):
		possible_items = {
			"gs": ItemGreenShell,
			"rs": ItemRedShell,
			"b":  ItemBanana
		}
		
		return possible_items.get(token)
		
		
	# Returns an object holding the current state of a user.
	def get_user_state(self, user_id):
		if user_id == None:
			return UserState(None, None, None)
		else:
			return UserState(user_id, self.score.get(user_id), self.itemboxes.get(user_id))


	# Simulates an item hitting a user.
	def simulate_hit(self, target_user_id, vr_penalty, ignores_held_item):
		if target_user_id == None:
			return SimulatedHit(SimulatedHit.HIT_NOTHING)
	
		target_held_item = self.held_items.get(target_user_id)
		
		if not ignores_held_item and target_held_item != None:
			return SimulatedHit(SimulatedHit.HIT_HELD_ITEM, user_id = target_user_id, held_item = target_held_item)
			
		return SimulatedHit(SimulatedHit.HIT_USER, user_id = target_user_id, vr_penalty = vr_penalty)
		
	
	# Actually performs the effect of a previously simulated hit.
	def perform_hit(self, simulated_hit):
		if simulated_hit.kind == SimulatedHit.HIT_NOTHING:
			return
			
		if simulated_hit.kind == SimulatedHit.HIT_HELD_ITEM:
			del self.held_items[simulated_hit.user_id]
			return
			
		self.score.add(simulated_hit.user_id, simulated_hit.vr_penalty)
		
		
	def place_down_item(self, item):
		self.placed_down_items.append(item)
		
		
	def destroy_placed_down_item(self, item):
		self.placed_down_items.remove(item)
	
	
	def perform_random_banana_hit(self, channel_id, target_user_id):
		if target_user_id == None:
			return
			
		for item in self.placed_down_items:
			if isinstance(item, ItemBanana):
				if item.channel_id != channel_id:
					continue
				
				if random.random() < self.cfg["banana_random_hit_chance"]:
					item.slip(self, channel_id, target_user_id)
					return