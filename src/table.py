
import random
import numpy as np
from collections import defaultdict

from src.constants import *
from src.matchups import Matchup

NUM_CARDS_COVERED = 3


class Table():
	def __init__(self, numPlayers):
		self.currentPlayer = 0
		self.numPlayers = numPlayers
		self.players = {}
		
		self.hands = None
		self.reserve = None
		self.redraw()

		self.matchup = Matchup()

		return

	# new turn
	def redraw(self):
		drawn = random.sample(range(SIZE_DECK), 2 * SIZE_HAND * self.numPlayers)
		hands = drawn[:SIZE_HAND * self.numPlayers]
		self.hands = np.reshape(hands, (self.numPlayers, SIZE_HAND)).tolist()
		self.reserve = drawn[SIZE_HAND * self.numPlayers:]
		return


	def displayHand(self, playerId):
		if playerId == self.currentPlayer:
			print('Your hand:\t\t', end='')
		else:
			print("Opponent's hand:\t", end='')
		
		for i, card in enumerate(self.hands[playerId]):
			if playerId != self.currentPlayer and i < NUM_CARDS_COVERED:
				print('****', end='\t')
			else:
				print(card2name(card), end='\t')
		print()
		return

	def displayTable(self):
		self.displayHand(not self.currentPlayer)
		self.displayHand(self.currentPlayer)
		return
		



	def switchPlayers(self):
		self.currentPlayer ^= 1
		return

	def swapCards(self, swapSet):
		hand = self.hands[self.currentPlayer]
		self.hands[self.currentPlayer] = [card for i, card in enumerate(hand) if i not in swapSet]

		for i in range(len(swapSet)):
			self.hands[self.currentPlayer].append(self.reserve.pop())
		return


	def doHandBattle(self, willPrintMoves):
		'''
		Have each hand reduce the opponent's hand as much as possible.
		New hands take the spot of the old ones.
		'''
		hand_1_remaining, hand_0_moves = self.matchup.bestStrategy(self.hands[0], self.hands[1])
		hand_0_remaining, hand_1_moves = self.matchup.bestStrategy(self.hands[1], self.hands[0])

		if willPrintMoves:
			print("Player 1's moves:")
			self.printMoves(hand_0_moves)
			print("Player 2's moves:")
			self.printMoves(hand_1_moves)

		self.hands[0], self.hands[1] = hand_0_remaining, hand_1_remaining

		print("Player 1's final hand:")
		self.printHand(self.hands[0])
		print("Player 2's final hand:")
		self.printHand(self.hands[1])
		return

	def printWinner(self):
		winner = self.matchup.handCmp(self.hands[0], self.hands[1])

		if winner > 0:
			print(self.players[0].name + 'wins!')
		elif winner < 0:
			print(self.players[1].name + 'wins!')
		else:
			print('It was a tie!')
		return

	def printMoves(self, moves):
		for move in moves:
			print(card2name(move[0]) + ' attacked ' + card2name(move[1]) + '!')
		print()
		return


	def printHand(self, hand):
		for card in hand:
			print(card2name(card), end=' ')
		print()
		return


	# def sortHands(self):
	# 	for i, hand in enumerate(self.hands):
	# 		self.hands[i] = self._sortHand(hand)
	# 	return

	def sortedHand(self, hand):
		# group into same types
		handTypes = defaultdict(list)
		for card in hand:
			handTypes[card // NUM_LEVELS].append(card)

		sortedTypes = list(handTypes.values())

		# sort each subgroup
		for i, types in enumerate(sortedTypes):
			sortedTypes[i].sort(key=lambda x: x%NUM_LEVELS, reverse=True)

		# sort each group
		sortedTypes.sort(key=self._sumlist, reverse=True)

		return [x for types in sortedTypes for x in types]

	# Auxiliary sorting function
	def _sumlist(self, lst):
		return sum([(1 + x % NUM_LEVELS) for x in lst])



# if __name__ == '__main__':
# 	t = Table(2)
# 	m = Matchup()

# 	for i in range(100):
# 		t.redraw()
# 		t.sortHands()

# 		for hand in t.hands:
# 			htype = m.findHandRank(hand)
# 			if htype[0] > 9:
# 				print(htype)
# 				t.display()
# 			htype = m.findHandRank(hand)
# 			# if htype[0] > 9:
# 			print(htype)

# 		t.display()
# 		rank = m.handCmp(t.hands[0], t.hands[1])

# 		print(rank)

# 	print('Everything passed')
