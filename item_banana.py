import random
import asyncio


class ItemBanana:
		
	def __init__(self, mk, command, author, channel):
		self.mk = mk
		self.command = command
		self.author = author
		self.channel = channel
		self.text_user = mk.maketext_user(author)
	
	
	def name(self):
		return "BANANA PEEL"

	
	def emoji(self):
		return self.mk.cfg.EMOJI_BANANA

	
	def cost(self):
		return self.mk.cfg.BANANA_COST
		
	
	def can_hold(self):
		return True
	
		
	async def use(self):
		reply = self.text_user + " "
		reply += "dropped a " + self.name() + self.emoji() + "!"
		await self.mk.client.send_message(self.channel, reply)
		await self.mk.check_random_banana_hit(self.command)
		self.mk.create_item(self)
		
	
	async def hit_random(self, target):
		self.mk.destroy_item(self)
		
		reply = self.mk.maketext_user(self.author) + "'s " + self.name() + " " + self.emoji() + " "
		reply += ":boom: was run over by "

		if self.author == target.author:
			reply += "**themselves**! "
		else:
			reply += self.mk.maketext_user(target.author) + "! "
		
		vr = self.mk.cfg.BANANA_HIT_VR
		reply += "*(" + str(vr) + " VR)*"
		self.mk.score_mngr.add(target.author, vr)
		await self.mk.client.send_message(self.channel, reply)