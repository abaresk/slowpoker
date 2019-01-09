
import random
import numpy as np
from collections import defaultdict

from constants import *
from matchups import Matchup

class Table():
	def __init__(self, numPlayers):
		self.numPlayers = numPlayers
		self.hands = None
		self.reserve = None
		self.redraw()

	def redraw(self):
		drawn = random.sample(range(SIZE_DECK), 2 * SIZE_HAND * self.numPlayers)
		hands = drawn[:SIZE_HAND * self.numPlayers]
		self.hands = np.reshape(hands, (self.numPlayers, SIZE_HAND)).tolist()
		self.reserve = drawn[SIZE_HAND * self.numPlayers:]
		return

	def display(self):
		for hand in self.hands:
			for card in hand:
				print(self._nameCard(card), end=' ')
			print()
		print()
		return

	def _nameCard(self, num):
		return types[num // NUM_LEVELS] + str(num % NUM_LEVELS + 1)

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
m = Matchup()

for i in range(1000):
	t.redraw()
	t.sortHands()

	for hand in t.hands:
		htype = m.findHandType(hand)
		if htype[0] > 9:
			print(htype)
			t.display()

