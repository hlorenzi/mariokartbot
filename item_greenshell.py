import random


class ItemGreenShell:
		
	def __init__(self, mk, command, author, channel):
		self.mk = mk
		self.command = command
		self.author = author
		self.channel = channel
		self.text_user = mk.maketext_user(author)
	
	
	def name(self):
		return "GREEN SHELL"

	
	def emoji(self):
		return self.mk.cfg.EMOJI_GREENSHELL

	
	def cost(self):
		return self.mk.cfg.GREENSHELL_COST
		
	
	def can_hold(self):
		return True
	
	
	def choose_target(self):
		channellog = self.mk.get_channellog(self.channel)
		
		for i in range(len(channellog)):
			possible_target = channellog[-1 - i]
			
			if possible_target == self.command:
				continue
			
			if random.random() < self.mk.cfg.GREENSHELL_HIT_PLAYER_CHANCE:
				return possible_target
				
			if random.random() < self.mk.cfg.GREENSHELL_HIT_WALL_CHANCE:
				break
				
		return None
	
		
	async def use(self):
		target = self.choose_target()
		
		reply = self.text_user + " "
		reply += "threw a "
		
		if target == None:
			reply += self.name() + " " + self.emoji() + " "
			reply += "and it just crashed into a wall..."
			
		else:
			reply += self.mk.hit_user("and it ", self, target, self.mk.cfg.GREENSHELL_HIT_VR)
			
		await self.mk.client.send_message(self.channel, reply)
		await self.mk.check_random_banana_hit(self.command)