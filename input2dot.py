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
from optparse import OptionParser
import os

def read_trees(filename):
	f = open(filename)
	trees = []
	for l in f.xreadlines():
		if l.find('#') == -1:
			trees.append(Tree().load(l.strip()))
	return trees


def input2dot(f_in, f_out):
	trees = read_trees(f_in)
	graph = pydot.Dot()
	
	for t in trees:
		tree_graph = t.createGraph()
		graph.add_subgraph(tree_graph)
	f = open(f_out, "wt")
	f.write(graph.to_string())
	f.close()
#	# to save the good png: ccomps -x all_graph.dot | dot | gvpack -g | neato -s -n2 -Tpng > all_trees.png
	if options.plot:
		os.system("ccomps -x %s | dot | gvpack -g | neato -s -n2 -Teps > %s.eps"%(f_out, f_out.replace(".dot","")))


if __name__=='__main__':
	parser = OptionParser()
	parser.add_option("-i", action="store", type="string", dest="input", help="Input file")
	parser.add_option("-o", action="store", type="string", dest="output", help="Output file")
	parser.add_option("-p", action="store_true", default=False, dest="plot", help="Whether to plot a graph. Default: False")
	
#	
	# parse options
	(options,args)=parser.parse_args()
	
	if options.input and options.output:
		input2dot(options.input, options.output)
	else:
		parser.error("Input or output files not set")
