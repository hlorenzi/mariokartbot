import random


class ItemGreenShell:
	def __init__(self, cfg, user_id):
		self.cfg = cfg
		self.user_id = user_id

	
	def cost(self):
		return self.cfg["greenshell_cost"]
		
	
	def can_hold(self):
		return True
		
	
	def can_specify_target(self):
		return True
	
		
	def use(self, mk, channel_id, msg_id, specified_target, was_held):
		target_user_id = specified_target
		if target_user_id == None or random.random() >= self.cfg["greenshell_hit_target_chance"]:
			target_user_id = self.choose_target(mk, channel_id, msg_id)
		
		user_state = mk.get_user_state(self.user_id)
		target_state = mk.get_user_state(target_user_id)
		simulated_hit = mk.simulate_hit(target_user_id, self.cfg["greenshell_hit_vr"], False)
		
		if not was_held:
			mk.itemboxes.spend(self.user_id, self.cost())
		
		mk.replier.reply_item_use_and_hit(channel_id, user_state, target_state, self, was_held, simulated_hit)
		
		mk.perform_hit(simulated_hit)
		mk.perform_random_banana_hit(channel_id, self.user_id)
	
	
	def choose_target(self, mk, channel_id, msg_id_to_avoid):
		channel_log = mk.msglog.get_messages(channel_id)
		
		for i in range(len(channel_log)):
			possible_target_msg = channel_log[-1 - i]
			
			if possible_target_msg.msg_id == msg_id_to_avoid:
				continue
			
			if random.random() < self.cfg["greenshell_hit_player_chance"]:
				return possible_target_msg.user_id
				
			if random.random() < self.cfg["greenshell_hit_nobody_chance"]:
				break
				
		return None