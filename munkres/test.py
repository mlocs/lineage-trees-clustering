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

from pymunkres import Munkres
import numpy as np
import timeit
data = np.array([[0, 0], [1,1]], 'd')
Munkres().maxWeightMatching(data)

#print timeit.Timer(stmt = 'Munkres().maxWeightMatching(data)', setup = """from pymunkres import Munkres
#import numpy as np
#data =  np.array([[3,3,3], [1,2,3],[3,3,2]], 'd')""").timeit(number=1000)


