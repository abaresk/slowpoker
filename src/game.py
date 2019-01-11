
import getpass

from src.table import Table

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


			self.table.addPlayer(name, pw1)

			print("You're all set, " + name + '!')
			print()
		return

	# Game commands
	def giveOptions(self):
		print("'view {mine theirs}'\tlets you view your hand or your opponent's.")
		print("'view' \t\t\tlets you view the entire table")
		print("'sort' \t\t\tlets you sort your hand")
		print("'bet' \t\t\tlets you place a bet")
		print("'swap <card numbers>' \tlets you swap out the cards you listed in <card numbers>")
		print("'end' \t\t\tends your turn")
		print()
		return


	# Gameplay
	def doRound(self):
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
		self.table.printWinner()
		return

	def doTurn(self):
		turnEnd = False
		swapUsed = False

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

			elif command[0] == 'swap' and len(command) > 1:
				if swapUsed:
					print('You already swapped your cards this turn.')
				else:
					swapSet = set([int(index) - 1 for index in command[1:]])
					self.table.swapCards(swapSet)
					self.table.displayHand(self.table.currentPlayer, isTransparent=False)
					swapUsed = True

			elif command[0] == 'end':
				turnEnd = True

			else:
				print('Invalid command')

			print()

		return


	def showResults(self):

		return

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




