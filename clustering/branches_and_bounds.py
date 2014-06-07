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
from VSH import *
from lagrangian_relaxation import *
# Determine whether the partial solution \gamma can lead to a sum of stars value that is better(smaller) than the incumbent value Z_star
#
# Langrangian relaxation subroutine with few minor modifications.
# additional constraints to LR2:
# y_w = 1, for w = \gamma_j and 1<=j<=r - r vertices of \gamma are selected in the p-median solution
# \sum_{w+1}^N y_w = p - r, where w = \gamma_r + 1 - the remaining p-r vertices will be selected from vertices \gamma_r + 1, \gamma_r + 2,...,N
def isPartialSolution(D, gamma, p): 
	N = numpy.size(D,0)
	V = numpy.arange(N) #all vertices
	#retrieve selected vertices
	S = [ int(i) for i in gamma if i != -1] #selected vertices
	
	#repeat until p vertices are obtained
	while len(S) != p:
		#for each unselected vertex the distance between that vertex and each of the selected vertices is obtained and the minimum of these distances is stored
		U = numpy.setdiff1d(V,S)
		#the unselected vertex with the maximum of these minimum distances is then selected and added to the set of selected vertices
		m = numpy.argmax(numpy.min(D[numpy.ix_(U,S)], axis=1))
		S.append(U[m])
	
	#the sum of stars for this complete set of p vertices servers as Z_H for Lagrangian relaxation algorithm
	Z_H = calcSumDist(D,V,S)
	return LR2(D,p,Z_H)

def BnB(D,gamma_star,p):
	#initialize 
	N = numpy.size(D,0)
	V = range(N)
	Z_star = calcSumDist(D,V,gamma_star)
	r = -1 # so that in the first iteration it becomes 0
	gamma = numpy.ones(p)*(-1)
	
	
	flag = True
	while(True):
		#branch forward
		if flag:
			r += 1
			gamma[r] = 1 if r == 0 else gamma[r-1] + 1
		#feasibile comletion test
		if (N-1) - gamma[r] >= p - (r+1): #goto DISPENSATION
			#partial solution evaluation (???)
			if isPartialSolution(D,gamma,p):
				#complete solution
				if r != p-1:
					flag = True
					continue
				else:
					gamma_star = numpy.copy(gamma)
					Z_star = calcSumDist(D,V,gamma_star)
		while gamma[r] >= N: 
			gamma[r] = 0
			r -= 1
			if r< 0:
				#terminate as all N!/(p!(N-p)!) feasible solutions have been either implicitly or explicitly evaluated 
				return (gamma_star, Z_star)
		gamma[r] += 1
		flag = False

