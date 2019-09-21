#!/usr/bin/env python3

from itertools import groupby
from operator import itemgetter
import collections
import sys


def read_mapper_output(file, separator='\t'):
	for line in file:
		yield line.rstrip().split(separator, 1)

def main(separator='\t'):
	from collections import OrderedDict
	sortedDictionary = {}
	# input comes from STDIN (standard input)
	data = read_mapper_output(sys.stdin, separator=separator)
	# groupby groups multiple word-count pairs by word,
	# and creates an iterator that returns consecutive keys and their group:
	#   current_word - string containing a word (the key)
	#   group - iterator yielding all ["&lt;current_word&gt;", "&lt;count&gt;"] items
	for current_word, group in groupby(data, itemgetter(0)):
		try:
			total_count = sum(int(count) for current_word, count in group)
			sortedDictionary[current_word] = total_count
			# print(current_word + separator + str(total_count))
		except ValueError:
		# count was not a number, so silently discard this item
			pass
	sortedDictionary = OrderedDict(sorted(sortedDictionary.items(), key=lambda kv: kv[1], reverse=True))
	count = 10
	for key,val in sortedDictionary.items():
		if count >= 1 & count <= 10:
			print (key, val)
			count = count-1

if __name__ == "__main__":
	main()