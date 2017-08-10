import random
import asyncio


class ItemRedShell:
		
	def __init__(self, mk, command, author, channel):
		self.mk = mk
		self.command = command
		self.author = author
		self.channel = channel
		self.text_user = mk.maketext_user(author)
	
	
	def name(self):
		return "RED SHELL"

	
	def emoji(self):
		return self.mk.cfg.EMOJI_REDSHELL

	
	def cost(self):
		return self.mk.cfg.REDSHELL_COST
		
	
	def can_hold(self):
		return True
	
	
	def choose_target(self):
		channellog = self.mk.get_channellog(self.channel)
		
		for i in range(len(channellog)):
			possible_target = channellog[-1 - i]
			
			if possible_target == self.command:
				continue
				
			if possible_target.author == self.author:
				continue
			
			return possible_target
				
		return None
	
		
	async def use(self):
		target = self.choose_target()
		
		reply = self.text_user + " "
		reply += "threw a " + self.name() + " " + self.emoji() + " "
		
		if target == None:
			reply += "and it just kept going forever..."
			await self.mk.client.send_message(self.channel, reply)
			await self.mk.check_random_banana_hit(self, self.command)
			return
			
		else:
			seconds_to_hit = self.mk.cfg.REDSHELL_SECONDS_TO_HIT
			reply += "targeting " + self.mk.maketext_user(target.author) + " "
			reply += "in :clock3: " + str(seconds_to_hit) + "s..."
			await self.mk.client.send_message(self.channel, reply)
			await self.mk.check_random_banana_hit(self.command)
			
			await asyncio.sleep(seconds_to_hit)
			
			reply = self.mk.maketext_user(self.author) + "'s "
			reply += self.mk.hit_user("", self, target, self.mk.cfg.REDSHELL_HIT_VR)
			
			await self.mk.client.send_message(self.channel, reply)
			return