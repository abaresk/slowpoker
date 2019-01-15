
import random
import numpy as np
import getpass
from collections import defaultdict

from src.constants import *
from src.matchups import Matchup

NUM_CARDS_COVERED = 2

class Player():
	def __init__(self, name=None, pw=None):
		self.name = name
		self._pw = pw
		return

class Table():
	def __init__(self, numPlayers):
		self.currentPlayer = 0
		self.numPlayers = numPlayers
		self.players = {}

		self.stocks = []
		self.bets = []
		
		self.hands = None
		self.reserve = None
		self.viewHands = None
		self.redraw()

		self.matchup = Matchup()

		# Copy of self.hands that can be optionally sorted for viewing

		return

	# new turn
	def redraw(self):
		drawn = random.sample(range(SIZE_DECK), 2 * SIZE_HAND * self.numPlayers)
		hands = drawn[:SIZE_HAND * self.numPlayers]
		self.hands = np.reshape(hands, (self.numPlayers, SIZE_HAND)).tolist()
		self.reserve = drawn[SIZE_HAND * self.numPlayers:]

		self.viewHands = self.hands[:]

		self.bets = [0 for i in range(self.numPlayers)]
		return


	def displayHand(self, playerId, isTransparent):
		if playerId == self.currentPlayer:
			print('Your hand:\t\t', end='')
		else:
			print("Opponent's hand:\t", end='')

		if playerId == self.currentPlayer or isTransparent:
			for card in self.hands[playerId]:
				print(card2name(card), end='\t')
		else:
			for i, card in enumerate(self.viewHands[playerId]):
				if i < NUM_CARDS_COVERED:
					print('****', end='\t')
				else:
					print(card2name(card), end='\t')
		print()
		return

	def displayTable(self, isTransparent):
		self.displayHand(not self.currentPlayer, isTransparent)
		self.displayHand(self.currentPlayer, isTransparent)
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
		hand_0_attacks = self.matchup.bestStrategy(self.hands[0], self.hands[1])
		hand_1_attacks = self.matchup.bestStrategy(self.hands[1], self.hands[0])

		hand_0_moves, hand_0_remaining = hand_0_attacks.moveHistory, hand_1_attacks.defHand
		hand_1_moves, hand_1_remaining = hand_1_attacks.moveHistory, hand_0_attacks.defHand

		if willPrintMoves:
			print(self.players[0].name + "'s moves:")
			self.printMoves(hand_0_moves)
			print(self.players[1].name + "'s moves:")
			self.printMoves(hand_1_moves)

		self.hands[0], self.hands[1] = hand_0_remaining, hand_1_remaining

		print()
		print(self.players[0].name + "'s final hand:")
		self.printHand(self.hands[0])

		print()
		print(self.players[1].name + "'s final hand:")
		self.printHand(self.hands[1])
		return

	def doWinnings(self):
		winner = self.matchup.handCmp(self.hands[0], self.hands[1])

		if winner > 0:
			print(self.players[0].name + '!!')
		elif winner < 0:
			print(self.players[1].name + ' !!')
		else:
			print('No one. It was a tie.')

		self._distributeWinnings(winner)
		return

	def _distributeWinnings(self, winner):
		if winner == 0:
			# each player gets their bets back
			for i in range(NUM_PLAYERS):
				self.stocks[i] += self.bets[i]
		
		else:
			potSum = sum(self.bets)

			handRank = self.matchup.findHandRank(self.hands[winner < 0])

			# if you guessed you'd win by that rank or higher...
			if handRank >= self.bets[winner < 0]:
				#...dealer adds pot * corresponding factor to your total
				potSum += self._getAddedPayout(potSum, handRank)

			self.hands[winner < 0] += potSum
		return 

	def _getAddedPayout(self, potSum, handRank):
		if handRank > 1:
			return potSum << (handRank - 2)
		elif handRank == 1:
			return potSum >> 1
		else:
			return 0



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

	def printStocks(self):
		for i in range(self.numPlayers):
			print(self.players[i].name + "'s coin stock:\t" + str(self.stocks[i]))
		return


	def sortHand(self):
		self.hands[self.currentPlayer] = self.sortedHand(self.hands[self.currentPlayer])
		return

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


	# Gameplay features
	def addPlayer(self, name, pw, stockInitial):
		assert(len(self.players) < 2)

		playerId = len(self.players)
		self.players[playerId] = Player(name, pw)

		self.stocks.append(stockInitial)
		self.bets.append(0)
		return

	def addBet(self, betVal):
		if betVal <= self.stocks[self.currentPlayer]:
			self.bets[self.currentPlayer] = betVal
			return True
		print('You do not have enough coins to make this bet.')
		return False

	def endTurn(self):
		self.switchPlayers()

		# "Hide" previous player's decisions
		for i in range(5000):
			print()

		self.authenticatePlayer()
		return

	def authenticatePlayer(self):
		print('Hello, ' + self.players[self.currentPlayer].name + '! Please enter your password.')
		pw = getpass.getpass(prompt='Password: ', stream=None)
		
		while pw != self.players[self.currentPlayer]._pw:
			print('That password was incorrect. Please enter your password.')
			pw = getpass.getpass(prompt='Password: ', stream=None)

		return



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
