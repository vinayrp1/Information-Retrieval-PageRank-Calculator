#! /usr/bin/python

import sys
import math 

class MetaData:
	'This class contains the number of outgoing links from a node, \\\
	list of incoming links and rank of the node'

	def __init__(self, ol, il, r):

		self.outList = ol               # list of outgoing links
		self.inList = il 				# list of incoming links
		self.rank = r    				# rank of the url/node

	def addToOutList(self, n):

		if n not in self.outList:      # check for duplicates
			self.outList.append(n)

	def setIncomingLinks(self, l):

		self.inList = l

class PageRankCalculator:
	'This class calculates and organises urls based on their        \\\
	page rank'

	def __init__(self, fileName, fd):

		self.inputFile = fileName       # input file
		
		self.urls = {}                  # dictionary containing 
										# node as key and 
										# MetaData as the value

		self.sinkNodes = []				# Node with no outgoing links

		self.perplexity = []		 	# list consisting of perplexity
										# values at each iteration
		self.organiseURLs()				
		self.assignDefaultPRtoNodes()

	def organiseURLs(self):

		fh = open(self.inputFile,'r')		
		lines = fh.readlines()
		for line in lines:
			# split the lines to get the nodes
			line = line.rstrip('\n')
			node_list = line.split(' ')
			LinkedNode = node_list[0]
			# Removing an extra unwanted empty character from the 
			# incoming list
			nodes = []
			for n in node_list[1:]:
				if n != "" and n not in nodes:
					nodes.append(n)

			# LinkedNode = nodes[0]
			# if source node is already present in the dicionary,
			# set the incoming_node_list in its MetaData, else create a 
			# MetaData object and populate it with incoming node
			# list	
			if not self.urls.has_key(LinkedNode):
				self.urls[LinkedNode] = MetaData([], nodes, 0)
			else:
				self.urls[LinkedNode].setIncomingLinks(nodes)
			# check the nodes in the incoming node list and update
			# the number of outgoing links in its 
			# corresponding hash value	
			for node in nodes:
				if not self.urls.has_key(node):
					self.urls[node] = MetaData([], [], 0)
				self.urls[node].addToOutList(LinkedNode)

		for key, value in self.urls.iteritems():
			if len(value.outList) == 0:
				self.sinkNodes.append(key)
	
	def assignDefaultPRtoNodes(self):

		self.N = len(self.urls)
		for key, value in self.urls.iteritems():
			value.rank = 1.0 / (self.N)

	def iterateTillConvergence(self):

		i = 0
		while(1):

			self.calculatePROneIteration()
			print "Iteration: ", i		
			entropy = 0
			for key, value in self.urls.iteritems():
				rank = value.rank
				entropy -= (rank) * (math.log(rank, 2))
			px = 2**entropy
			self.perplexity.append(px)
			print "Perplexity:", px, "\n"
			if len(self.perplexity) > 3:
				if int(self.perplexity[i]) == int(self.perplexity[i - 1]) == int(self.perplexity[i - 2]) == int(self.perplexity[i - 3]):
					print "Convergence achieved\n"
					break
			i += 1
			
	def calculatePROneIteration(self):

		newPR = {}
		d = 0.85
		sinkPR = 0
		for n in self.sinkNodes:
			sinkPR += self.urls[n].rank
		for key, value in self.urls.iteritems():
			newPR[key] = (1 - d) / (self.N)
			newPR[key] += (d * sinkPR) / (self.N)
			for inode in value.inList:
				newPR[key] += (d * self.urls[inode].rank) / (len(self.urls[inode].outList))
		for key, value in newPR.iteritems():
			self.urls[key].rank = value