from pyted import *

treeF = Load("treeF.txt")
treeG = Load("treeG.txt")
dist = Distance()
ted = TED(treeF, treeG, dist, 0)
print "The distnace is:",ted.GetTED()


