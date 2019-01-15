
import re

types = ['normal', 'fire', 'fight', 'water', 'flying', 'grass', 'poison',
		 'elec', 'ground', 'psy', 'rock', 'ice', 'bug', 'dragon', 
		 'ghost', 'dark', 'steel', 'fairy']

typeEffChart = {
	'normal': [],
	'fight': ['normal', 'rock', 'steel', 'ice', 'dark'],
	'flying': ['fight', 'bug', 'grass'],
	'poison': ['grass', 'fairy'],
	'ground': ['poison', 'rock', 'steel', 'fire', 'elec'],
	'rock': ['flying', 'bug', 'fire', 'ice'],
	'bug': ['grass', 'psy', 'dark'],
	'ghost': ['ghost', 'psy'],
	'steel': ['rock', 'ice'],
	'fire': ['bug', 'steel', 'grass', 'ice'],
	'water': ['ground', 'rock', 'fire'],
	'grass': ['ground', 'rock', 'water'],
	'elec': ['flying', 'water'],
	'psy': ['fight', 'poison'],
	'ice': ['flying', 'ground', 'grass', 'dragon'],
	'dragon': ['dragon'],
	'dark': ['ghost', 'psy'],
	'fairy': ['fight', 'dragon', 'dark']
}

NUM_LEVELS = 3
NUM_TYPES = len(types)
SIZE_DECK = NUM_TYPES * NUM_LEVELS
SIZE_HAND = 5

NUM_PLAYERS = 2

def card2name(num):
	return types[num // NUM_LEVELS] + str(num % NUM_LEVELS + 1)

def name2card(card_name):
	name = re.sub("[0-9]","",card_name).strip()
	level = re.sub("[^0-9]", "", card_name).strip()
	return types.index(name) * NUM_LEVELS + int(level) - 1
