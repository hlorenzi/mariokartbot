from collections import deque
		
		
class Message:
	def __init__(self, user_id, msg_id):
		self.user_id = user_id
		self.msg_id = msg_id


# Stores a list of messages per channel of a server.
class MessageLogManager:
	def __init__(self, cfg):
		self.cfg = cfg
		self.channel_logs = dict()
		
		
	def record_message(self, channel_id, user_id, msg_id):
		# Append new message.
		channel_log = self.get_messages(channel_id)
		channel_log.append(Message(user_id, msg_id))
		
		# Cap max log length by removing the oldest messages.
		while len(channel_log) > self.cfg["max_messagelog_len_per_channel"]:
			channel_log.popleft()
			
			
	def get_messages(self, channel_id):
		return self.channel_logs.setdefault(channel_id, deque())