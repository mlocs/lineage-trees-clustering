# This file is part of the Lineage Tree Clustering project. 
# Copyright (C) 2014 
# Author: Valeriy Khakhutskyy
# 
# Lineage Tree Clustering is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Lineage Tree Clustering is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with the Lineage Tree Clustering project files.  If not, see <http://www.gnu.org/licenses/>.

import numpy.random as rnd
import random
import numpy
from Node import Node
from Tree import Tree
from abstract_distance import AbstractDistance

import math
from abstract_centroid import AbstractCentroid
import logging

class Centroid(AbstractCentroid):
	
	distanceCalculator = None
	convergenceStop = None
	numOfRestarts = None
	
	##
	# @param convergenceStop how much iterations the result should remain unchanged to be a minimum (Good values e.g. 50-100)
	# @param distanceCalculator
	# @param numOfRestarts default=1 how many restarts should the algorithm perform
	def __init__(self, convergenceStop, distanceCalculator, numOfRestarts=1):
		self.convergenceStop = convergenceStop
		self.numOfRestarts = numOfRestarts
		
		if not isinstance(distanceCalculator, AbstractDistance):
			raise Exception('The instance of distnace calculator is not of a proper AbstractDistance sub-class')
		else: self.distanceCalculator = distanceCalculator
		
		
	def pickOperation(self, tree, alphabet):
		operation = {}
		rndOp = rnd.rand()
		if rndOp < 1.0/3:
			operation['name'] = 'relabel'
		elif rndOp < 2.0/3:
			operation['name'] = 'addChildren'
		elif tree.getSize() == 1:
			operation['name'] = 'addChildren'
		else:
			operation['name'] = 'removeLeaf'
			
		#operation['relabel'] = True if rndOp > 2.0/3 else False
		if operation['name'] == 'relabel':
			#choose node to relabel
			index = rnd.randint(0, high=tree.getSize())
			#print "index:",index
			node = tree.getVertices()[index]
			operation['node'] = node.getHashNum()
			#choose new label
			while True:
				operation['newLabel'] = random.choice(alphabet)
				if operation['newLabel'] != node.getLabel():
					break
		elif operation['name'] == 'addChildren':
			#create children
			for node in rnd.permutation(tree.getVertices()):
				if len(node.getChildren()) < 2:
					operation['node'] = node.getHashNum()
					operation['childLabels'] = [random.choice(alphabet) for i in xrange(2 - len(node.getChildren()))]
					#print "nodu num:", node.getHashNum()
					break
		elif operation['name'] == 'removeLeaf':
			for node in rnd.permutation(tree.getVertices()):
				if node.getChildren() == []:
					operation['node'] = node.getHashNum()
					break
					
		return operation
	
	
	def applyOperation(self, tree, operation):	
		if operation['name'] == 'relabel':
			for node in tree.getVertices():
				if node.getHashNum() == operation['node']:
					node.label = operation['newLabel']
					break
		elif operation['name'] == 'addChildren':
			for node in tree.getVertices():
				if node.getHashNum() == operation['node']:
					for label in operation['childLabels']:
						child = Node(label)
						node.children.append(child)
					break
			tree.initHashNum()
		elif operation['name'] == 'removeLeaf':
			for node in tree.getVertices():
				if operation['node'] in [c.getHashNum() for c in node.getChildren()]:
					for child in node.getChildren():
						if child.getHashNum() == operation['node']:
							node.children.remove(child)
							break
			tree.initHashNum()
		return tree
	
	
	def objFunc(self, tree, trees):
		raise NotImplemented("This method was not implemented")
	
	
	def getCentroidWithSimulatedAnnealing(self, trees, alphabet, initial = None):
		if initial == None:
			meanTree = Tree().load("0")
		else:
			meanTree = initial
		fOld = self.objFunc(meanTree, trees)
		convCounter = 0
		t = 1 # temperature schedule
		#while converges:
		while True:
			convCounter += 1
			newTree = meanTree.copy()
			#pick some operation
			rndOp = self.pickOperation(newTree, alphabet)
			#apply operation
			newTree = self.applyOperation(newTree, rndOp)
			#should you take this tree?
			fNew = self.objFunc(newTree, trees)
			if fNew < fOld:
				del meanTree
				meanTree = newTree
				fOld = fNew
				convCounter = 0
			elif rnd.random() < math.exp(- (fNew - fOld) / t):
				del meanTree
				meanTree = newTree
				fOld = fNew
				convCounter = 0
				
			t += 1
			if convCounter > self.convergenceStop:
				break
		return (meanTree, fOld)
	
	
	def getCentroid(self, trees, alphabet, initial = None):
		logging.debug( "**********Getting centroid******" )
		logging.debug( "initial centroid:",initial )
		(centroid, val) = self.__findCentroid(trees, alphabet, initial)
		
		for restarts in xrange(self.numOfRestarts-1):
			(c,v) = self.__findCentroid(trees, alphabet, initial)
			if v < val:
				centroid = c
				val = v
		return (centroid, val)
	
	
	def __findCentroid(self, trees, alphabet, initial = None):
		if initial == None:
			meanTree = Tree().generateRandomTree(alphabet, 2, numpy.ones([len(alphabet), len(alphabet)+1])/(len(alphabet)+1))
		else: meanTree = initial
		if len(trees) == 0:
			return (meanTree, 0)
		fOld = self.objFunc(meanTree, trees)
		convCounter = 0
		#while converges:
		while True:
			convCounter += 1
			newTree = meanTree.copy()
			#pick some operation
			rndOp = self.pickOperation(newTree, alphabet)
			#apply operation
			newTree = self.applyOperation(newTree, rndOp)
			#should you take this tree?
			fNew = self.objFunc(newTree, trees)
			#print "current:",fNew
			if fNew < fOld:
				del meanTree
				meanTree = newTree
				fOld = fNew
				convCounter = 0
			
			if convCounter > self.convergenceStop:
				break
		return (meanTree, fOld)
	



