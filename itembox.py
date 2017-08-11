import time
import math


class Record:
	def __init__(self, amount, time):
		self.amount = amount
		self.time = time


class ItemBoxManager:
	def __init__(self, cfg):
		self.cfg = cfg
		self.latest_records = dict()
		
		
	# Computes the number of itemboxes a user currently has, taking the
	# last recorded amount and extrapolating by the time passed since.
	def get(self, user_id):
		latest_record = self.latest_records.get(user_id)
		
		if latest_record == None:
			return self.cfg["itemboxes_initial"]
			
		time_since = time.time() - latest_record.time
		
		amount = math.floor(latest_record.amount + time_since / self.cfg["itemboxes_regen_time"])
		amount = max(amount, 0)
		amount = min(amount, self.cfg["itemboxes_max"])
		return amount
		
	
	# Computes how many seconds remain to regenerate the next itembox.
	def time_until_regen(self, user_id):
		latest_record = self.latest_records.get(user_id)
		
		if latest_record == None:
			return None
			
		time_since = time.time() - latest_record.time
		return self.cfg["itemboxes_regen_time"] - (time_since % self.cfg["itemboxes_regen_time"])
		
		
	def can_spend(self, user_id, amount):
		return self.get(user_id) >= amount
		
		
	def spend(self, user_id, cost):
		self.latest_records[user_id] = Record(self.get(user_id) - cost, time.time())