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

from Node import Node
import numpy.random as rnd
from time import time
from traceback import print_stack
import logging

class Tree:
	root = None
	emptyTree = None
	treeHashNum = None
	
	def copy(self):
		newTree = Tree()
		newTree.root = self.root.copy()
		return newTree
		
		
	def getTreeHashNum(self):
		if self.treeHashNum == None:
			self.treeHashNum = str(time()) + "." + str(rnd.random())
		return self.treeHashNum
	
	
	def getHashNum(self):
		if not self.root == None: return  self.root.getHashNum()
		else: return 0
	
	@classmethod
	def getEmptyTree(cls):
		return Tree()
	
	
	def __init__(self):
		self.root = None

	
	@classmethod
	def loadFromFile(cls, filename):
		trees = []
		f = open(filename, "r")
		for line in f.xreadlines():
			if not line.strip()[0] == '#': #ignore comments where line begins with '#'
				tree = Tree().load(line.strip())
				trees.append(tree)
		return trees
	
	
	def initHashNum(self):
		self.root.initHashNum()
		
		
	def load(self, string):
		self.root = Node(string[0])
		self.root.loadChildren(string[2:-1])
		self.root.initHashNum()
		return self
	
	
	def getSize(self):
		if not self.root == None:
			return self.root.getSize()
		else:
			return 0
	
	
	def getVertices(self):
		if not self.root == None:
			return self.root.getVertices()
		else: return []
	
	
	def getRoot(self):
		return self.root
	
	
	def toString(self):
		return self.root.toString()
	

	def generateRandomTree(self, alphabet, deg, pvals):
		rootIdx = rnd.random_integers(0, len(alphabet)-1, 1)
		self.root = Node(alphabet[int(rootIdx)]).generateRandom(alphabet, deg, pvals)
		self.root.initHashNum()
		return self
	
	
	def getStatistics(self):
		return self.root.getStatistics()
	
	
	def createGraph(self, name=""):
		import pydot
		if name != "":
			graph = pydot.Subgraph(name, graph_type="digraph", strict=True, label=name)
		else:
			graph = pydot.Subgraph(graph_type="digraph", strict=True)
		rootNode = pydot.Node(str(time()) + str(rnd.random()), label = str(self.root.getLabel()))
		graph.add_node(rootNode)
		self.root.visualize(rootNode, graph)
		return graph
