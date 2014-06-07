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
from VSH import *
from lagrangian_relaxation import *
from branches_and_bounds import *

# @param D distance matrix
# @param p number of centroids
def findMedian(D,p=-1):
    if p == -1:
        p = D[1]
        D = D[0]
    # consider the trivial case of p = 1
    if p == 1:
        Dsum = numpy.sum(D, axis=0)
        idx = numpy.argmin(Dsum)
        k = Dsum[idx]
        return (D, p, ([idx], k))
    phase1_iterations = 20
    phase1_medians = []
    phase1_Z_H = []
    print "stage 1"
    # Stage 1: Run 20 replications of the VS heuristic to obtain an upper bound on the optimal solution Z_H
    for i in xrange(phase1_iterations):
        (m,Z_H) = VS(D,p)
        phase1_medians.append(m)
        phase1_Z_H.append(Z_H)
        
    iMax = numpy.argmin(phase1_Z_H)
    Z_H = min(phase1_Z_H)
    median = phase1_medians[iMax]
    print Z_H," ",median
    print "stage 2"
    # Stage 2: Run the Lagrangian relaxation algorithm with 5 restarts of the procedure with a maximum of 4000 iterations each
    if LR2(D,p,Z_H):
        # If optimal solution is not found
        return (D,p,(median,Z_H))
    else:
        print "stage 3"
        # Stage 3: Run the Branch-and-Bound algorithm with an embedded Lagrangian relaxation scheme
        return (D,p,BnB(D,median,p))
