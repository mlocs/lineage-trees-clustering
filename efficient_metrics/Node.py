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

import numpy as np
import numpy.random as rnd
from time import time
from types import *

def compare(a, b):
	return -cmp(a.hashNum, b.hashNum)

class Node:
	label = None
	children = None
	hashNum = None
	statistics = None
	MAX_RECURSION = 100
	
	def copy(self):
		newNode = Node(self.label)
		newNode.hashNum = self.hashNum
		for child in self.getChildren():
			newNode.addChild(child.copy())
		return newNode
	
	
	def __getEmtpyStatistics(self):
		statistics = {'leaves':{}, 'childs':{}}
		return statistics
	
	
	
	def __init__(self, label):
		self.label = str(label)
		self.children = []
		self.statistics = self.__getEmtpyStatistics()
		
		
	def addChild(self, node):
		self.children.append(node)
		return node
		
		
	def getChildren(self):
		#if self.children == None: return []
		# does it make any difference???
		#return sorted(self.children,compare)
		return self.children
		
		
	def getLabel(self):
		return self.label
	
	
	def getVertices(self):
		vertices = [self]
		
		for c in self.children:
			vertices += c.getVertices()
		
		return sorted(vertices, compare)
	
	
	def getSize(self):
		size = 1
		for c in self.children:
			size += c.getSize()
			
		return size
	
	
	def loadChildren(self, string):
		lastChild = None
		i=0
#		for j in xrange(len(string)):
		while(len(string)>0):
			if string[i] == "(":
				string = lastChild.loadChildren(string[1:])
			elif string[i] == ")":
				return string
			else:
				lastChild = self.addChild(Node(string[i]))
			string = string[1:]
		return string
	
	## new version
	def generateRandom(self, alphabet, deg, pvals, rec_counter=0):
		if rec_counter > self.MAX_RECURSION:
			return self
		if rnd.rand() > pvals[int(self.label)-1, 0]:
			results = rnd.multinomial(deg, pvals[int(self.label)-1, 1: ]/sum(pvals[int(self.label)-1, 1: ]))
			childLabelIdx = np.nonzero(results)[0]
			for idx in childLabelIdx:
				node = Node(alphabet[int(idx)])
				self.addChild(node.generateRandom(alphabet, deg, pvals, rec_counter+1))
		return self


	def toString(self):
		string = str(self.label)
		if len(self.children) > 0:
			string += "(" 
			for c in self.children:
				string += c.toString()
			string += ")"
		return string
	
	
	def visualize(self, node, graph):
		import pydot
		for c in self.children:
			childNode = pydot.Node(str(time())+ str(rnd.random()), label = str(c.getLabel()))
			graph.add_node(childNode)
			graph.add_edge(pydot.Edge(node, childNode))
			c.visualize(childNode, graph)
	
	
	def initHashNum(self, i=0):
		self.hashNum = i+1
		if not self.children == None:
			for c in self.children:
				i += 1
				i = c.initHashNum(i)
		return i
	
	
	def getStatistics(self):
		self.statistics = self.__getEmtpyStatistics()
		statistics = self.__getEmtpyStatistics()
		
		if len(self.children) == 0:
			if not (self.getLabel() in self.statistics['leaves'].keys()):
				self.statistics['leaves'][self.getLabel()] = 0
			self.statistics['leaves'][self.getLabel()] += 1
		
		for child in self.children:
			stat = child.getStatistics()
			statistics = self.sumDicts(statistics, stat)
			
			transition = self.getLabel()+child.getLabel()
			if not (transition in self.statistics['childs'].keys()):
				self.statistics['childs'][transition] = 0
			self.statistics['childs'][transition] += 1
		
		self.statistics = self.sumDicts(self.statistics, statistics)
			
		return self.statistics
	
	
	def sumDicts(self, dict1, dict2):
		for key in dict1.keys():
			if type(dict1[key]) == DictType:
				dict1[key] = self.sumDicts(dict1[key], dict2[key])
			else:
				if dict2.has_key(key):
					dict1[key] += dict2[key]
				
					
		for key in dict2.keys():
			if not dict1.has_key(key):
				dict1[key] = dict2[key]
				
		return dict1
	

	def getHashNum(self):
		return self.hashNum
