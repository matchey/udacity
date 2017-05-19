# -*- coding: utf-8 -*-
# ----------
# User Instructions:
# 
# Define a function, search() that returns a list
# in the form of [optimal path length, row, col]. For
# the grid shown below, your function should output
# [11, 4, 5].
#
# If there is no valid path from the start point
# to the goal, your function should return the string
# 'fail'
# ----------

# Grid format:
#   0 = Navigable space
#   1 = Occupied space

from first_search import search as s

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0]]
init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1

# delta = [[-1, 0], # go up
#          [ 0,-1], # go left
#          [ 1, 0], # go down
#          [ 0, 1]] # go right

delta = [[ 0,-1], # go up
         [-1, 0], # go left
         [ 0, 1], # go down
         [ 1, 0]] # go right

delta_name = ['^', '<', 'v', '>']

print(s(grid,init,goal,cost))


