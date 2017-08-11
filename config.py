import json


default_cfg = {
	"bot_token": None,

	"emoji_yoshi": None,
	"emoji_itembox": None,
	"emoji_greenshell": None,
	"emoji_redshell": None,
	"emoji_banana": None,
	
	"max_messagelog_len_per_channel": 100,
	
	"vr_initial": 1000,
	"vr_min": 0,
	"vr_max": 999999,
	
	"itemboxes_initial": 5,
	"itemboxes_max": 10,
	"itemboxes_regen_time": 1,
	
	"greenshell_cost": 3,
	"greenshell_hit_vr": -15,
	"greenshell_hit_target_chance": 0.2,
	"greenshell_hit_player_chance": 0.2,
	"greenshell_hit_nobody_chance": 0.2,
	
	"redshell_cost": 4,
	"redshell_hit_vr": -15,
	"redshell_time_until_hit": 5,
	
	"banana_cost": 3,
	"banana_hit_vr": -10,
	"banana_random_hit_chance": 0.2
}


def load_config():
	cfg = dict()
	cfg.update(default_cfg)
	
	with open("config.json") as f:
		cfg.update(json.load(f))
		
	return cfg