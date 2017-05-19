# ----------
# Part Five
#
# This time, the sensor measurements from the runaway Traxbot will be VERY 
# noisy (about twice the target's stepsize). You will use this noisy stream
# of measurements to localize and catch the target.
#
# ----------
# YOUR JOB
#
# Complete the next_move function, similar to how you did last time. 
#
# ----------
# GRADING
# 
# Same as part 3 and 4. Again, try to catch the target in as few steps as possible.

from robot import *
from math import *
from matrix import *
import random

def saijien(measurement):
    K=matrix([[0.,0.,0.],[0.,0.,0.],[0.,0.,0.]]) #Coefficient
    T=matrix([[0.],[0.],[0.]]) #Constants
    S=matrix([[0.],[0.],[0.]]) #Kai
    for x,y in measurement[1:]:
        K += matrix([[x**2, x*y,  x ],
                     [x*y,  y**2, y ],
                     [x,    y,    1.]])
        T -= matrix([[x**3+x*y**2],
                     [x**2*y+y**3],
                     [x**2+y**2  ]])
    S = K.inverse()*T
    center = (-S.value[0][0]/2, -S.value[1][0]/2)
    radius = sqrt(center[0]**2 + center[1]**2 - S.value[2][0])

    return center, radius

# def saijien(measurement):
#     K=matrix([[0.,0.,0.],[0.,0.,0.],[0.,0.,0.]]) #Coefficient
#     T=matrix([[0.],[0.],[0.]]) #Constants
#     S=matrix([[0.],[0.],[0.]]) #Kai
#     while True:
#         x,y = measurement[len(measurement)-1]
#
#         K += matrix([[x**2, x*y,  x ],
#                      [x*y,  y**2, y ],
#                      [x,    y,    1.]])
#         T -= matrix([[x**3+x*y**2],
#                      [x**2*y+y**3],
#                      [x**2+y**2  ]])
#         S = K.inverse()*T
#         center = (-S.value[0][0]/2, -S.value[1][0]/2)
#         radius = sqrt(center[0]**2 + center[1]**2 - S.value[2][0])
#         
#         yield center, radius

def update(mean1, var1, mean2, var2):
    new_mean = tuple([(var2*m1+var1*m2)/(var1 + var2) for (m1,m2) in zip(mean1,mean2)])
    # new_mean = (var2 * mean1 + var1 * mean2) / (var1 + var2)
    # new_var = ( 1/(1/v1 + 1/v2) for (v1,v2) in zip(var1,var2))
    new_var = 1.0/(1.0/var1 + 1.0/var2)
    return [new_mean, new_var]

def predict(mean1, var1, round_ang, radius, center, var2):
    # new_mean = mean1+mean2
    # new_mean = ( m1+m2 for (m1,m2) in zip(mean1,mean2))
    new_var = var1+var2
    # new_var = ( v1+v2 for (v1,v2) in zip(var1,var2))
    estimate = matrix([[cos(round_ang), -sin(round_ang)],
                       [sin(round_ang),  cos(round_ang)]]) *\
               matrix([[radius/distance_between(mean1,center),0],
                       [0,radius/distance_between(mean1,center)]])*matrix([[mean1[0]-center[0]],
                                                                           [mean1[1]-center[1]]]) +\
               matrix([[center[0]],
                       [center[1]]])
    new_mean = (estimate.value[0][0], estimate.value[1][0])
    return [new_mean, new_var]

