import math


class ScoreManager:

	def __init__(self, cfg):
		self.cfg = cfg
		self.score_per_user = dict()
		
		
	def get(self, user):
		return self.score_per_user.setdefault(user, self.cfg.STARTING_VR)
		
		
	def add(self, user, delta):
		score = self.get(user)
		
		score += delta
		score = max(self.cfg.MIN_VR, score)
		score = min(self.cfg.MAX_VR, score)
		
		self.score_per_user[user] = score