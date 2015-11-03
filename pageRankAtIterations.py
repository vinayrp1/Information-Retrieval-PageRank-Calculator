#! /usr/bin/python

import sys
from page_rank import PageRankCalculator

if __name__ == '__main__':

	# The input graph consists of 6 nodes
	if len(sys.argv) > 1:
		fileName = sys.argv[1]
	else:
		fileName = "Graph_SmallSet"
	fh = open("RankAtIterations.txt", 'wb')
	prc = PageRankCalculator(fileName, fh)
	# Calculate Page rank for 100 iterations
	for i in range(1,101):
		prc.calculatePROneIteration()
		# Record PageRank values after 1, 10, 100 iterations
		if i == 1 or i == 10 or i == 100:
			fh.write("Iteration: " + str(i) + "\n")
			print "Iteration No. : ", i
			for key, value in prc.urls.iteritems():
				print "Node: ", key," | Rank: ", value.rank
				fh.write("Node: " + key + " | Rank: " + str(value.rank) + '\n')