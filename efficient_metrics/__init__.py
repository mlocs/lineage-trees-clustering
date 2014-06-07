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

## abstract class defining the interface for calculation the distance
from abstract_distance import AbstractDistance

## implementation of contrained TED as described in the paper 
#  K. Zhang, "A constrained edit distance between unordered labeled trees," Algorithmica, vol. 15, 1996, p. 205–222.
from constrained_ted import ConstrainedTED

## generation of random forests with given parameters
from generate_trees import *

## Implements the basic methods for the graph data structure as well as Bellman-Ford 
# algorithm as well as can find Min-Cost-Max-Flow. Used for contrained TED
from Graph import Graph

## Four different Max Similarity Metrices as described in the paper
#A. Torsello, D. Hidović-Rowe, and M. Pelillo, "Polynomial-time metrics for attributed trees.," IEEE transactions on pattern analysis and machine intelligence, vol. 27, 2005, pp. 1087-99.
from max_similarity import MaxSimilarityMetric1, MaxSimilarityMetric2, MaxSimilarityMetric3, MaxSimilarityMetric4

## The calculation of mean or median tree using combinatorical search (with simmulated annealing)
from mean_tree import *

## The part of the implementation of the tree data structure
from Node import Node


## The implementation of the tree data structure. However the magic happens mostly in the Node class.
from Tree import Tree