def estimate_next_pos(steps, max_distance, measurement, OTHER = None):
    """Estimate the next (x, y) position of the wandering Traxbot
    based on noisy (x, y) measurements."""
    if OTHER:
        # if len(OTHER)<100 or fabs(distance_between(OTHER[0][0], measurement)) < 2.0*max_distance:
        #     OTHER.append(measurement)
        OTHER.append(measurement)
        if len(OTHER)<4:
            mean1 = measurement
            var1 = 10000
            OTHER[0] = [[mean1, var1],[(0,0),0]]
            xy_estimate = OTHER[0][0][0]
        else:
            if len(OTHER)==5 or not len(OTHER)%6:
                OTHER[0][1][0], OTHER[0][1][1] = saijien(OTHER)
            center, radius = OTHER[0][1][0], OTHER[0][1][1]
            if len(OTHER)>250:
                if not (0.00*radius <= fabs(distance_between(center, measurement)) < 1.00*radius):
                    OTHER.pop()
                    # print("poped by r")
                elif fabs(distance_between(OTHER[0][0][0], measurement)) > 0.7*radius:
                # elif fabs(distance_between(OTHER[0][0][0], measurement)) > 3.5*max_distance:
                    OTHER.pop()
                    # print("poped by est")
            print "(%5.1f,%5.1f)" % (center),"%5.1f" % radius
            # if len(OTHER)>90:
            #     center = (-0.8, 17.1)
            #     radius = 7.2
            ang = 0.0
            for i in xrange(1,len(OTHER)-1):
                ang += angle_between(center, radius, OTHER[i], OTHER[i+1])
                
            ang_mean = ang/(len(OTHER)-1)
            # print(2*pi/ang_mean)
            # ang_mean = 2*pi/30
            # steps = 1
            round_ang = steps * ang_mean
            var_measure = 960
            OTHER[0][0] = update(OTHER[0][0][0], OTHER[0][0][1], measurement, var_measure)
            var_move = 11
            OTHER[0][0] = predict(OTHER[0][0][0], OTHER[0][0][1], round_ang, radius, center, var_move)
            xy_estimate = OTHER[0][0][0]
    else:
        OTHER = [measurement]
        xy_estimate = measurement
        OTHER.append(measurement)
    return xy_estimate, OTHER

def circle_next_pos(hunter_position, measurement, OTHER = None):#{{{
    """Estimate the next (x, y) position of the wandering Traxbot
    based on noisy (x, y) measurements."""
    if OTHER:
        OTHER.append(measurement)
        if len(OTHER)<4:
            xy_estimate = measurement
        else:
            center, radius = saijien(OTHER)
            ang = 0.0
            for i in xrange(1,len(OTHER)-1):
                ang += angle_between(center, radius, OTHER[i], OTHER[i+1])

            ang_mean = ang/(len(OTHER)-1)
            # print int(2.0*pi/ang_mean)
            if(len(OTHER[0])-3):
                round_ang = -fabs(ang_mean)
                estimate = matrix([[cos(round_ang), -sin(round_ang)],
                                   [sin(round_ang),  cos(round_ang)]]) *\
                           matrix([[radius/distance_between(hunter_position,center),0],
                                   [0,radius/distance_between(hunter_position,center)]])*matrix([[hunter_position[0]-center[0]],
                                                                                             [hunter_position[1]-center[1]]]) +\
                           matrix([[center[0]],
                                   [center[1]]])
                xy_estimate = (estimate.value[0][0], estimate.value[1][0])
            else:
                OTHER[0] = [center[0]+radius, center[1], int(2*pi/ang_mean), 0]
                xy_estimate = (center[0]+radius, center[1])
    else:
        OTHER = [measurement]
        xy_estimate = measurement
        OTHER.append(measurement)

    # You must return xy_estimate (x, y), and OTHER (even if it is None) 
    # in this order for grading purposes.
    # xy_estimate = (3.2, 9.1)
    return xy_estimate, OTHER#}}}

