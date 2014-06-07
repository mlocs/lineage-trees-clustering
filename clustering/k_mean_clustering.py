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

from Tree import Tree
import numpy

## k-mean framework for clustering
def clusterForest(k, trees, alphabet, centroidCalculator, distanceCalculator):
	
	sValOld = 0
	# first generate k random centroids:
	centroids = []
	vals = numpy.zeros(k)
	for i in xrange(k):
		centroids.append(Tree().generateRandomTree(alphabet, 2, numpy.ones(2) * 0.1, 2))

	# while converges:
	while True:
		
		#cluster assignment
		clusters = [[] for i in xrange(k)]
		for tree in trees:
			clusters[getClusterAssignment(tree, centroids, distanceCalculator)].append(tree)
			
		#cluster update
		for i in xrange(len(clusters)):
			if len(clusters[i]) == 0:
				(centroid, val) = centroidCalculator.getCentroid(clusters[i], alphabet)
			else:
				(centroid, val) = centroidCalculator.getCentroid(clusters[i], alphabet, centroids[i])
			centroids[i] = centroid
			vals[i] = val
			
		sValNew = sum(vals)
		print "sValNew:",sValNew
		if sValNew == sValOld:
			break
		sValOld = sValNew
		
		
		
def getClusterAssignment(tree, centroids, distanceCalculator):
	return numpy.argmin([distanceCalculator.calculateDistance(centroids[i], tree) for i in xrange(len(centroids))])


## Some test code
if __name__== '__main__':
	from constrained_ted import ConstrainedTED
	from centroid import MeanTree
	#from max_similarity import MaxSimilarityMetric1, MaxSimilarityMetric2, MaxSimilarityMetric3, MaxSimilarityMetric4
	filename = "../efficient_metrics/data/trees_type1.input"
	alphabet = [0, 1]
	trees = Tree.loadFromFile(filename)
#	print graph.to_string()
	# to save the good png: ccomps -x all_graph.dot | dot | gvpack -g | neato -s -n2 -Tpng > all_graph.png
	#graph.write_png("all_trees.png")
	
#	for tree in trees:
#		print func(tree, trees)

	distanceCalculator = ConstrainedTED()
	centroidCalculator = MeanTree(100, distanceCalculator)
	#distanceCalculator = MaxSimilarityMetric4()
	
	
	clusterForest(3, trees, alphabet, centroidCalculator, distanceCalculator)
	print "Complete"
