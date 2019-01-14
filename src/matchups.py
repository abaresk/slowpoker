
'''
Functionality for inter-hand combat system

After each player has drawn their hand of 5 cards, their cards will attempt
to knock out some of the players cards. This game is programmed so that each
player's hand will reduce the opponent's hand as much as is possible.

Matchup is a collection of functions that will be used for one hand to attack
another.
'''

from src.constants import *

class Strategy():
	'''
	Final state of matchup, showing the opponent's reduced hand and the moves that
	reduced it
	'''
	def __init__(self, defHand, moveHistory):
		self.defHand = defHand[:]
		self.moveHistory = moveHistory[:]
		return


class Matchup():

	def bestStrategy(self, hAttack, hDefense):
		memoStrategy = {}

		# moveHistory stores the sequence of (attCard, defCard) pairs 
		# representing 1 token that attCard used against defCard
		moveHistory = []

		# Each team is a dictionary mapping the card to its token count
		attTeam = {card : card % NUM_LEVELS + 1 for card in hAttack}
		defTeam = {card : card % NUM_LEVELS + 1 for card in hDefense}

		return self._bestStrategyAux(attTeam, defTeam, memoStrategy, moveHistory)

	def _bestStrategyAux(self, attTeam, defTeam, memoStrategy, moveHistory):
		# use memoized solution when possible
		if (self._tuplify(attTeam), self._tuplify(defTeam)) in memoStrategy:
			return memoStrategy[(self._tuplify(attTeam), self._tuplify(defTeam))]

		attHand = [card for card, val in attTeam.items() if val > 0]
		defHand = [card for card, val in defTeam.items() if val > 0]

		# defTargets gives top threats, which should be targeted
		defTargets = self._findTargets(attTeam, defTeam, attHand, defHand)

		# if there's nobody to attack, return the final hand and the moves made
		if not defTargets:
			return Strategy(defHand, moveHistory)

		# out of all ways to expend 1 token, we want to return the one that 
		# damages the opponent most
		bestStrat = Strategy(defHand, moveHistory)	# default, do nothing

		# for each defender...
		for defCard in defTargets:
			#... find attackers with a super-effective attack...
			for attCard in attHand:
				if types[defCard // NUM_LEVELS] in typeEffChart[types[attCard // NUM_LEVELS]]:
					
					#... and see what happens when they spend a token
					self._prepareState(attTeam, defTeam, attCard, defCard, moveHistory, -1)

					strat = self._bestStrategyAux(attTeam, defTeam, memoStrategy, moveHistory)
					bestStrat = strat if self.handCmp(strat.defHand, bestStrat.defHand) < 0 else bestStrat

					self._prepareState(attTeam, defTeam, attCard, defCard, moveHistory, 1)


		memoStrategy[(self._tuplify(attTeam), self._tuplify(defTeam))] = bestStrat

		return bestStrat


	# find cards in defender's hand that should be targeted
	def _findTargets(self, attTeam, defTeam, attHand, defHand):
		targets = set()

		while defHand and not targets:
			defRank, defWinners = self.findHandRank(defHand)

			# return defTargets if we can attack any of them
			for defIndex in defWinners:
				for attCard in attHand:
					if types[defHand[defIndex] // NUM_LEVELS] in typeEffChart[types[attCard // NUM_LEVELS]]:
						targets.add(defHand[defIndex])

			# if attTeam can't attack any top-tier threats...
			if not targets:
				#... retry with next highest rank
				defHand = [card for i,card in enumerate(defHand) if i not in defWinners]

		return targets

	def _prepareState(self, attTeam, defTeam, attCard, defCard, moveHistory, delta):
		attTeam[attCard] += delta
		defTeam[defCard] += delta
		if delta < 0:
			moveHistory.append((attCard, defCard))
		else:
			moveHistory.pop()
		return

	def _tuplify(self, dict):
		return tuple(sorted(dict.items()))


	# for debugging
	def _memoRanks(self, memoStrategy):
		s = set()
		for strat in memoStrategy.values():
			s.add(strat)
		return [self.findHandRank(strat.defHand)[0] for strat in s]

	def _memoChecker(self, memoStrategy, attTeam, defTeam):
		output = []
		s = set()
		for st in memoStrategy.values():
			s.add(st)

		strat = memoStrategy[(self._tuplify(attTeam), self._tuplify(defTeam))]

		for st in s:
			output.append(self.handCmp(st.defHand, strat.defHand))

		return output


	def handCmp(self, hand1, hand2):
		'''
		Returns: 
			* 1 if hand1 is ranked higher than hand2 
			* 0 if hand1 is tied with hand2
			* -1 if hand1 is ranked worse than hand2
		'''
		if (hand1 or hand2) is None:
			return 0

		if hand1 is None or hand2 is None:
			return 1 if hand1 else -1

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

		return 1 if h1 else -1 if h2 else 0



	def findHandRank(self, hand):
		'''
		Return rank of hand and winning indices of cards in that hand

		Hand ranks:
			* 11 	-> 3 in evo set, 2 in evo set
			* 10 	-> 5 fully evolved
			* 9 	-> 5 same level
			* 8 	-> 3 in evo set only
			* 7 	-> 2 in evo set, 2 in evo set
			* 6 	-> 4 same level
			* 5 	-> 3 same level, 2 same level
			* 4 	-> 3 same level only
			* 3 	-> 2 in evo set only
			* 2 	-> 2 same level, 2 same level
			* 1 	-> 2 same level (only possible when len(cards) < 5)
			* 0 	-> nothing
		'''

		typeCounts  = [NUM_LEVELS for x in range(NUM_TYPES)]
		levelCounts = [NUM_TYPES for x in range(NUM_LEVELS)]

		for card in hand:
			typeCounts[card // NUM_LEVELS] -= 1
			levelCounts[card % NUM_LEVELS] -= 1


		# full house (types)
		if 0 in typeCounts and 1 in typeCounts:
			return (9, self._winnerIndices(hand, 'evo', [typeCounts.index(0), typeCounts.index(1)]))

		# flush (level)
		elif NUM_TYPES - 5 in levelCounts:
			return (8, self._winnerIndices(hand, 'level', [levelCounts.index(NUM_TYPES - 5)]))

		# flush (types)
		elif 0 in typeCounts:
			return (7, self._winnerIndices(hand, 'evo', [typeCounts.index(0)]))

		# two pair (types)
		elif len([x for x in typeCounts if x == 1]) == 2:
			return (6, self._winnerIndices(hand, 'evo', [i for i,x in enumerate(typeCounts) if x == 1]))

		# quadruple (level)
		elif NUM_TYPES - 4 in levelCounts:
			return (5, self._winnerIndices(hand, 'level', [levelCounts.index(NUM_TYPES - 4)]))

		# full house (level)
		elif NUM_TYPES - 3 in levelCounts and NUM_TYPES - 2 in levelCounts:
			return (4, self._winnerIndices(hand, 'level', [levelCounts.index(NUM_TYPES - 3), levelCounts.index(NUM_TYPES - 2)]))

		# This rank would mess with the final probabilities and incentives
		# # pair (types)
		# elif 1 in typeCounts:
		# 	return (4, self._winnerIndices(hand, 'evo', [typeCounts.index(1)]))

		# two pair (level)
		elif len([x for x in levelCounts if x == NUM_TYPES - 2]) == 2:
			return (3, self._winnerIndices(hand, 'level', [i for i,x in enumerate(levelCounts) if x == NUM_TYPES - 2]))

		# triple (level)
		elif NUM_TYPES - 3 in levelCounts:
			return (2, self._winnerIndices(hand, 'level', [levelCounts.index(NUM_TYPES - 3)]))

		# pair (level)
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

