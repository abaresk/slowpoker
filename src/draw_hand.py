
import random
import numpy as np
from collections import defaultdict

# Constants

types = ['normal', 'fire', 'fighting', 'water', 'flying', 'grass', 'poison',
		 'electric', 'ground', 'psychic', 'rock', 'ice', 'bug', 'dragon', 
		 'ghost', 'dark', 'steel', 'fairy']

NUM_LEVELS = 3
SIZE_DECK = len(types) * NUM_LEVELS
SIZE_HAND = 5


class Table():
	def __init__(self, numPlayers):
		self.numPlayers = numPlayers
		self.hands = self.redraw()

	def redraw(self):
		hands = random.sample(range(SIZE_DECK), SIZE_HAND * self.numPlayers)
		self.hands = np.reshape(hands, (self.numPlayers, SIZE_HAND)).tolist()
		return

	def display(self):
		for hand in self.hands:
			for card in hand:
				print(types[card//NUM_LEVELS] + str(card%NUM_LEVELS+1), end=' ')
			print()
		print()
		return

	def sortHands(self):
		for i, hand in enumerate(self.hands):
			self.hands[i] = self._sortHand(hand)
		return

	def _sortHand(self, hand):
		# group into same types
		handTypes = defaultdict(list)
		for card in hand:
			handTypes[card // NUM_LEVELS].append(card)

		sortedHand = list(handTypes.values())

		# sort each subgroup
		for i, types in enumerate(sortedHand):
			sortedHand[i].sort(key=lambda x: x%NUM_LEVELS, reverse=True)

		# sort each group
		sortedHand.sort(key=self._sumlist, reverse=True)

		return [x for types in sortedHand for x in types]

	# Auxiliary sorting function
	def _sumlist(self, lst):
		return sum([(1 + x % NUM_LEVELS) for x in lst])


	
# Test
t = Table(2)
for i in range(6):
	t.redraw()
	t.sortHands()
	t.display()
