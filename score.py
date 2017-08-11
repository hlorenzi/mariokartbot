import math


class ScoreManager:
	def __init__(self, cfg):
		self.cfg = cfg
		self.scores = dict()
		
		
	def get(self, user_id):
		return self.scores.setdefault(user_id, self.cfg["vr_initial"])
		
		
	def add(self, user_id, delta):
		score = self.get(user_id)
		
		score += delta
		score = max(score, self.cfg["vr_min"])
		score = min(score, self.cfg["vr_max"])
		
		self.scores[user_id] = score