
import random
from collections import defaultdict
import concurrent.futures


from src.matchups import Matchup
from src.constants import *

N = 5000

m = Matchup()

def addCount(counts, hand):
	rank, winners = m.findHandRank(hand)
	counts[rank] += 1
	return

def simulateDrawsAux(counts):
	hand = random.sample(range(SIZE_DECK), 10)
	attHand = hand[:5]
	defHand = hand[5:]

	strat1 = m.bestStrategy(attHand, defHand)
	strat2 = m.bestStrategy(defHand, attHand)

	addCount(counts, strat1.defHand)
	addCount(counts, strat2.defHand)
	return


def simulateDraws():
	with concurrent.futures.ProcessPoolExecutor() as executor:

		counts = defaultdict(int)

		# for trial, retVal in zip(range(N), executor.map(lambda p: simulateDrawsAux(*p), counts)):
		# 	print(trial)

		for trial in range(N):
			simulateDrawsAux(counts)




	
		print(sorted(counts.items()))

		if sum(counts.values()) != 2*N:
			print('Bad calc')

	return

