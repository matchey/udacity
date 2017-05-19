# -----------
# User Instructions
#
# Define a function smooth that takes a path as its input
# (with optional parameters for weight_data, weight_smooth,
# and tolerance) and returns a smooth path. The first and 
# last points should remain unchanged.
#
# Smoothing should be implemented by iteratively updating
# each entry in newpath until some desired level of accuracy
# is reached. The update should be done according to the
# gradient descent equations given in the instructor's note
# below (the equations given in the video are not quite 
# correct).
# -----------

from copy import deepcopy

# thank you to EnTerr for posting this on our discussion forum
def printpaths(path,newpath):
    for old,new in zip(path,newpath):
        print '['+ ', '.join('%.3f'%x for x in old) + \
               '] -> ['+ ', '.join('%.3f'%x for x in new) +']'

# Don't modify path inside your function.
path = [[0, 0],
        [0, 1],
        [0, 2],
        [1, 2],
        [2, 2],
        [3, 2],
        [4, 2],
        [4, 3],
        [4, 4]]

def smooth(path, weight_data = 0.5, weight_smooth = 0.1, tolerance = 0.000001):
    a = weight_data
    b = weight_smooth
    newpath = deepcopy(path)
    
    flag = True
    while flag:
        flag = False
        for i in range(1,len(path)-1):
            bf = newpath[i]
            newpath[i] = [y1+a*(x-y1)+b*(y2+y0-2*y1) for (x,y1,y0,y2) in zip(path[i],bf,newpath[i-1],newpath[i+1])]
            flag = flag or sum([(x-y)*(x-y) for (x,y) in zip(newpath[i],bf)]) >= tolerance*tolerance
    return newpath # Leave this line for the grader!

printpaths(path,smooth(path))
