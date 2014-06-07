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
from exceptions import Exception
from traceback import *
import logging

class Medoid(object):
	
	distanceCalculator = None
	
	
	def __init__(self, distanceCalculator):
		self.distanceCalculator = distanceCalculator
		
	
	def getMedoid(self, trees):
		size = len(trees)
		D = np.zeros([size,size])
		for i in xrange(size):
			for j in xrange(1,size):
				D[i,j] = D[j,i] = self.distanceCalculator.calculateDistance(trees[i],trees[j])
		minIndex = np.argmin(np.sum(D, axis=0))
		return (trees[minIndex], np.sum(D, axis=0)[minIndex])
	
	
	def getCentroid(self,trees, alphabet=None, initial=None):
		return self.getMedoid(trees)
	
