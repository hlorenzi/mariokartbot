import asyncio
import discord
import random
from threading import Thread
from config import load_config
from replier import Replier
from mariokart import MarioKartManager
from item_banana import ItemBanana


class DiscordIO:
	def __init__(self, async_queue, client):
		self.async_queue = async_queue
		self.client = client
		
		
	def delete_msg(self, channel_id, user_id, msg_id):
		self.async_queue.append(self.client.delete_message(msg_id))
		
		
	def send_msg(self, channel_id, content):
		self.async_queue.append(self.client.send_message(channel_id, content))
		
		
	def get_user_mention(self, user_id):
		return user_id.mention
		
	
	def get_message_mentions(self, msg_id):
		return msg_id.mentions
		
		
class Scheduler:
	def __init__(self):
		self.delay = None
		self.thread = None
		
		
	def clear(self):
		self.delay = None
		self.thread = None
		
		
	def delay_task(self, delay, thread):
		self.delay = delay
		self.thread = thread


cfg = load_config()
if cfg["bot_token"] == None:
	print("Please set the bot_token in the config.json file!")
	exit()


random.seed()
client = discord.Client()
async_queue = list()
scheduler = Scheduler()
io = DiscordIO(async_queue, client)
replier = Replier(io, cfg)
mk = MarioKartManager(io, replier, scheduler, cfg)


@client.event
async def on_ready():
	print("Logged in as:")
	print(client.user.name)
	print(client.user.id)
	print("---")


@client.event
async def on_message(msg):
	if msg.content.startswith("=q"):
		exit()
		
	if msg.content.startswith("=bothold"):
		mk.held_items[client.user] = ItemBanana(cfg, client.user)
		return
	
	thread = Thread(target = mk.receive_msg, args = (msg.channel, msg.author, msg, msg.content))
	
	while thread != None:
		scheduler.clear()
		async_queue.clear()
		
		thread.start()
		thread.join()
		
		thread = scheduler.thread
		delay = scheduler.delay
		
		for fn in async_queue:
			await fn
			
		if thread != None:
			await asyncio.sleep(delay)


client.run(cfg["bot_token"])