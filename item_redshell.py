import time
from threading import Thread


class ItemRedShell:
	def __init__(self, cfg, user_id):
		self.cfg = cfg
		self.user_id = user_id
		self.target_user_id = None

	
	def cost(self):
		return self.cfg["redshell_cost"]
		
	
	def can_hold(self):
		return True
	
		
	def use(self, mk, channel_id, msg_id, was_held):
		self.target_user_id = self.choose_target(mk, channel_id, msg_id)
		
		user_state = mk.get_user_state(self.user_id)
		target_state = mk.get_user_state(self.target_user_id)
		time_until_hit = self.cfg["redshell_time_until_hit"]
		
		if not was_held:
			mk.itemboxes.spend(self.user_id, self.cost())
		
		mk.replier.reply_item_use_delayed_target(channel_id, user_state, target_state, self, was_held, time_until_hit)
		mk.perform_random_banana_hit(channel_id, self.user_id)
		mk.scheduler.delay_task(time_until_hit, Thread(target = self.reach_target, args = (mk, channel_id, msg_id)))
		
		
	def reach_target(self, mk, channel_id, msg_id):
		user_state = mk.get_user_state(self.user_id)
		target_state = mk.get_user_state(self.target_user_id)
		simulated_hit = mk.simulate_hit(self.target_user_id, self.cfg["redshell_hit_vr"], False)
		
		mk.replier.reply_item_hit(channel_id, user_state, target_state, self, False, simulated_hit)
		
		mk.perform_hit(simulated_hit)
	
	
	def choose_target(self, mk, channel_id, msg_id_to_avoid):
		channel_log = mk.msglog.get_messages(channel_id)
		
		for i in range(len(channel_log)):
			possible_target_msg = channel_log[-1 - i]
			
			if possible_target_msg.msg_id == msg_id_to_avoid:
				continue
			
			if possible_target_msg.user_id == self.user_id:
				continue
			
			return possible_target_msg.user_id
				
		return None