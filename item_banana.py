class ItemBanana:
	def __init__(self, cfg, user_id):
		self.cfg = cfg
		self.user_id = user_id
		self.channel_id = None
	
	
	def cost(self):
		return self.cfg["banana_cost"]
		
	
	def can_hold(self):
		return True
	
		
	def use(self, mk, channel_id, msg_id, was_held):
		user_state = mk.get_user_state(self.user_id)
		
		if not was_held:
			mk.itemboxes.spend(self.user_id, self.cost())
		
		mk.replier.reply_place_down_item(user_state, channel_id, self, was_held)
		
		self.channel_id = channel_id
		mk.place_down_item(self)
		
		
	def slip(self, mk, channel_id, target_user_id):
		user_state = mk.get_user_state(self.user_id)
		target_state = mk.get_user_state(target_user_id)
		
		simulated_hit = mk.simulate_hit(target_user_id, self.cfg["banana_hit_vr"], True)
		
		mk.replier.reply_item_hit(channel_id, user_state, target_state, self, False, simulated_hit)
		
		mk.perform_hit(simulated_hit)
		mk.destroy_placed_down_item(self)