def next_move0(hunter_position, hunter_heading, target_measurement, max_distance, OTHER = None):#{{{
    # This function will be called after each time the target moves. 
    
    # steps = not OTHER or not len(OTHER)%6 and 3 or 1
    if OTHER == None:
        xy_estimate, OTHER = circle_next_pos(hunter_position, target_measurement, OTHER)

        heading_to_estimate = get_heading(hunter_position, xy_estimate)
        heading_difference = heading_to_estimate - hunter_heading
        turning =  heading_difference # turn towards the target
        distance = max_distance
    else:
        # OTHER[0] = hunter_position
        if(len(OTHER)>500):
            if(OTHER[0][3]>10):
                distance = 0.1 * max_distance
                if(not OTHER[0][3]%(OTHER[0][2]+3)):
                    xy_estimate = (OTHER[0][0] - 0.1*max_distance, OTHER[1][1] - 0.1*max_distance)
                    # xy_estimate = (xy_estimate[0] - 0.1*(OTHER[0][2]+3)*max_distance, xy_estimate[1] - 0.1*(OTHER[0][2]+3)*max_distance)
                else:
                    xy_estimate = (OTHER[0][1], OTHER[0][2])
            else:
                distance = max_distance
                xy_estimate = (OTHER[0][1], OTHER[0][2])
            OTHER[0][3] = OTHER[0][3] + 1
            heading_to_estimate = get_heading(hunter_position, xy_estimate)
            heading_difference = heading_to_estimate - hunter_heading
            turning =  heading_difference # turn towards the target
            while fabs(turning)>=pi:
                turning = (turning+2*pi)%2*pi
        else:
            xy_estimate, OTHER = circle_next_pos(hunter_position, target_measurement, OTHER)
            
            if(len(OTHER)==50):
                OTHER[0]=[xy_estimate[0],xy_estimate[1],100]
           
                xy_estimate, OTHER = circle_next_pos(hunter_position, target_measurement, OTHER)
            
            heading_to_estimate = get_heading(hunter_position, xy_estimate)
            heading_difference = heading_to_estimate - hunter_heading
            turning =  heading_difference # turn towards the target
            while fabs(turning)>=pi:
                turning = (turning+2*pi)%2*pi
            distance = max_distance
            # if(len(OTHER)%4):
            #     distance = 0.0
    # The OTHER variable is a place for you to store any historical information about
    # the progress of the hunt (or maybe some localization information). Your return format
    # must be as follows in order to be graded properly.
    return turning, distance, OTHER#}}}

def wait_pos(init, max_distance, OTHER):
    # step_x = len(OTHER)%100
    # step_y = len(OTHER)%1000
    step_x = random.random()%2000
    step_y = random.random()%2000

    pos_x = init[0] + 2.0*max_distance*(0.001*step_x - 1.0)
    pos_y = init[1] + 2.0*max_distance*(0.001*step_y - 1.0)
    xy_estimate = (pos_x, pos_y)
    return xy_estimate

def next_move(hunter_position, hunter_heading, target_measurement, max_distance, OTHER = None):
    # This function will be called after each time the target moves. 
    steps = not OTHER or len(OTHER)%56<2 and 3 or 1
    # steps =1

    xy_estimate, OTHER = estimate_next_pos(steps, max_distance, target_measurement, OTHER)

    heading_to_estimate = get_heading(hunter_position, xy_estimate)
    heading_difference = heading_to_estimate - hunter_heading
    turning =  angle_trunc(heading_difference) # turn towards the target
    xte = distance_between(hunter_position, xy_estimate)
    distance = max_distance < xte and max_distance or xte # full speed ahead!

    # The OTHER variable is a place for you to store any historical information about
    # the progress of the hunt (or maybe some localization information). Your return format
    # must be as follows in order to be graded properly.
    return turning, distance, OTHER

def distance_between(point1, point2):
    """Computes distance between point1 and point2. Points are (x, y) pairs."""
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def angle_between(center, radius, point1, point2):
    """Computes distance between point1 and point2. Points are (x, y) pairs."""
    x1, y1 = point1
    x2, y2 = point2
    ox, oy = center 
    cos_value = radius and ((x1-ox)*(x2-ox)+(y1-oy)*(y2-oy))/radius**2 or 0
    d_theta = fabs(cos_value) <= 1 and acos(cos_value) or 0
    # print 180*d_theta/(2*pi)
    theta1 = atan2(y1-oy, x1-ox)
    theta2 = atan2(y2-oy, x2-ox)
    while(theta1<0):
        theta1 = (theta1 + 2*pi)%(2*pi)
    while(theta2<0):
        theta2 = (theta2 + 2*pi)%(2*pi)
    d_theta = (theta2 - theta1)
    while fabs(d_theta)>pi:
        # d_theta = pi - (2*pi - d_theta)%(2*pi)
        d_theta = pi - (d_theta + 2*pi)%(2*pi)
    # print "theta=", 180*d_theta/(2*pi)
    # print"==="
    return d_theta

