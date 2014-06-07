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
import pydot
import numpy as np
import numpy.random as rnd
from optparse import OptionParser
import os

def generateRandomPvalsRow(size):
	row = rnd.rand(size)
	row = row/sum(row)
	return row

if __name__ == '__main__':
	
	parser = OptionParser()
	parser.add_option("--typenum", action="store", default=1, type="int", dest="typenum", help="Number of type. Default: 1")
	parser.add_option("--alphasize", action="store", default=2, type="int", dest="alphasize", help="Size of the alphabet. Default: 2")
	parser.add_option("--trialsnum", action="store", default=100, type="int", dest="trialsnum", help="Number of trials. Default: 100")
	parser.add_option("--treesnum", action="store", default=30, type="int", dest="treesnum", help="Number of trees. Default: 30")
	parser.add_option("--treesize", action="store", default=10, type="int", dest="treesize", help="Minimum tree size. Default: 5")

	# parse options
	(options,args)=parser.parse_args()

	alphabet = range(1, options.alphasize+1)
	degree = 2
	pvals = np.array([[ 0.9,    0.1,   0.0,   0.0   ],
			 [ 0.9,    0.0,  0.1,  0.0 ], 
			 [ 0.2,    0.0,     0.0 ,  0.8 ]])
	size = len(alphabet)
	
	for nforests in xrange(options.trialsnum):
		treesNum = options.treesnum
		filename = "trees_type" + str(options.typenum) +  "_trial" + str(nforests)
	
		comment = """# file: """ + filename + """
# characteristic: the probability to stop after 1 is much higher then to stop after 0
# generated with parameters:
# alphabet = """ + str(alphabet) + """ : node labels
# size = """ + str(size) + """ : maximal number of children
# pvals = """ + str(pvals).replace("\n","") + """ : transition probabilities
# treesNum = """ + str(treesNum) + """ : number of trees"""
	
		graph = pydot.Dot()
		f = open(filename + ".input", "wt")
		f.write(comment + "\n")
		i = 0
		while i < treesNum:
		#for i in xrange(treesNum):
			t = Tree().generateRandomTree(alphabet, degree, pvals)
			if t.getSize() >= options.treesize:
				tree_graph = t.createGraph()
				graph.add_subgraph(tree_graph)
				f.write(t.toString() + "\n")
				i += 1
		f.close()
		f = open(filename + ".dot", "wt")
		f.write(graph.to_string())
		f.close()
	#	# to save the good png: ccomps -x all_graph.dot | dot | gvpack -g | neato -s -n2 -Tpng > all_trees.png
		
		os.system("ccomps -x %s.dot | dot | gvpack -g | neato -s -n2 -Teps > %s.eps"%(filename, filename))
		
