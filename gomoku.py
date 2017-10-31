import numpy as np

from min_max import minmax
from heuristic import winner, calculH

class Stade(object):
	def __init__(self, mapping, player):
		self.mapping = mapping
		self.player = player

	@property
	def heuristic_value(self):
		self._heuristic_value = calculH(self.mapping, self.player)
		return self._heuristic_value

	@property
	def available_moves(self):
	#	print("---------------------------")
		height = 19
		width = 19
		proxim_mapping = self.mapping.copy()
		radius = 3
		proxim_matrix = np.ones((radius, radius))*3
#		print("proxim_matrix", proxim_matrix)
		tmp = np.count_nonzero(proxim_mapping)
		if (tmp > 1):
			for row in range(height - radius + 1):
				for col in range(width - radius + 1):
					if np.any(self.mapping[row:row + radius, col:col + radius]):
						proxim_mapping[row:row + radius, col:col + radius] += proxim_matrix
		elif tmp == 1 and self.mapping[int(height/2), int(width/2)] == 0:
			proxim_mapping[int(height/2), int(width/2)] = 3		
		elif tmp == 1 and self.mapping[int(height/2), int(width/2)] != 0:
			proxim_mapping[int(height/2) - 1, int(width/2) - 1]  = 3		
		elif tmp == 0:
			proxim_mapping[int(height/2), int(width/2)] = 3		
#		print("proxim_mapping", proxim_mapping)
		
		self._available_moves = []
		diff_to_centerH = abs(np.arange(height) - int(height/2))
		center_to_borderH = np.argsort(diff_to_centerH)
	#	print (center_to_borderH)
		diff_to_centerW = abs(np.arange(width) - int(width/2))
		center_to_borderW = np.argsort(diff_to_centerW)
	#	print (center_to_borderW)
		for row in center_to_borderH:
			for col in center_to_borderW:
				if (proxim_mapping[row][col] % 3 == 0 and proxim_mapping[row][col] > 0):
					move = [row, col]
					self._available_moves.append(move)
#		print(self._available_moves)
		return self._available_moves
		
	def next_state(self, move):
		next_mapping = np.copy(self.mapping)
	#	print("moveee", move)
		next_mapping[move[0]][move[1]] = self.player
		next_player = -1*self.player
		return Stade(next_mapping, next_player)

	def is_terminal(self):
		if not (0 in self.mapping):
			return True
		if winner(self.mapping, self.player):
	#		print('laaaaaaaa')
			return True
		else:
			return False		


class Gomoku:
	def __init__(self):
		init_map = np.zeros((19,19))
		player = 1
		self.current = Stade(init_map, 1)
		nb_player = int(input("combien de joueur humain 0-1-2 ? "))
		self.win = False

		if nb_player == 0:
			self.player_1 = False 
		if nb_player == 2:
			self.player_2 = True
		if nb_player == 1 or nb_player == 2:
			self.player_1 = True
		if nb_player == 0 or nb_player == 1:
			self.player_2 = False

	def printing(self):
		for x in self.current.mapping:
			for y in x:
				if y == 0: print(".", end="")
				elif y == 1: print("\033[31mX\033[0m", end = "")
				elif y == -1: print("\033[34mO\033[0m", end = "")
			print("\n", end = "")
		print("\n", end = "")
				

	def loop_game(self):
		while self.win == False:
			if self.player_1 == True:
				move = input("choose coordonate ex: 4-6: ")
				move = move.split("-")
				move[0] = int(move[0])
				move[1] = int(move[1])
				self.current.mapping[move[0]][move[1]] = self.current.player

			if self.player_1 == False:
				move = minmax(self.current)
				#print("move:", move)
				self.current.mapping[move[0]][move[1]] = self.current.player

			self.printing()
			self.win = self.current.is_terminal()
			if self.win == True:
				print("\033[31mWINNER PLAYER 1\033[0m")
				break
			self.current.player = -1*self.current.player

			if self.player_2 == True:
				move = input("choose coordonate ex: 4-6: ")
				move = move.split("-")
				move[0] = int(move[0])
				move[1] = int(move[1])
				self.current.mapping[move[0]][move[1]] = self.current.player

			if self.player_2 == False:
				move = minmax(self.current)
				#print("move:", move)
				self.current.mapping[move[0]][move[1]] = self.current.player
			
			self.printing()
			self.win = self.current.is_terminal()
			if self.win == True:
				print("\033[31mWINNER PLAYER 2\033[0m")
				break
			self.current.player = -1*self.current.player
		
	
if __name__ == '__main__':
	partie = Gomoku()
	partie.loop_game()

