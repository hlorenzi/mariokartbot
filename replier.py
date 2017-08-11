from mariokart import SimulatedHit
from item_greenshell import ItemGreenShell
from item_redshell import ItemRedShell
from item_banana import ItemBanana


class Replier:
	def __init__(self, io, cfg):
		self.io = io
		self.cfg = cfg
		
		
	def delete_msg(self, channel_id, user_id, msg_id):
		self.io.delete_msg(channel_id, user_id, msg_id)
		
		
	def send_msg(self, channel_id, content):
		self.io.send_msg(channel_id, content)
		
		
	def reply_invalid_command(self, user_state, channel_id, msg_id, content):
		reply = self.make_user_text(user_state) + ": "
		reply += "invalid command"
		self.send_msg(channel_id, reply)
		
		
	def reply_insufficient_itemboxes(self, user_state, channel_id, item):
		reply = self.make_user_text(user_state) + ": "
		reply += self.make_item_name(item) + " " + self.make_item_emoji(item) + " "
		reply += "costs " + str(item.cost()) + self.cfg["emoji_itembox"]
		self.send_msg(channel_id, reply)
		
	
	def reply_already_holding_item(self, user_state, channel_id, item):
		reply = self.make_user_text(user_state) + ": "
		reply += "you're already holding "
		reply += self.make_item_article(item) + " " + self.make_item_name(item) + " " + self.make_item_emoji(item) + "! "
		reply += "Maybe `=drop` it first"
		self.send_msg(channel_id, reply)
		
	
	def reply_no_held_item(self, user_state, channel_id):
		reply = self.make_user_text(user_state) + ": "
		reply += "you're not holding an item!"
		self.send_msg(channel_id, reply)
		
	
	def reply_cant_use_holding_item(self, user_state, channel_id, item):
		reply = self.make_user_text(user_state) + ": "
		reply += "you're holding "
		reply += self.make_item_article(item) + " " + self.make_item_name(item) + " " + self.make_item_emoji(item) + "! "
		reply += "`=drop` it first"
		self.send_msg(channel_id, reply)
	
	
	def reply_hold_item(self, user_state, channel_id, item):
		reply = self.make_user_text(user_state) + " "
		reply += "held "
		reply += self.make_item_article(item) + " " + self.make_item_name(item) + " " + self.make_item_emoji(item) + "!"
		self.send_msg(channel_id, reply)
	
	
	def reply_place_down_item(self, user_state, channel_id, item, was_held):
		reply = self.make_user_text(user_state) + " "
		reply += "placed down "
		
		if was_held:
			reply += "their held "
		else:
			reply += self.make_item_article(item) + " "
			
		reply += self.make_item_name(item) + " " + self.make_item_emoji(item) + "!"
		self.send_msg(channel_id, reply)
		
		
	def reply_item_use_and_hit(self, channel_id, user_state, target_state, item, was_held, simulated_hit):
		reply = self.make_user_text(user_state) + " "
		reply += "threw "
		
		if was_held:
			reply += "their held "
		else:
			reply += self.make_item_article(item) + " "
		
		if simulated_hit.kind == SimulatedHit.HIT_NOTHING:
			reply += self.make_item_name(item) + " " + self.make_item_emoji(item) + " "
			reply += "and it just crashed into a wall..."
			
		else:
			reply += self.make_target_hit_text("and it ", user_state, target_state, item, simulated_hit)
			
		self.send_msg(channel_id, reply)
		
		
	def reply_item_use_delayed_target(self, channel_id, user_state, target_state, item, was_held, delay):
		reply = self.make_user_text(user_state) + " "
		reply += "threw "
		
		if was_held:
			reply += "their held "
		else:
			reply += self.make_item_article(item) + " "
			
		reply += self.make_item_name(item) + " " + self.make_item_emoji(item) + " "
		reply += "targeting "
		reply += self.make_user_text(target_state) + " "
		
		reply += "in :clock3: " + str(delay) + "s!"
		self.send_msg(channel_id, reply)
		
		
	def reply_item_use_delayed_target_none(self, channel_id, user_state, target_state, item, was_held, delay):
		reply = self.make_user_text(user_state) + " "
		reply += "threw "
		
		if was_held:
			reply += "their held "
		else:
			reply += self.make_item_article(item) + " "
			
		reply += self.make_item_name(item) + " " + self.make_item_emoji(item) + " "
		reply += "and it just kept going forever..."
		self.send_msg(channel_id, reply)
		
		
	def reply_item_hit(self, channel_id, user_state, target_state, item, was_held, simulated_hit):
		reply = self.make_user_text(user_state) + "'s "
		
		if was_held:
			reply += "held "
		
		if simulated_hit.kind == SimulatedHit.HIT_NOTHING:
			reply += self.make_item_name(item) + " " + self.make_item_emoji(item) + " "
			reply += "just crashed into a wall..."
			
		else:
			reply += self.make_target_hit_text("", user_state, target_state, item, simulated_hit)
			
		self.send_msg(channel_id, reply)
		
		
	def make_item_name(self, item):
		names = {
			ItemGreenShell: "GREEN SHELL",
			ItemRedShell: "RED SHELL",
			ItemBanana: "BANANA PEEL"
		}
		
		return names[type(item)]
		
		
	def make_item_article(self, item):
		articles = {
			ItemGreenShell: "a",
			ItemRedShell: "a",
			ItemBanana: "a"
		}
		
		return articles[type(item)]
		
		
	def make_item_emoji(self, item):
		emojis = {
			ItemGreenShell: self.cfg["emoji_greenshell"],
			ItemRedShell: self.cfg["emoji_redshell"],
			ItemBanana: self.cfg["emoji_banana"]
		}
		
		return emojis[type(item)]
		
	
	
	def name(self):
		return "GREEN SHELL"
	
	
	def article(self):
		return "a"

	
	def emoji(self):
		return self.cfg["emoji_greenshell"]
		
		
	def make_target_hit_text(self, text_between_emoji_and_target, user_state, target_state, item, simulated_hit):
		if simulated_hit.kind == SimulatedHit.HIT_HELD_ITEM:
			reply = self.make_item_name(item) + " " + self.make_item_emoji(item) + " :boom: "
			reply += self.make_item_emoji(simulated_hit.held_item)
			reply += text_between_emoji_and_target
			reply += "hit the item held by " + self.make_user_text(target_state) + "!"
			return reply
		
		else:
			reply = self.make_item_name(item) + " " + self.make_item_emoji(item) + " :boom: "
			reply += text_between_emoji_and_target
			reply += "hit "
			
			if user_state == None or user_state.user_id != target_state.user_id:
				reply += self.make_user_text(target_state) + "! "
			else:
				reply += "**themselves**! "
			
			reply += "*(" + str(simulated_hit.vr_penalty) + " VR)*"
			
		return reply
		
		
	def make_user_text(self, state):
		text = "**"
		text += self.cfg["emoji_yoshi"] + " "
		text += self.io.get_user_mention(state.user_id)
		
		text += " ("
		text += str(state.vr) + " VR"
		text += ", "
		text += str(state.itemboxes) + self.cfg["emoji_itembox"]
		text += ")"
		
		text += "**"
		return text