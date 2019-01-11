

from src.table import Table 

class Player():
	def __init__(self, name=None, pw=None):
		self.name = name
		self._pw = pw
		return

class Game():
	def __init__(self):
		self.table = Table(2)
		return

	def addPlayer(self, name, pw):
		assert(len(self.table.players) < 2)

		playerId = len(self.table.players)
		self.table.players[playerId] = Player(name, pw)
		return

	def 
