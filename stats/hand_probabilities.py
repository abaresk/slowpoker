
import numpy as np 

NUM_TYPES = 18
NUM_LEVELS = 3
DECK_SIZE = NUM_TYPES * NUM_LEVELS
N = 10000

def addCount(counts, hand):
	typeCounts = [NUM_LEVELS for x in range(NUM_TYPES)]
	levelCounts = [NUM_TYPES for x in range(NUM_LEVELS)]

	for card in hand:
		typeCounts[card // NUM_LEVELS] -= 1
		levelCounts[card % NUM_LEVELS] -= 1

	# full evolution set, 2 in another
	if any(map(lambda x: x == 0, typeCounts)) and any(map(lambda x: x == 1, typeCounts)):
		counts[0] += 1

	# full evolution set
	elif any(map(lambda x: x == 0, typeCounts)):
		counts[3] += 1

	# 2 pair evolution set
	elif len(list(filter(lambda x: x == 1, typeCounts))) == 2:
		counts[4] += 1

	# else
	else:
		counts[7] += 1


	# 5 fully evolved 
	if levelCounts[0] == NUM_TYPES - 5:
		counts[1] += 1

	# 5 same level
	elif any(map(lambda x: x == NUM_TYPES - 5, levelCounts)):
		counts[2] += 1

	# 4 fully evolved
	elif levelCounts[0] == NUM_TYPES - 4:
		counts[5] += 1

	# 4 same level
	elif any(map(lambda x: x == NUM_TYPES - 4, levelCounts)):
		counts[6] += 1

	# else
	else:
		counts[7] += 1


	# only true else if it is else in both of the above
	counts[7] -= 1

	return


def simulateDraws():
	counts = [0 for x in range(8)]

	for trial in range(N):
		hand = np.random.choice(DECK_SIZE, 5, False)
		addCount(counts, hand)

	
	print(counts)

	if sum(counts) != N:
		print('Bad calc')

	return

for i in range(100):
	simulateDraws()