def demo_grading2(hunter_bot, target_bot, next_move_fcn, OTHER = None):
    """Returns True if your next_move_fcn successfully guides the hunter_bot
    to the target_bot. This function is here to help you understand how we 
    will grade your submission."""
    max_distance = 0.97 * target_bot.distance # 0.98 is an example. It will change.
    # max_distance = 1.11 * target_bot.distance # 0.98 is an example. It will change.
    separation_tolerance = 0.9 * target_bot.distance # hunter must be within 0.02 step size to catch target
    caught = False
    ctr = 0
    #For Visualization
    import turtle
    window = turtle.Screen()
    window.bgcolor('white')
    
    chaser_robot = turtle.Turtle()
    chaser_robot.shape('arrow')
    chaser_robot.color('blue')
    chaser_robot.resizemode('user')
    chaser_robot.shapesize(0.3, 0.3, 0.3)
    broken_robot = turtle.Turtle()
    broken_robot.shape('turtle')
    broken_robot.color('green')
    broken_robot.resizemode('user')
    broken_robot.shapesize(0.3, 0.3, 0.3)
    size_multiplier = 15.0 #change size of animation
    chaser_robot.hideturtle()
    chaser_robot.penup()
    chaser_robot.goto(hunter_bot.x*size_multiplier, hunter_bot.y*size_multiplier-100)
    chaser_robot.showturtle()
    broken_robot.hideturtle()
    broken_robot.penup()
    broken_robot.goto(target_bot.x*size_multiplier, target_bot.y*size_multiplier-100)
    broken_robot.showturtle()
    
    measuredbroken_robot = turtle.Turtle()
    measuredbroken_robot.shape('circle')
    measuredbroken_robot.color('red')
    measuredbroken_robot.penup()
    measuredbroken_robot.resizemode('user')
    measuredbroken_robot.shapesize(0.1, 0.1, 0.1)
    broken_robot.pendown()
    chaser_robot.pendown()
    #End of Visualization
    # We will use your next_move_fcn until we catch the target or time expires.
    minimam = 10 * max_distance
    while not caught and ctr < 1000:
        # Check to see if the hunter has caught the target.
        hunter_position = (hunter_bot.x, hunter_bot.y)
        target_position = (target_bot.x, target_bot.y)
        separation = distance_between(hunter_position, target_position)
        # if minimam > fabs(separation):
        #     minimam = fabs(separation)
        #     # print minimam/(0.02*separation_tolerance)*100,"%"
        #     if minimam/(max_distance)*100 < 10:
        #         print minimam/(max_distance)*100,"%"
        if separation < 0.02 * separation_tolerance:
            print "You got it right! It took you ", ctr, " steps to catch the target."
            caught = True

        # The target broadcasts its noisy measurement
        target_measurement = target_bot.sense()

        # This is where YOUR function will be called.
        turning, distance, OTHER = next_move_fcn(hunter_position, hunter_bot.heading, target_measurement, max_distance, OTHER)

        # Don't try to move faster than allowed!
        if distance > max_distance:
            distance = max_distance

        # We move the hunter according to your instructions
        hunter_bot.move(turning, distance)

        # The target continues its (nearly) circular motion.
        target_bot.move_in_circle()
        #Visualize it
        measuredbroken_robot.setheading(target_bot.heading*180/pi)
        measuredbroken_robot.goto(target_measurement[0]*size_multiplier, target_measurement[1]*size_multiplier-100)
        measuredbroken_robot.stamp()
        broken_robot.setheading(target_bot.heading*180/pi)
        broken_robot.goto(target_bot.x*size_multiplier, target_bot.y*size_multiplier-100)
        chaser_robot.setheading(hunter_bot.heading*180/pi)
        chaser_robot.goto(hunter_bot.x*size_multiplier, hunter_bot.y*size_multiplier-100)
        #End of visualization
        ctr += 1            
        if ctr >= 1000:
            print "It took too many steps to catch the target."
    return caught


