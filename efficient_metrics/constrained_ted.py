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
from Graph import Graph
from abstract_distance import AbstractDistance


from Tree import Tree

class ConstrainedTED(AbstractDistance):
	
	remove_cost = 1
	add_cost = 1
	relabel_cost = 1
	
	def calculateDistance(self, Tree1, Tree2):
		D_F_F = -1 * numpy.ones([Tree1.getSize()+1,Tree2.getSize()+1])
		D_T_T = -1 * numpy.ones([Tree1.getSize()+1,Tree2.getSize()+1])
		return self.getConstrainedTED(Tree1, Tree2, D_T_T, D_F_F)
	
	def getRelabelCost(self, v,w):
		if v.getLabel() == w.getLabel(): return 0
		return 1
	
	def getConstrainedTED(self, T1, T2, D_T_T, D_F_F):
		n1 = n2 = 0 #hashnum of empty node
		
		D_T_T[n1,n2] = 0
		D_F_F[n1,n2] = 0
		if D_T_T[T1.getHashNum(), T2.getHashNum()] != -1:
			return D_T_T[T1.getHashNum(), T2.getHashNum()]
		
		for node in T1.getVertices():
			d = 0
			for c in node.getChildren():
				D_T_T[c.getHashNum(), n2] = self.getConstrainedTED(c, Tree.getEmptyTree(), D_T_T, D_F_F)
				d += D_T_T[c.getHashNum(), n2]
			D_F_F[node.getHashNum(), n2] = d
			D_T_T[node.getHashNum(), n2] = D_F_F[node.getHashNum(), n2] + self.remove_cost
			
		for node in T2.getVertices():
			d = 0
			for c in node.getChildren():
				D_T_T[n1, c.getHashNum()] = self.getConstrainedTED(Tree.getEmptyTree(), c, D_T_T, D_F_F)
				d += D_T_T[n2, c.getHashNum()]
			D_F_F[n1, node.getHashNum()] = d
			D_T_T[n1, node.getHashNum()] = D_F_F[n1, node.getHashNum()] + self.add_cost
				
			
		for v in T1.getVertices():
			for w in T2.getVertices():
				if v.getChildren() == [] and w.getChildren() == []:
					#D_F_F[v.getHashNum(), w.getHashNum()] = 0
					D_F_F[v.getHashNum(), w.getHashNum()] = D_F_F[n1, n2]
				elif v.getChildren() == [] and w.getChildren() != []:
					#D_F_F[v.getHashNum(), w.getHashNum()] = sum([getConstrainedTED(Tree.getEmptyTree(), w_i, D_T_T, D_F_F) for w_i in w.getChildren()])
					D_F_F[v.getHashNum(), w.getHashNum()] = D_F_F[n1, w.getHashNum()]
				elif v.getChildren() != [] and w.getChildren() == []:
					#D_F_F[v.getHashNum(), w.getHashNum()] = sum([getConstrainedTED(v_i, Tree.getEmptyTree(), D_T_T, D_F_F) for v_i in v.getChildren()])
					D_F_F[v.getHashNum(), w.getHashNum()] = D_F_F[v.getHashNum(), n2]
				else:
					d1 = D_F_F[n1, w.getHashNum()] + min([D_F_F[v.getHashNum(), k.getHashNum()] - D_F_F[n1, k.getHashNum()] for k in w.getChildren()])
					d2 = D_F_F[v.getHashNum(), n2] + min([D_F_F[k.getHashNum(), w.getHashNum()] - D_F_F[k.getHashNum(), n2] for k in v.getChildren()])
					d3 = self.minMM(v,w, D_T_T, D_F_F)
					
					D_F_F[v.getHashNum(), w.getHashNum()] = min(d1,d2,d3)
				if w.getChildren() != []:
					d4 = self.getConstrainedTED(Tree.getEmptyTree(), w, D_T_T, D_F_F) + numpy.min([self.getConstrainedTED(v, k, D_T_T, D_F_F) - self.getConstrainedTED(Tree.getEmptyTree(), k, D_T_T, D_F_F) for k in w.getChildren()])
				else:
					d4 = self.getConstrainedTED(Tree.getEmptyTree(), w, D_T_T, D_F_F) + self. getConstrainedTED(v, Tree.getEmptyTree(), D_T_T, D_F_F)
				
				if v.getChildren() != []:
					d5 = self.getConstrainedTED(v, Tree.getEmptyTree(), D_T_T, D_F_F) + numpy.min([self.getConstrainedTED(k, w, D_T_T, D_F_F) - self.getConstrainedTED(k, Tree.getEmptyTree(), D_T_T, D_F_F) for k in v.getChildren()])
				else:
					d5 = self.getConstrainedTED(v, Tree.getEmptyTree(), D_T_T, D_F_F) + self.getConstrainedTED(Tree.getEmptyTree(), w, D_T_T, D_F_F) 
				
				d6 = D_F_F[v.getHashNum(), w.getHashNum()] + self.getRelabelCost(v, w)
				
				D_T_T[v.getHashNum(), w.getHashNum()] = min(d4, d5, d6)
		
		return D_T_T[T1.getHashNum(), T2.getHashNum()]
	
	
	def constructGraph(self, v,w, D_T_T, D_F_F):
		G = Graph()
		V = {}
		V['s'] = 0
		
		i = 1
		for v_i in v.getChildren():
			V["v" + str(v_i.getHashNum())] = i
			i += 1
			
		V['e_i'] = i
		i += 1
			
		for w_i in w.getChildren():
			V["w" + str(w_i.getHashNum())] = i
			i += 1
		
		V['e_j'] = i
		i += 1
		V['t'] = i
		
		G.V = range(len(V))
		
		G.capacity = numpy.zeros([len(V),len(V)])
		
		for v_i in v.getChildren():
			G.capacity[V['s'],V["v" + str(v_i.getHashNum())]] = 1	
			for w_i in w.getChildren():
				G.capacity[V["v" + str(v_i.getHashNum())],V["w" + str(w_i.getHashNum())]] = 1
			G.capacity[V["v" + str(v_i.getHashNum())],V['e_j']] = 1
				
		for w_i in w.getChildren():
			G.capacity[V["w" + str(w_i.getHashNum())], V['t']] = 1
			G.capacity[V['e_i'],V["w" + str(w_i.getHashNum())]] = 1
			
		G.capacity[V['s'],V['e_i']] = n_j = len(w.getChildren())
		G.capacity[V['e_j'],V['t']] = n_i = len(v.getChildren())
		G.capacity[V['e_i'],V['e_j']] = max(n_i, n_j) - min(n_i, n_j)
		
		G.cost = numpy.zeros([len(V),len(V)])
		for v_i in v.getChildren():
			for w_i in w.getChildren():
				G.cost[V["v" + str(v_i.getHashNum())], V["w" + str(w_i.getHashNum())]] = self.getConstrainedTED(v_i, w_i, D_T_T, D_F_F)
				G.cost[V['e_i'], V["w" + str(w_i.getHashNum())]] = self.getConstrainedTED(Tree.getEmptyTree(), w_i, D_T_T, D_F_F)
			G.cost[V["v" + str(v_i.getHashNum())], V['e_j']] = self.getConstrainedTED(v_i, Tree.getEmptyTree(), D_T_T, D_F_F)
		
		G.init_edges()
		G.init_cost_rev()
		return (G,V)
				
	
	def minMM(self, v,w, D_T_T, D_F_F):
		(G, Vmap) = self.constructGraph(v, w, D_T_T, D_F_F)
		flow = G.getMinCostMaxFlow(Vmap['s'], Vmap['t'])
		return flow
	
AbstractDistance.register(ConstrainedTED)