class MeanTree(Centroid):
	def objFunc(self, tree, trees):
		size = len(trees)
		sum = 0
		for t in trees:
			sum += self.distanceCalculator.calculateDistance(tree, t)**2
		#return sum/size
		return sum
	
	
	

class MedianTree(Centroid):
	def objFunc(self, tree, trees):
		size = len(trees)
		sum = 0
		for t in trees:
			sum += self.distanceCalculator.calculateDistance(tree, t)
		#return sum/size
		return sum
	
	
	
	
AbstractCentroid.register(MeanTree)
AbstractCentroid.register(MedianTree)



## Some test code
if __name__== '__main__':
	import pydot
	from constrained_ted import ConstrainedTED
	from max_similarity import MaxSimilarityMetric1, MaxSimilarityMetric2, MaxSimilarityMetric3, MaxSimilarityMetric4
	filename = "data/trees_type1.input"
	alphabet = [0, 1]
#	trees = []
#	f = open(filename, "rt")
##	graph = pydot.Dot()
#
#	for line in f.xreadlines():
#		trees.append( Tree().load(line.strip()) )
##		tree_graph = trees[-1].createGraph()
##		graph.add_subgraph(tree_graph)
#	f.close()
	trees = Tree.loadFromFile(filename)
#	print graph.to_string()
	# to save the good png: ccomps -x all_graph.dot | dot | gvpack -g | neato -s -n2 -Tpng > all_graph.png
	#graph.write_png("all_trees.png")
	
#	for tree in trees:
#		print func(tree, trees)

	distanceCalculator = ConstrainedTED()
	#distanceCalculator = MaxSimilarityMetric4()
	
	
	(meanTree, fVal) = MedianTree(50, distanceCalculator,5).getCentroid(trees, alphabet)
	subgraph = meanTree.createGraph()
	graph = pydot.Dot()
	graph.add_subgraph(subgraph)
	graph.write_png('mean_tree.png')
	
