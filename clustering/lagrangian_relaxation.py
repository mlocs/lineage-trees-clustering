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
import math

#calculate the value of Z_2(\lambda)
def Z_2(D,x,l):
	N = numpy.size(D,0)
	Z2 = sum(l)
	for i in xrange(N):
		for j in xrange(N):
			Z2 += (D[i,j] - l[i]) * x[i,j]
	 #+ numpy.sum(numpy.sum(numpy.multiply(D - l,x), axis=1) , axis=0)
	return Z2
	
	
# for given \lambda_i's obtain x_{ij}'s
def subroutine(D, l, p):
	N = numpy.size(D,0)
	y = numpy.zeros(N)
	x = numpy.zeros([N,N])
	# select p vertices y_j for which \sum_{i=1}^N \min(d_{ij} - \lambda_i,0) is the smallest.
	indeces = numpy.argsort(numpy.sum(numpy.minimum(D- numpy.mat(l).T,0), axis = 0)).tolist()[0][0:p]
	#print indeces
	y[indeces] = 1
	
	# obtain x_{ij} variables as x_{ij} = 1 if y_j == 1 and d_{ij} - \lambda_i < 0 else 0
	for i in xrange(N):
		for j in xrange(N):
			if (y[j] == 1 and D[i,j] - l[i] < 0):
				x[i,j] = 1
	return x
	
	
# find \lambda_i's which maximizes Z_2(\lambda)
# use subgradient method as defined in paper by Brusco and Koehn in paper "OPTIMAL PARTITIONING OF A DATA SET BASED ON THE p-MEDIAN MODEL"
def LR2(D, p, Z_H):
	restarting_times = 5
	qmax = 4000
	epsilon2 = (10**(-5))**2
	N = numpy.size(D,0)
	l = numpy.ones(N)*100000
	Z2_old = 0
	# repeat 5 times, restarting \tau^0 = 2
	for restarting_step in xrange(restarting_times):
		tau = 2.0
		
		iterations_without_increase = 0
		# repeat qmax = 4000
		for iteration_step in xrange(qmax):
			# calculate new x_{ij}'s
			x = subroutine(D,l, p)
			#return
			Z2 = Z_2(D,x,l)
			
			if Z2_old >= Z2: iterations_without_increase += 1
			else: 
				iterations_without_increase = 0
				Z2_old = Z2
				#print "Z2_old",Z2_old
		
			# if Z_2(\lambda^{qmax}) = Z_H (within some tolerance, \epsilon), then the solution from VS heuristicshas been confirmed to be globally optimal
			if (Z2_old - Z_H)**2 < epsilon2:
				return True
			
			#\tau^0 = 2, \tau^{q+1} = \tau^q unless 200 iteration without increase of Z_2(\lambda^q), otherwise \tau^{q+1} = \tau^q/2
			if iterations_without_increase > 200:
				tau = tau/2
				iterations_without_increase = 0
			# "Z2",Z2
			# step size t^q = \tau^q (Z_H - Z_2(\lambda^q))/\sum_{i=1}^N (1-\sum_{j=1}^N x_{ij}^q)^2
			t = tau * (Z_H - Z2) / sum((1-numpy.sum(x,axis=1))**2)
			if math.isnan(t) or math.isinf(t):
				return False
				
				
			# updating formula: \lambda_i^{q+1} = \labda_i^{q} + t^{q} (1-\sum_{j=1}^N x_{ij}^q) for 1<=i<=N
			#for i in xrange(N):
			l += t * (1-numpy.sum(x,axis=1))
			
			
			
	return False
