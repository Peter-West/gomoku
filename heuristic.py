import numpy as np
import regex as re


UTILITY = {'Q': [20000000, ['xxxxx']],
           'Q2': [400000, ['exxxxe']],
           'Q1': [50000, ['nxxxxe', 'exxxxn']],
           'T2': [30000, ['exxxe']],
           'T1': [15000, ['nxxxee', 'eexxxn']],
           'PQ2': [7000, ['exexxe', 'exxexe']],
           'PQ1': [3000, ['nxexxe','nxxexe', 'exxexn', 'exexxn']],
           'D2': [500, ['eexxe', 'exxee']],
           'D1': [400, ['nxxeee', 'eeexxn']],
           'PT2': [100, ['exexe']],
           'PT1': [40, ['nxexee', 'eexexn']]}

FINISHED = {'Q': [200000, ['xxxxx']]}

HEURISTIC = [[0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0.2, 0.4, 0.6, 0.8, 0.8, 0.8, 0.6, 0.4, 0.2, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0.2, 0.4, 0.6, 0.8, 1.0, 0.8, 0.6, 0.4, 0.2, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0.2, 0.4, 0.6, 0.8, 0.8, 0.8, 0.6, 0.4, 0.2, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0, 0, 0]]

def winner(mapping, player, forwin='xxxxx'):
	map2 = mapping.copy()
	count = 0
	count += search(makeDig(map2, player), forwin)
	count += search(makeCol(map2, player), forwin)
	count += search(makeLin(map2, player), forwin)
	if count > 0:
		return True
	else:
		return False


def calculH(mapping,player, val_H = UTILITY, pos_val_H = HEURISTIC):
	seq_H = 0
	pos_H = 0
	map2 = mapping.copy()
	for values in val_H.keys():
		val_seq = val_H[values][0]
		count = 0
		sequence = val_H[values][1]
		for seq in sequence:
			count += search(makeDig(map2, player), seq)
			count += search(makeCol(map2, player), seq)
			count += search(makeLin(map2, player), seq)
		seq_H += count* val_seq
#	print(seq_H)
	map2 = mapping.copy()
	if(player == 1):
		np.place(map2, map2 == -1, 0)
		pos_H = np.sum(np.multiply(map2, pos_val_H))
	else:
		np.place(map2, map2 == 1, 0)
		pos_H = -np.sum(np.multiply(map2, pos_val_H))
#	print("pos_h: ", pos_H)
	heuristic_val = pos_H + seq_H
#	print(heuristic_val)
	total = heuristic_val


	player = -1*player
	seq_H = 0
	pos_H = 0
	map2 = mapping.copy()
	for values in val_H.keys():
		val_seq = val_H[values][0]
		count = 0
		sequence = val_H[values][1]
		for seq in sequence:
			count += search(makeDig(map2, player), seq)
			count += search(makeCol(map2, player), seq)
			count += search(makeLin(map2, player), seq)
		seq_H += count * val_seq
#	print(seq_H)
	map2 = mapping.copy()
	if(player == 1):
		np.place(map2, map2 == -1, 0)
		pos_H = np.sum(np.multiply(map2, pos_val_H))
	else:
#		print("ok")
		np.place(map2, map2 == 1, 0)
		pos_H = -np.sum(np.multiply(map2, pos_val_H))
#	print("pos_h: ", pos_H)
	heuristic_val = pos_H + seq_H
#	print(heuristic_val)
	return total - 1.05 * heuristic_val


def makeDig(mapping, player):
	dig = [mapping[::-1, :].diagonal(i) for i in range(-mapping.shape[1] + 5, mapping.shape[1] - 4)]
	diagonal = []
	for i in dig:
		str1 = ''
		for e in i:
			if player == 1:
				if e == 0:
					str1 += 'e'
				elif (e == -1 or e == 2):
					str1 += 'n'
				elif(e == 1):
					str1 += 'x'
			else:
				if e == 0:
					str1 += 'e'
				elif (e == 1 or e == 2):
					str1 += 'n'
				elif(e == -1):
					str1 += 'x'
		diagonal.append(str1)
	dig = [mapping.diagonal(i) for i in range(mapping.shape[1]-5, -mapping.shape[1] + 4, -1)]
	for i in dig:
		str1 = ''
		for e in i:
			if player == 1:
				if e == 0:
					str1 += 'e'
				elif (e == -1 or e == 2):
					str1 += 'n'
				elif(e == 1):
					str1 += 'x'
			else:
				if e == 0:
					str1 += 'e'
				elif (e == 1 or e == 2):
					str1 += 'n'
				elif(e == -1):
					str1 += 'x'
		diagonal.append(str1)
	return diagonal


def makeLin(mapping, player):
	line = []
	for i in mapping:
		str1 = ''
		for e in i:
			if player == 1:
				if e == 0:
					str1 += 'e'
				elif (e == -1 or e == 2):
					str1 += 'n'
				elif(e == 1):
					str1 += 'x'
			else:
				if e == 0:
					str1 += 'e'
				elif (e == 1 or e == 2):
					str1 += 'n'
				elif(e == -1):
					str1 += 'x'
		line.append(str1)
	return line


def makeCol(mapping, player):
	col = []
	matrix = mapping.copy().T
	for i in matrix:
		str1 = ''
		for e in i:
			if player == 1:
				if e == 0:
					str1 += 'e'
				elif (e == -1 or e == 2):
					str1 += 'n'
				elif(e == 1):
					str1 += 'x'
			else:
				if e == 0:
					str1 += 'e'
				elif (e == 1 or e == 2):
					str1 += 'n'
				elif(e == -1):
					str1 += 'x'
		col.append(str1)
	return col


def search(forcheck, pattern):
	count = 0
	for check in forcheck:
		count += counteur(check, pattern)
	return count


def counteur(check, pattern):
#	print("counteur: ", check)
#	print("pattern: ", pattern)
	return len(re.findall(pattern, check, overlapped=True))
