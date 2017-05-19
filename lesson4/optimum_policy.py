# ----------
# User Instructions:
# 
# Write a function optimum_policy that returns
# a grid which shows the optimum policy for robot
# motion. This means there should be an optimum
# direction associated with each navigable cell from
# which the goal can be reached.
# 
# Unnavigable cells as well as cells from which 
# the goal cannot be reached should have a string 
# containing a single space (' '), as shown in the 
# previous video. The goal cell should have '*'.
# ----------

grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0]]
init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1 # the cost associated with moving from a cell to an adjacent one

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

def judge(value,cell,closed):
    rtn = -1
    mini=value[cell[0]][cell[1]]
    for a in range(len(delta))[::-1]:
        if closed[cell]>=pow(2,a):
            closed[cell]-=pow(2,a)
            x = cell[0]+delta[a][0]
            y = cell[1]+delta[a][1]
            if value[x][y] < mini:
                mini = value[x][y]
                rtn = a
    if rtn+1:
        rtn = delta_name[rtn]
    else:
        rtn = ' '
    return rtn

def optimum_policy(grid,goal,cost):
    value = [[99 for row in range(len(grid[0]))] for col in range(len(grid))]
    policy = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]
    closed={}
    change = True

    while change:
        change = False
        for x in range(len(grid)):
            for y in range(len(grid[0])):
                closed[(x,y)]=0
                tmp=0
                if goal[0] == x and goal[1] == y:
                    if value[x][y] > 0:
                        value[x][y] = 0
                        change = True
                elif grid[x][y] == 0:
                    for a in range(len(delta)):
                        x2 = x + delta[a][0]
                        y2 = y + delta[a][1]
                        if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]) and grid[x2][y2] == 0:
                            v2 = value[x2][y2] + cost
                            tmp+=pow(2,a)
                            if v2 < value[x][y]:
                                change = True
                                value[x][y] = v2
                if not closed[(x,y)]:
                    closed[(x,y)]=tmp
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            policy[x][y]=judge(value,(x,y),closed)
    policy[goal[0]][goal[1]]='*'
    return policy

def show_result(func):
    for row in func:
        print row

show_result(optimum_policy(grid,goal,cost))

