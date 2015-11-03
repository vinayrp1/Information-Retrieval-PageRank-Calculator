#! /usr/bin/python

import sys
from page_rank import PageRankCalculator
from operator import itemgetter

def printIntoFile(dict, file_handle):

	i = 1
	for key, value in sorted(dict.items(), key=itemgetter(1), reverse=True):
		if i > 50:
			break
		file_handle.write(str(i) + ". " + str(key) + " : " + str(value) + '\n')
		i += 1	

if __name__ == '__main__':

	urlPR = {}							# dictionary holding node as key and
										# page rank as value

	urlInLink = {}						# dictionary holding node as key and
										# inLinks count as value

	if len(sys.argv) > 1:
		fileName = sys.argv[1]
	else:
		fileName = "Graph_LargeSet"

	# create 3 files 	
	fo = open("PerplexityValues.txt", 'wb')
	fo.write("PerplexityValues at different iterations till convergence\n")
	fh = open("Top50_PageRank.txt", 'wb')
	fh.write("Top 50 URLs with high page ranks \n")
	fd = open("Top50_InLinks.txt", 'wb')
	fd.write("Top 50 URLs with high in-links \n")

	# create PageRankCalculator object with input and run the process 
	# till it is converged
	# ----------------------------------------------------------------
	prc = PageRankCalculator(fileName, fh)
	prc.iterateTillConvergence()
	# ----------------------------------------------------------------

	noInLinkC = 0
	noOutLinkC = 0
	reducedPR = 0
	totalURLS = prc.N
	initialPR = 1/float(totalURLS)
	for key, value in prc.urls.iteritems():
		urlPR[key] = value.rank
		urlInLink[key] = len(value.inList)
		if len(value.inList) == 0:
			noInLinkC += 1
		if len(value.outList) == 0:	
			noOutLinkC += 1
		if value.rank < initialPR:
			reducedPR += 1

	print "1. " + str(noInLinkC * 100 / totalURLS) + "% URLs have zero inlinks\n"
	print "2. " + str(noOutLinkC * 100 / totalURLS) + "% URLs have zero outlinks\n"
	print "3. " + str(reducedPR * 100 / totalURLS) + "% URLs have lesser page rank than initial page rank\n"
			
	# put perplexities at each iteration into a file
	i = 1
	for p in prc.perplexity:
		fo.write("Iteration: " + str(i) + " | Perplexity: " + str(p) + '\n')
		i += 1

	# put top 50 urls with high inlinks and page ranks	
	printIntoFile(urlPR, fh)
	printIntoFile(urlInLink, fd)