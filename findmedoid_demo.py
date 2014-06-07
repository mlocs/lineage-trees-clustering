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

from meta_algorithm import findMedian as findMedoid
from Tree import Tree
from max_similarity import MaxSimilarityMetric1, MaxSimilarityMetric2, MaxSimilarityMetric3, MaxSimilarityMetric4
from constrained_ted import ConstrainedTED
from multiprocessing import Pool
import numpy as np
from numpy import zeros
import pickle
from optparse import OptionParser
import logging
from os.path import isfile

# Calculate distance matrix using define distance object
# @param input_data a tuple (<array of trees>, <distance calculator object>)
# @ return distance matrix
def calculate_distances(input_data):
	trees, distance_calculator = input_data
	size = len(trees)
	distances = zeros([size, size])
	for i in xrange(size):
		for j in xrange(i,size):
			distances[i,j] = distances[j,i] = distance_calculator.calculateDistance(trees[i], trees[j])
	return distances
	

def main():
	logging.basicConfig()
	parser = OptionParser()
	parser.add_option("-m", "--metric", dest="metric", action='append',
					  type="int", help="Use following metric: 0 - "
					  + "constrained TED, [1,...,4] - Similarity [1,...,4]")
	parser.add_option("-i", "--input", dest="input_file", type="string",
					  action='store', help="Input file with trees")
	parser.add_option("-o", "--output", dest="output_file", type="string",
					  action='store', help="Output file. Default: <input>.out",
					  default="")
	parser.add_option("-p", "--processors", action="store", type="int", default=1,
					  dest="processors", help="Number of CPUs. Default: 1")	
	parser.add_option("-k", "--k_start", action="store", type="int", default=2,
					  dest="k_start", help="Number of clusters to start. Default: 2")	
	parser.add_option("-K", "--k_finish", action="store", type="int", default=2,
					  dest="k_finish", help="Number of clusters to finish. Default: 2")
	(options, args) = parser.parse_args()
	
	if options.metric == None  or len(options.metric) == 0:
		parser.error("No metric types specified")
		
	if options.input_file == None or not isfile(options.input_file):
		 parser.error("No input file specified or the file does not exist")
	else: input_file = options.input_file
	if options.output_file == None or options.output_file=="":
		 output_file = options.input_file + ".out"
	else: output_file = options.output_file
	
	
	# deserialize all trees into an array
	trees = Tree.loadFromFile(input_file)
	
	# array with different distance objects
	distance_calculators = []
	for m in options.metric:
		if m == 0:
			distance_calculators.append(ConstrainedTED())
		elif m == 1:
			distance_calculators.append(MaxSimilarityMetric1())
		elif m == 2:
			distance_calculators.append(MaxSimilarityMetric2())
		elif m == 3:
			distance_calculators.append(MaxSimilarityMetric3())
		elif m == 4:
			distance_calculators.append(MaxSimilarityMetric4())
		else:
			logging.error("Unknown metric type")
	
	# format input so it can be calculated parallel in Pool
	input_data = [(trees, dc) for dc in distance_calculators]
	pool = Pool(processes=options.processors)
	
	# calculate distance matrices
	distances = pool.map(calculate_distances, input_data)
	
	# calculate medoids	
	logging.info( "Start calculating medoids" )
	medoid_input = [(d,k) for d in distances for k in
			range(options.k_start,options.k_finish+1)]
	result = pool.map(findMedoid, medoid_input)
	# the result array has the form [(<distance matrix>, k, ([<sequence
	# numbers of medoid trees>], value function)), (...),...]
	
	# results are serialized with pickle, so you have to use pickle.load to 
	# deserialize them later
	logging.info("Calculation completed")
	logging.info("Saving the files with clusters")
	i = 0
	for metric in  options.metric:
		for k in xrange(options.k_start, options.k_finish+1):
			centroids = result[i][2][0] #centroid indices
			fname = 'centroids.m%i.k%i.out'%(metric, k)
			#np.savetxt(fname, centroids)
			D = result[i][0] # distance matrix
			fname = 'distance.m%i.out'%(metric)
			#np.savetxt(fname, D)
			clusters = {} # cluster lists
			for cidx in centroids: clusters[cidx]=[trees[cidx]]
            # find the closest centroids to every tree in D
			assignments = [centroids[cidx] for cidx in
					np.argmin(D[:,centroids], axis=1)]
			print assignments
			fname = 'assignments.m%i.k%i.out'%(metric, k)
			#np.savetxt(fname, assignments)
            # append trees to cluster lists
			for tidx in xrange(len(trees)):
				clusters[assignments[tidx]].append(trees[tidx])
            # print out clusters into different files. Centroid is printed out twice
			for cidx in centroids:
				fname = 'cluster%i.m%i.k%i.out'%(cidx,metric, k)
				fout = open(fname, 'wt')
				for tree in clusters[cidx]:
					fout.write("%s\n"%tree.toString())
				fout.close()
			i += 1
	

if __name__ == "__main__":
	main()
