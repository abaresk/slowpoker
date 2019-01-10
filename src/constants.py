
import re

types = ['normal', 'fire', 'fighting', 'water', 'flying', 'grass', 'poison',
		 'electric', 'ground', 'psychic', 'rock', 'ice', 'bug', 'dragon', 
		 'ghost', 'dark', 'steel', 'fairy']

typeEffChart = {
	'normal': [],
	'fighting': ['normal', 'rock', 'steel', 'ice', 'dark'],
	'flying': ['fighting', 'bug', 'grass'],
	'poison': ['grass', 'fairy'],
	'ground': ['poison', 'rock', 'steel', 'fire', 'electric'],
	'rock': ['flying', 'bug', 'fire', 'ice'],
	'bug': ['grass', 'psychic', 'dark'],
	'ghost': ['ghost', 'psychic'],
	'steel': ['rock', 'ice'],
	'fire': ['bug', 'steel', 'grass', 'ice'],
	'water': ['ground', 'rock', 'fire'],
	'grass': ['ground', 'rock', 'water'],
	'electric': ['flying', 'water'],
	'psychic': ['fighting', 'poison'],
	'ice': ['flying', 'ground', 'grass', 'dragon'],
	'dragon': ['dragon'],
	'dark': ['ghost', 'psychic'],
	'fairy': ['fighting', 'dragon', 'dark']
}

NUM_LEVELS = 3
NUM_TYPES = len(types)
SIZE_DECK = NUM_TYPES * NUM_LEVELS
SIZE_HAND = 5

def card2name(num):
	return types[num // NUM_LEVELS] + str(num % NUM_LEVELS + 1)

def name2card(card_name):
	name = re.sub("[0-9]","",card_name).strip()
	level = re.sub("[^0-9]", "", card_name).strip()
	return types.index(name) * NUM_LEVELS + int(level) - 1