def demo_grading(hunter_bot, target_bot, next_move_fcn, OTHER = None):
    """Returns True if your next_move_fcn successfully guides the hunter_bot
    to the target_bot. This function is here to help you understand how we 
    will grade your submission."""
    max_distance = 0.97 * target_bot.distance # 0.97 is an example. It will change.
    separation_tolerance = 0.02 * target_bot.distance # hunter must be within 0.02 step size to catch target
    caught = False
    ctr = 0

    # We will use your next_move_fcn until we catch the target or time expires.
    while not caught and ctr < 1000:

        # Check to see if the hunter has caught the target.
        hunter_position = (hunter_bot.x, hunter_bot.y)
        target_position = (target_bot.x, target_bot.y)
        separation = distance_between(hunter_position, target_position)
        if separation < separation_tolerance:
            print "You got it right! It took you ", ctr, " steps to catch the target."
            caught = True

        # The target broadcasts its noisy measurement
        target_measurement = target_bot.sense()

        # This is where YOUR function will be called.
        turning, distance, OTHER = next_move_fcn(hunter_position, hunter_bot.heading, target_measurement, max_distance, OTHER)
        
        # Don't try to move faster than allowed!
        if distance > max_distance:
            distance = max_distance

        # We move the hunter according to your instructions
        hunter_bot.move(turning, distance)

        # The target continues its (nearly) circular motion.
        target_bot.move_in_circle()

        ctr += 1            
        if ctr >= 1000:
            print "It took too many steps to catch the target."
    return caught

def angle_trunc(a):
    """This maps all angles to a domain of [-pi, pi]"""
    while a < 0.0:
        a += pi * 2
    return ((a + pi) % (pi * 2)) - pi

def get_heading(hunter_position, target_position):
    """Returns the angle, in radians, between the target and hunter positions"""
    hunter_x, hunter_y = hunter_position
    target_x, target_y = target_position
    heading = atan2(target_y - hunter_y, target_x - hunter_x)
    heading = angle_trunc(heading)
    return heading

def naive_next_move(hunter_position, hunter_heading, target_measurement, max_distance, OTHER):
    """This strategy always tries to steer the hunter directly towards where the target last
    said it was and then moves forwards at full speed. This strategy also keeps track of all 
    the target measurements, hunter positions, and hunter headings over time, but it doesn't 
    do anything with that information."""
    if not OTHER: # first time calling this function, set up my OTHER variables.
        measurements = [target_measurement]
        hunter_positions = [hunter_position]
        hunter_headings = [hunter_heading]
        OTHER = (measurements, hunter_positions, hunter_headings) # now I can keep track of history
    else: # not the first time, update my history
        OTHER[0].append(target_measurement)
        OTHER[1].append(hunter_position)
        OTHER[2].append(hunter_heading)
        measurements, hunter_positions, hunter_headings = OTHER # now I can always refer to these variables
    
    heading_to_target = get_heading(hunter_position, target_measurement)
    heading_difference = heading_to_target - hunter_heading
    turning =  heading_difference # turn towards the target
    distance = max_distance # full speed ahead!
    return turning, distance, OTHER

target = robot(0.0, 10.0, 0.0, 2*pi / 30, 1.5)
measurement_noise = 2.0*target.distance # VERY NOISY!!
target.set_noise(0.0, 0.0, measurement_noise)

hunter = robot(-10.0, -10.0, 0.0)

# print demo_grading2(hunter, target, next_move)
print demo_grading(hunter, target, next_move)

