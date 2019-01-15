
import getpass

from src.table import Table

INITIAL_STOCK = 100

# Game functions
class Game():
	def __init__(self):
		self.table = Table(2)
		return

	def gameBegin(self):
		print()
		print('Welcome to Slowpoker!!')
		print()
		print()
		return

	def initPlayers(self):
		for i in range(2):
			# Get name
			print('Hi Player ' + str(i+1) + '! Please enter your name.')
			name = input('--> ')

			# Get password
			print('Now please enter a password.')
			pw1 = getpass.getpass(prompt='Password: ', stream=None)
			print('Please confirm your password.')
			pw2 = getpass.getpass(prompt='Password: ', stream=None)

			while pw1 != pw2:
				print()
				print('Your passwords did not match. Please try again.')

				print('Please enter a password.')
				pw1 = getpass.getpass(prompt='Password: ', stream=None)
				print('Please confirm your password.')
				pw2 = getpass.getpass(prompt='Password: ', stream=None)


			self.table.addPlayer(name, pw1, INITIAL_STOCK)

			print("You're all set, " + name + '!')
			print()
		return

	# Game commands
	def giveOptions(self):
		print("'view {mine theirs}'\tlets you view your hand or your opponent's.")
		print("'view' \t\t\tlets you view the entire table")
		print("'sort' \t\t\tlets you sort your hand")
		print("'ranks'\t\t\tlets you view the different hand ranks")
		print("'bet <cost value>' \tlets you place a bet at rank whose cost is <cost value>")
		print("'swap <card numbers>' \tlets you swap out the cards you listed in <card numbers>")
		print("'end' \t\t\tends your turn")
		return

	def giveRanks(self):
		print("Cost\tPayout\tName\t\t\tDescription")
		print("9\t128\tFull house (types)\t3 mons same type, 2 mons same type")
		print("8\t64\tFlush (levels)\t\t5 mons same level")
		print("7\t32\tFlush (types)\t\t3 mons same type")
		print("6\t16\tTwo pair (types)\t2 mons same type, 2 mons same type")
		print("5\t8\tQuadruple (level)\t4 mons same level")
		print("4\t4\tFull house (level)\t3 mons same level, 2 mons same level")
		print("3\t2\tTwo pair (level)\t2 mons same level, 2 mons same level")
		print("2\t1\tTriple (level)\t\t3 mons same level")
		print("1\t1/2\tPair (level)\t\t2 mons same level")
		print("0\t0\tHigh level\t\totherwise, goes to higher level sum")
		return


	# Gameplay
	def doRound(self):
		# TODO: Take ante from both players

		self.doTurn()
		self.table.endTurn()
		self.doTurn()

		# Buffer between turns and results
		for i in range(5000):
			print()

		print('Your turns have ended. Here are your hands:')
		for i in range(2):
			print(self.table.players[i].name)
			self.table.displayHand(i, isTransparent=True)
			print()
		
		input('Continue? ')
		print('Now they will battle!')
		print()
		self.table.doHandBattle(willPrintMoves=True)
		print()

		input('And the winner is..... ')
		self.table.doWinnings()
		self.table.printStocks()
		return

	def doTurn(self):
		turnEnd = False
		swapUsed = False
		hasBet = False

		print('It is your turn, ' + self.table.players[self.table.currentPlayer].name + '.')
		
		while not turnEnd:
			print("Please type in a command, or type 'options' to learn about the commands.")
			command = input('--> ').strip().lower().split()

			if len(command) == 0:
				print('Invalid command')
			
			elif command[0] == 'options':
				self.giveOptions()
			
			elif command[0] == 'view':
				whoseHand = ['mine', 'theirs']
				if len(command) == 1:
					self.table.displayTable(isTransparent=False)
				elif command[1] not in whoseHand:
					print('Invalid command')
				else:
					playerId = self.table.currentPlayer ^ whoseHand.index(command[1])
					self.table.displayHand(playerId=playerId, isTransparent=False)

			elif command[0] == 'sort':
				self.table.sortHand()
				self.table.displayHand(self.table.currentPlayer, isTransparent=False)
			
			elif command[0] == 'ranks':
				self.giveRanks()

			elif command[0] == 'swap' and len(command) > 1:
				swapUsed = self._swapTurn(command, swapUsed, hasBet)

			elif command[0] == 'bet' and len(command) == 2:
				hasBet = self._betTurn(command, hasBet)

			elif command[0] == 'end':
				if not hasBet:
					print('You need to make a bet before you can end your turn.')
				else:
					turnEnd = True

			else:
				print('Invalid command')

			print()

		return

	def _swapTurn(self, command, swapUsed, hasBet):
		if swapUsed:
			print('You already swapped your cards this turn.')
			return True

		elif not hasBet:
			print("You cannot swap your cards until you have made a bet.")
			return False

		swapSet = set([int(index) - 1 for index in command[1:]])
		self.table.swapCards(swapSet)
		self.table.displayHand(self.table.currentPlayer, isTransparent=False)
		return True

	def _betTurn(self, command, hasBet):
		if hasBet:
			return True
		try:
			betVal = int(command[1])
			if 0 <= betVal <= 9:
				return self.table.addBet(betVal)
		except ValueError:
			pass
			
		print('Invalid hand rank')
		return False




	# Game running
	def run(self):
		self.gameBegin()
		self.initPlayers()
		
		anotherRound = True
		while anotherRound:
			self.table.redraw()
			self.doRound()

			print()
			cont = input('Would you like to play another round? ').strip().lower()
			anotherRound = not cont or cont[0] == 'y'
			print()

		return




