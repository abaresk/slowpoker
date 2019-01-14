
import random
from collections import defaultdict


from src.matchups import Matchup
from src.constants import *

N = 500000

m = Matchup()

def addCount(counts, hand):
	rank, winners = m.findHandRank(hand)
	counts[rank] += 1
	return


def simulateDraws():
	counts = defaultdict(int)
	for trial in range(N):
		hand = random.sample(range(SIZE_DECK), 10)
		attHand = hand[:5]
		defHand = hand[5:]

		strat1 = m.bestStrategy(attHand, defHand)
		strat2 = m.bestStrategy(defHand, attHand)

		addCount(counts, strat1.defHand)
		addCount(counts, strat2.defHand)


	
	print(sorted(counts.items()))

	if sum(counts.values()) != 2*N:
		print('Bad calc')

	return

