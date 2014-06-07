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

import numpy
from pymunkres import Munkres
from abstract_distance import AbstractDistance
from collections import defaultdict

class MaxSimilarityMetric(AbstractDistance):

	similarityHash = None
	munkres =  Munkres()

	def getTreeSize(self, T):
		return None
	
	def sigma(self, u,v):
		if u.getLabel() != v.getLabel(): return 0
		else: return 1
	#	return 1
	
	def AnchoredSimilarity(self, u, w, tHN1, tHN2):
		val = 0
		C_u = u.getChildren()
		C_w = w.getChildren()
		
		if len(C_u)>0 and len(C_w)>0:
			
			hash_u = [node.getHashNum() for node in C_u]
			hash_u.sort()
			hash_u_str = tHN1 + str(hash_u)
			
			hash_w = [node.getHashNum() for node in C_w]
			hash_w.sort()
			hash_w_str = tHN2 + str(hash_w)
			
			if self.similarityHash.has_key((hash_u_str, hash_w_str)):
				val = self.similarityHash[(hash_u_str, hash_w_str)]
			elif self.similarityHash.has_key((hash_w_str, hash_u_str)):
				val = self.similarityHash[(hash_w_str, hash_u_str)]
				
			else:
				weights = numpy.zeros([len(C_u), len(C_w)],'d')
				for i in xrange(len(C_u)):
					for j in xrange(len(C_w)):
						weights[i,j] = self.AnchoredSimilarity(C_u[i], C_w[j], tHN1, tHN2)
				val = Munkres().maxWeightMatching(weights)
				self.similarityHash[(hash_u_str, hash_w_str)] = val
				
				
		return self.sigma(u,w) + val
				
	
	
	def getMaxSimilarity(self, T1,T2):
		maxsim = 0
		self.similarityHash = defaultdict(int)
		for u in T1.getVertices():
			if len(u.getChildren())>0:
				sim = self.AnchoredSimilarity( u, T2.getRoot(), T1.getTreeHashNum(), T2.getTreeHashNum())
				if sim > maxsim:
					maxsim = sim
		for w in T2.getVertices():
			if len(w.getChildren())>0:
				sim = self.AnchoredSimilarity( T1.getRoot(), w, T1.getTreeHashNum(), T2.getTreeHashNum())
				if sim > maxsim:
					maxsim = sim
		del self.similarityHash
		return maxsim
		
	
class MaxSimilarityMetric1(MaxSimilarityMetric):
	def calculateDistance(self, Tree1, Tree2):
		W = self.getMaxSimilarity(Tree1, Tree2)
		return max(Tree1.getSize(),Tree2.getSize()) - W

class MaxSimilarityMetric2(MaxSimilarityMetric):
	def calculateDistance(self, Tree1, Tree2):
		W = self.getMaxSimilarity(Tree1, Tree2)
		return Tree1.getSize() + Tree2.getSize() - 2*W
	
class MaxSimilarityMetric3(MaxSimilarityMetric):
	def calculateDistance(self, Tree1, Tree2):
		W = self.getMaxSimilarity(Tree1, Tree2)
		return 1 - W/max(Tree1.getSize(),Tree2.getSize())
	
class MaxSimilarityMetric4(MaxSimilarityMetric):
	def calculateDistance(self, Tree1, Tree2):
		W = self.getMaxSimilarity(Tree1, Tree2)
		return 1 - W/(Tree1.getSize() + Tree2.getSize() - W)
	
	
AbstractDistance.register(MaxSimilarityMetric1)
AbstractDistance.register(MaxSimilarityMetric2)
AbstractDistance.register(MaxSimilarityMetric3)
AbstractDistance.register(MaxSimilarityMetric4)
