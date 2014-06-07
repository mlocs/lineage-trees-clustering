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

# Stage 1: The Vertex Substitution Heuristic
import numpy
import random
import sys


# D - distance matrix
# V - set of verteces
# S - candidate subset for p-median
# P - mapping of verteces to the corresponding median verteces
def calcSumDist(D,V,S):
	sum = 0
	S = map(int,S)
	for v in V: sum += min(D[numpy.ix_([v],S)][0])
	return sum


# D - distance matrix 
# s - old vertex in the subset
# v - candidate vertex for the subset
# The paper by Teitz and Bart (1967) has a mistake, when discirbing the calculation of differneces on the p. 959.
# the difference has to be calculated the other way around
def calcDistDiff(D,S,v,s):
	sum = 0
	N = numpy.size(D,0)
	for i in xrange(N):
		[smallest, secondSmallest] = numpy.sort(D[numpy.ix_([i],S)])[0][0:2]
		if D[i,s] == smallest:
			if D[i,v] <= secondSmallest:
				sum += D[i,v] - D[i,s]
			else:	sum +=  secondSmallest - smallest
	return sum


# D - distance matrix
# p - number of clusters
def VS(D, p):
	#initialize, select initial vertex subset
	improvement = True
	N = numpy.size(D, 0)
	V = range(N)
	S = random.sample(V,p)
	oldSumDist = calcSumDist(D,V,S)
	#while verbesserung moeglich
	while improvement:
		#for each vertex find its assotiated group and computed total weighted distance of the system
		for v in numpy.setdiff1d(V,S):
			#for each vertex not in source subset
			minVert = -1
			minDist = sys.maxint
			for s in S:
				#try to substitute and recalculate the distances
				T = [ i if i != s else v for i in S]
				dist = calcDistDiff(D,S,v,s)
				if dist < minDist:
					minDist = dist
					minVert = s
			#exchange verteces if condition holds
			if minDist < 0:
				S = [ i if i != minVert else v for i in S ]
		#if there an improvement?
		newSumDist = calcSumDist(D,V,S)
		if (newSumDist < oldSumDist):
			improvement = True
		else:
			improvement = False
		oldSumDist = newSumDist
	return (S, oldSumDist)

