import argparse
from .heuristics import KV
import sys


def is_valid_input(data):
	if len(data[0]) != 1:
		return 'first line of input should be a single number (size)'  # first list[] in data must be size of matrix
	size = data.pop(0)[0]
	if size < 2:  # puzzle too small?
		return 'puzzle too small'
	if len(data) != size:  # data[] should be an array of size N lists[]
		return 'number of rows doesnt match puzzle size'
	for line in data:  # each list[] must be of size N (data must be square matrix)
		if len(line) != size:
			return 'number of columns doesnt match puzzle size'
	expanded = []
	for line in data:
		for x in line:
			expanded.append(x)
	generated = [x for x in range(size ** 2)]
	difference = [x for x in generated if x not in expanded]
	if len(difference) != 0:
		return 'puzzle tiles must be in range from 0 to SIZE**2-1'
	return 'ok'


def get_input():
	parser = argparse.ArgumentParser(description='n-puzzle @ 42 aallali/helamri')
	parser.add_argument('-g', action='store_true', help='greedy search')
	parser.add_argument('-u', action='store_true', help='uniform-cost search')
	parser.add_argument('-f', help='heuristic function', choices=list(KV.keys()), default='conflicts')
	parser.add_argument('-s', help='snail', choices=['zero_first', 'zero_last', 'snail'], default='snail')
	parser.add_argument('-v', action='store_true', help='gui visualizer')
	parser.add_argument('--fast', '-fs', action='store_true', help='fast search', default=False)
	parser.add_argument('file', help='input file', type=argparse.FileType('r'))
	args = parser.parse_args()
	data = args.file.read().splitlines()
	args.file.close()
	data = [line.strip().split('#')[0] for line in data]  # remove comments
	data = [line for line in data if len(line) > 0]  # remove empty lines
	puzzle = []
	try:
		for line in data:
			row = []
			for x in line.split(' '):
				if len(x) > 0:
					if not x.isdigit():
						print('parser: invalid input, must be all numeric')
						sys.exit(0)
					row.append(int(x))
			puzzle.append(row)
		size = puzzle[0][0]
	except:
		print('Invalid Puzzle Input')
		sys.exit(0)

	v = is_valid_input(puzzle)
	if v != 'ok':
		print('parser: invalid input,', v)
		sys.exit(0)
	puzzle1d = []  # convert 2d matrix into list
	for row in puzzle:
		for item in row:
			puzzle1d.append(item)
	return (puzzle1d, size, args)
