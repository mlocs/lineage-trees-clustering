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
import sys


class Graph:
	E = None #Adjacency list
	V = None #List of vertices
	cost = None #Matrix of costs: c[i,j] are costs from i to j
	cost_rev = None #Matrix of reverse costs, used in max-flow algorithms
	capacity = None #Capacity matrix
	capacity_rev = None 
	
	def init_edges(self):
		self.E = []
		for i in xrange(self.cost.shape[0]):
			for j in xrange(self.cost.shape[0]):
				if self.capacity[i,j]:
					self.E.append((i,j))
					
	
	def init_cost_rev(self):
		size = self.cost.shape[0]
		self.cost_rev = np.zeros([size,size])
		self.capacity_rev = np.zeros([size,size])

	
	def BellmanFord(self,s,t):
	#  This implementation takes in a graph, represented as lists of vertices
	#   and edges, and modifies the vertices so that their distance and
	#   predecessor attributes store the shortest paths.
	#
		
		self.init_edges()
		
		predecessor = -1*np.ones(len(self.V))
	
	#   Step 1: Initialize graph
	#   for each vertex v in vertices:
		distance = sys.maxint*np.ones(len(self.V))
		distance[s] = 0
#		for v in self.V:
	#       if v is source then v.distance := 0
#			if v == s: distance[v] = 0
	#       else v.distance := infinity
#			else: distance[v] = sys.maxint
	
	#   
	#   // Step 2: relax edges repeatedly
	#   for i from 1 to size(vertices)-1:  
		for i in xrange(0,len(self.V)):  
	#       for each edge uv in edges: // uv is the edge from u to v
			for (u,v) in self.E:
	#           u := uv.source
	#           v := uv.destination             
	#           if u.distance + uv.weight < v.distance:
				if distance[u] + self.cost[u,v] < distance[v]:
	#               v.distance := u.distance + uv.weight
					distance[v] = distance[u] + self.cost[u,v]
	#               v.predecessor := u
					predecessor[v] = u
	#
	#   // Step 3: check for negative-weight cycles
	#   for each edge uv in edges:
		if max(predecessor) == -1:
			raise Exception("Graph contains a negative-weight cycle")
		else:
			for (u,v) in self.E:
		#       u := uv.source
		#       v := uv.destination
		#       if u.distance + uv.weight < v.distance:
				if distance[u] + self.cost[u,v] < distance[v]:
		#           error "Graph contains a negative-weight cycle"
					raise Exception("Graph contains a negative-weight cycle")
		return (predecessor, distance)
	
	
	def hasPath(self,s,t):
		try:
			(predecessor, distance) = self.BellmanFord(s,t)
			if predecessor[t] == -1:
				return False
		except:
			return False
		return True
	
	def ReduceCost(self, predecessor, Pi):
	# For each (i,j) in E_x do
		for (i,j) in self.E:
			# c_{ij} <- c_{ij} + Pi_i - Pi_j
			if Pi[i] != sys.maxint and Pi[j] != sys.maxint:
				self.cost[i,j] = self.cost[i,j] + Pi[i] - Pi[j]
			# c_{rev(i,j)} <- 0
			# for the purpose of IDP c_rev is not needed (no circles, however I leave it here for  generality
			#G_x.cost_rev[i,j] = 0 
		self.init_edges()
#		return G_x


	def AugmentFlow(self,P,s,t):
		
		path = []
		v = t
		while True:
			u = P[v]
			path.append((u,v))
			if u == s:
				break
			v = u
		capacity = sys.maxint	
		for (u,v) in path:
			capacity = min(capacity, self.capacity[u,v])
		for (u,v) in path:
			self.capacity[u,v] -= capacity
			#G.capacity[v,u] += capacity
			self.capacity_rev[u,v] += capacity
		#return G
	
	
	def ssp_wp(self,s,t):
		# Initial flow x with zero
		x = np.zeros([len(self.V),len(self.V)]) #x will be an integral feasible solution
		#Use Bellman-Ford's algorithm to establish potentials Pi
		(predecessor,Pi) = self.BellmanFord(s,t)
		#Reduce Cost (Pi)
		self.ReduceCost(predecessor, Pi)
		
		#while (G_x contains a path from s to t) do
		while self.hasPath(s,t):
			
			#Find any shortest path P from s to t
			(P,Pi) = self.BellmanFord(s,t)
			# Reduce Cost (Pi)
			self.ReduceCost(P, Pi)
			# Augment current flow in G along P
			self.AugmentFlow(P,s,t)
		#return G
	
	
	def getMinCostMaxFlow(self, s, t):
		cost = self.cost.copy()
		self.ssp_wp(s, t)
		s = 0
		for i in xrange(len(self.V)):
			for j in xrange(i+1,len(self.V)):
				s += cost[i,j]*self.capacity_rev[i,j]
		
		return s
