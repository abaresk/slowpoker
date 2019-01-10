
from src.table import *
from src.matchups import Matchup

if __name__ == '__main__':
	t = Table(2)
	m = Matchup()


	# Test
	attHand = [name2card(x) for x in ['rock3', 'psychic2', 'steel2', 'dragon2', 'ice1']]
	defHand = [name2card(x) for x in ['steel3', 'steel1', 'ground3', 'flying2', 'poison2']]
	strat = m.bestStrategy(attHand, defHand)

	attHand = [name2card(x) for x in ['ghost2', 'ice2', 'fighting2', 'fighting1', 'fire1']]
	defHand = [name2card(x) for x in ['ice3', 'ice1', 'normal3', 'fairy2', 'steel2']]
	strat = m.bestStrategy(attHand, defHand)

	attHand = [name2card(x) for x in ['fighting2', 'fighting1', 'rock2', 'fire2', 'ghost1']]
	defHand = [name2card(x) for x in ['ice3', 'ice1', 'flying3', 'bug2', 'steel2']]
	strat = m.bestStrategy(attHand, defHand)	


	# for i in range(10):
	# 	t.redraw()
	# 	t.sortHands()

	# 	for hand in t.hands:
	# 		htype = m.findHandRank(hand)
	# 		print(htype)
	# 	t.display()


	# 	strat = m.bestStrategy(t.hands[1], t.hands[0])

	print('Everything passed')