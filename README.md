
> Lineage Tree Clustering
> Copyright (C) 2014  
>
> Lineage Tree Clustering is free software: you can redistribute it and/or modify
> it under the terms of the GNU General Public License as published by
> the Free Software Foundation, either version 3 of the License, or
> (at your option) any later version.
>
> Lineage Tree Clustering project is distributed in the hope that it will be useful,
> but WITHOUT ANY WARRANTY; without even the implied warranty of
> MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
> GNU General Public License for more details.
>
> You should have received a copy of the GNU General Public License
> along with the Lineage Tree Clustering project files.  If not, see <http://www.gnu.org/licenses/>.


Lineage Tree Clustering
=======================

Software requirement:
---------------------

- Scons (www.scons.org)
- Swig (www.swig.org)
- Python (>= 2.6)
- Graphviz dot and pydot python interfance are required for graphics generation 


Installation process:
---------------------

Step 1. First we need to compile the libmunkres library to solve the assignment
problem in cTED.
Just go to /munkres and compile the library by calling
$ scons

This will generate three files:
_pymunkres.so
libmunkres.a
pymunkres.py

You should copy all these files into the directory /efficient_metrics

Step 2. Make sure youre direcories /efficient_metrics and /clustering are in $PYTHONPATH
environment variable so that modules can be found by the python interpreter.

Using the code
---------------

### findmedoid_demo.py 

The file findmedoid_demo.py illustrates how to use the code. You can run the demo with 
$ python findmedoid_demo.py -i dataset_demo.input -m 2 -m 4 -p 2 -k 2 -K 3

This will generate an number of output files like cluster5.m4.k2.out which
contains all trees assigned to the medoid from the 5th line of the input file,
while the clustering was conducted using distance metric 4 (MaxSimilarity 4)
with 2 clusters.

You can generate even more files with usefull information by uncommenting
corresponding lines in the demo file.

### input2dots.py 

Create eps output using input2dots.py:
$ python input2dot.py -i dataset_demo.input -o test.dot -p

This will generates two files:
- test.eps the visualisation of trees
- test.dot the input file for the graphviz dot program

The second file can be used, e.g. to produce visualization with different parameters.

### visTreeClustering.m 

This Matlab script shows an example of how to produce visualization of clusters
similar to those used in the paper. In order to use it you would need to
uncomment the additional outputs in findmedoid_demo.py to generate necessary
input files.

