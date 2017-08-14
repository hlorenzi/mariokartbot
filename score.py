import math
from bisect import bisect_left
from bisect import bisect_right


class ScoreManager:
	def __init__(self, cfg):
		self.cfg = cfg
		self.user_id_to_score = dict()
		self.sorted_scores = list()
		self.sorted_user_ids = list()
		
		
	def get(self, user_id):
		return self.user_id_to_score.get(user_id, self.cfg["vr_initial"])
		
		
	def add(self, user_id, delta):
		score = self.get(user_id)
		
		self.sorted_remove(user_id, score)
	
		score += delta
		score = max(score, self.cfg["vr_min"])
		score = min(score, self.cfg["vr_max"])
		
		self.user_id_to_score[user_id] = score
		
		self.sorted_add(user_id, score)
		
		
	def get_sorted_user_ids(self):
		return self.sorted_user_ids
		
		
	def get_index(self, user_id):
		score = self.get(user_id)
		i = bisect_left(self.sorted_scores, score)
		while True:
			if i == len(self.sorted_scores):
				return None
				
			if self.sorted_scores[i] != score:
				return None
		
			if self.sorted_user_ids[i] == user_id:
				return i
				
			i += 1
		
		
	def get_ranking(self, user_id):
		score = self.get(user_id)
		return len(self.sorted_scores) - bisect_right(self.sorted_scores, score) + 1
		
		
	def sorted_remove(self, user_id, score):
		i = bisect_left(self.sorted_scores, score)
		while True:
			if i == len(self.sorted_scores):
				return
				
			if self.sorted_scores[i] != score:
				return
		
			if self.sorted_user_ids[i] == user_id:
				del self.sorted_scores[i]
				del self.sorted_user_ids[i]
				return
				
			i += 1
		
	
	def sorted_add(self, user_id, score):
		i = bisect_left(self.sorted_scores, score)
		self.sorted_scores.insert(i, score)
		self.sorted_user_ids.insert(i, user_id)