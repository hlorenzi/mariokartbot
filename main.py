import discord
import random
from config import load_config
from mariokart import MarioKartLogic


cfg = load_config()
if cfg["bot_token"] == None:
	print("Please set the bot_token in the config file!")
	exit()


random.seed()
client = discord.Client()
mariokart = MarioKartLogic(client, cfg)


@client.event
async def on_ready():
	print("Logged in as:")
	print(client.user.name)
	print(client.user.id)
	print("---")


@client.event
async def on_message(msg):
	await mariokart.handle_message(msg)
	# mariokart.print_logs()
	
	if msg.content.startswith("=q"):
		exit()


client.run(cfg["bot_token"])