import numpy
import math
from meta_algorithm import findMedian

if __name__ == '__main__':
  import sys, os
  pathname = os.path.dirname(__file__)
  pathsgpp = os.path.abspath(pathname) + '/../TED_Final/source'
  if pathsgpp not in sys.path: sys.path.append(pathsgpp)

  import pyted

  points = [[3,3],[3,5],[4,5],[6,5],[7,8],[9,7],[9,8]]
  n = len(points)
  D = numpy.zeros([n,n])
  for i in xrange(n):
	  for j in xrange(n):
		  d = math.sqrt((points[i][0]-points[j][0])**2 + (points[i][1]-points[j][1])**2)
		  D[i,j] = d
		
  p = 3
  median,Z_H = findMedian(D,p)
  print "(median, Z_H): ",median,",",Z_H,")"

  (m, Z_H) = VS(D,p)
  print "median",m
  print "Z_H=",Z_H
  print "LR2"
  print LR2(D, p, Z_H)
  print "BnB"
  gamma = [1,-1]
  gamma_star,Z_star = BnB(D,m,p)
  print "Results of BnB: gamma_star",gamma_star,"with Z_star",Z_star

		

	
