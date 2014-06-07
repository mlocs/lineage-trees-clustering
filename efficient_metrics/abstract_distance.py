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

from abc import ABCMeta, abstractmethod

## An abstract class defines the common interface for different methods of
# distance/similarity metric calculation
class AbstractDistance(object):
	
	__metaclass__ = ABCMeta
	
	## Calculates the distance between two trees
	# @param Tree1 Tree the first tree
	# @param Tree2 Tree the second tree
	# @return numerical value for distance or dissimilarity metric 
	@abstractmethod
	def calculateDistance(self, Tree1, Tree2):
		raise NotImplemented("This method was not implemented")
