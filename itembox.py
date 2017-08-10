import time
import math


class LastUse:

	def __init__(self, itemboxes_at_this, time):
		self.itemboxes_at_this = itemboxes_at_this
		self.time = time


class ItemBoxManager:

	def __init__(self, cfg):
		self.cfg = cfg
		self.lastuse_per_user = dict()
		
		
	def count(self, user):
		lastuse = self.lastuse_per_user.get(user)
		
		if lastuse == None:
			return self.cfg.STARTING_ITEMBOXES
			
		time_since_lastuse = time.time() - lastuse.time
		
		itemboxes = math.floor(lastuse.itemboxes_at_this + time_since_lastuse / self.cfg.SECONDS_PER_ITEMBOX)
		itemboxes = max(0, itemboxes)
		itemboxes = min(self.cfg.MAX_ITEMBOXES, itemboxes)
		return itemboxes
		
	
	def seconds_to_next(self, user):
		lastuse = self.lastuse_per_user.get(user)
		
		if lastuse == None:
			return None
			
		time_since_lastuse = time.time() - lastuse.time
		return self.cfg.SECONDS_PER_ITEMBOX - (time_since_lastuse % self.cfg.SECONDS_PER_ITEMBOX)
		
		
	def try_use(self, user, amount):
		itemboxes = self.count(user)
		if itemboxes < amount:
			return False
			
		self.lastuse_per_user[user] = LastUse(itemboxes - amount, time.time())
		return True