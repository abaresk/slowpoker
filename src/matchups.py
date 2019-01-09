
'''
Functionality for inter-hand combat system

After each player has drawn their hand of 5 cards, their cards will attempt
to knock out some of the players cards. This game is programmed so that each
player's hand will reduce the opponent's hand as much as is possible.

Matchup is a collection of functions that will be used for one hand to attack
another.
'''

from constants import *

class Matchup():
	
	def handCmp(self, hand1, hand2):
		'''
		Returns: 
			* 1 if hand1 is ranked higher than hand2 
			* 0 if hand1 is tied with hand2
			* -1 if hand1 is ranked worse than hand2
		'''
		h1, h2 = hand1[:], hand2[:]

		while h1 and h2:
			(hrank1, hwin1), (hrank2, hwin2) = self.findHandRank(h1), self.findHandRank(h2)

			if hrank1 != hrank2:
				return 1 if hrank1 > hrank2 else -1

			# They're tied at the same rank, so check level differences
			# Winner goes to the winning set with greatest level sum
			sum1, sum2 = sum([x % NUM_LEVELS + 1 for i,x in enumerate(h1) if i in hwin1]), sum([x % NUM_LEVELS + 1 for i,x in enumerate(h2) if i in hwin2])
			if sum1 != sum2:
				return 1 if sum1 > sum2 else -1

			# Level sums were equal for both hands' winning cards
			# Remove winning cards from both hands and try again
			h1, h2 = [x for i,x in enumerate(h1) if i not in hwin1], [x for i,x in enumerate(h2) if i not in hwin2]

		return 0


	def findHandRank(self, hand):
		'''
		Return rank of hand and winning indices of cards in that hand

		Hand ranks:
			* 11	-> 3 in evo set, 2 in evo set
			* 10	-> 5 fully evolved
			* 9		-> 5 same level
			* 8		-> 3 in evo set only
			* 7		-> 2 in evo set, 2 in evo set
			* 6		-> 4 same level
			* 5		-> 3 same level, 2 same level
			* 4		-> 3 same level only
			* 3		-> 2 in evo set only
			* 2		-> 2 same level, 2 same level
			* 1		-> 2 same level (only possible when len(cards) < 5)
			* 0		-> nothing
		'''

		typeCounts  = [NUM_LEVELS for x in range(NUM_TYPES)]
		levelCounts = [NUM_TYPES for x in range(NUM_LEVELS)]

		for card in hand:
			typeCounts[card // NUM_LEVELS] -= 1
			levelCounts[card % NUM_LEVELS] -= 1


		# 3 in evo set, 2 in evo set
		if 0 in typeCounts and 1 in typeCounts:
			return (11, self._winnerIndices(hand, 'evo', [typeCounts.index(0), typeCounts.index(1)]))

		# 5 fully evolved
		elif levelCounts[2] == NUM_TYPES - 5:
			return (10, self._winnerIndices(hand, 'level', [2]))

		# 5 in same level
		elif NUM_TYPES - 5 in levelCounts:
			return (9, self._winnerIndices(hand, 'level', [levelCounts.index(NUM_TYPES - 5)]))

		# 3 in evo set only
		elif 0 in typeCounts:
			return (8, self._winnerIndices(hand, 'evo', [typeCounts.index(0)]))

		# 2 in evo set, 2 in evo set
		elif len([x for x in typeCounts if x == 1]) == 2:
			return (7, self._winnerIndices(hand, 'evo', [i for i,x in enumerate(typeCounts) if x == 1]))

		# 4 same level
		elif NUM_TYPES - 4 in levelCounts:
			return (6, self._winnerIndices(hand, 'level', [levelCounts.index(NUM_TYPES - 4)]))

		# 3 same level, 2 same level
		elif NUM_TYPES - 3 in levelCounts and NUM_TYPES - 2 in levelCounts:
			return (5, self._winnerIndices(hand, 'level', [levelCounts.index(NUM_TYPES - 3), levelCounts.index(NUM_TYPES - 2)]))

		# 3 same level only
		elif NUM_TYPES - 3 in levelCounts:
			return (4, self._winnerIndices(hand, 'level', [levelCounts.index(NUM_TYPES - 3)]))

		# 2 in evo set only
		elif 1 in typeCounts:
			return (3, self._winnerIndices(hand, 'evo', [typeCounts.index(1)]))

		# 2 same level, 2 same level
		elif len([x for x in levelCounts if x == NUM_TYPES - 2]) == 2:
			return (2, self._winnerIndices(hand, 'level', [i for i,x in enumerate(levelCounts) if x == NUM_TYPES - 2]))

		# 2 same level only (can only happen with hand of size < 5)
		elif NUM_TYPES - 2 in levelCounts:
			return (1, self._winnerIndices(hand, 'level', [levelCounts.index(NUM_TYPES - 2)]))

		# nothing
		else:
			return (0, [x for x in range(len(hand))])


	def _winnerIndices(self, hand, searchType, searchParams):
		''' 
		Find cards in a hand that match the given level or given evolution set

		searchType can be either 'level' or 'evo'
		searchParams is a list of levels or type IDs
		'''
		output = []

		for i,card in enumerate(hand):
			if searchType == 'level' and card % NUM_LEVELS in searchParams:
				output.append(i)
			elif searchType == 'evo' and card // NUM_LEVELS in searchParams:
				output.append(i)

		return output

