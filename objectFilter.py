import math


def calcNewLoc(x, y, Speed_X, Speed_Y, t, dt, yaw, v):
    '''Calculate future locations of object based on the current properties'''
    alpha = - yaw * t
    x = x - (v - Speed_X) * t
    y = y + Speed_Y * t
    new_x = math.cos(alpha) * x - math.sin(alpha) * y
    new_y = math.sin(alpha) * x + math.cos(alpha) * y
    return {'x': new_x, 'y': new_y}


def filterClosest(situation):
    '''Filter objects based on distance
        return value: index of closest object'''

    p_dist = []  # distance container
    midx = -100;  # index of the relevant object initialization
    for i, obj in enumerate(situation['objects']):
        if obj['Distance_X'] != 0:  # we don't need any data which is 0
            dist = math.sqrt(math.pow(obj['Distance_Y'], 2) + math.pow(obj['Distance_X'], 2))
            p_dist.append(dist)  # add dist to a list
        else:
            p_dist.append(9999)  # if we have 0 x than we give it a big distance, because it a measure error
        midx = p_dist.index(min(p_dist))  # get the index of the min distance
    situation['objects'][midx]['state'] = True  # set it to the relevant objext

    # print(situation['objects'][midx]['name'], situation['objects'][midx]['state'], 'close')

    return midx


def predictPath(situation, time_range, break_dist, dt, CAR_WIDTH):

    closest = {'x': 100000, 'y': 1000000, 't': 1000000, 'name': ''}
    for idx, obj in enumerate(situation['objects']):
        done = False
        for t in range(0, time_range * 100, 1):
            t = float(t) / 100

            if not done:
                if not (obj['Distance_X'] == 0): # if tracking data exists
                    #calculate
                    loc = calcNewLoc(x=obj['Distance_X'], y=obj['Distance_Y'],
                                     Speed_X=obj['Speed_X'], Speed_Y=obj['Speed_Y'],
                                     t=t, dt=dt, yaw=situation["YawRate"], v=situation['VehicleSpeed'])

                    if abs(loc['y']) < CAR_WIDTH / 2 and loc['x'] < break_dist * 1.5:
                        '''if future location is in front of the car 
                            and predicted distance is under 1.5 of breakdistance '''
                        if closest['t'] > t:
                            closest['x'] = obj['Distance_X']
                            closest['y'] = obj['Distance_Y']
                            closest['t'] = t
                            closest['Speed_X'] = obj['Speed_X']
                            closest['Speed_Y'] = obj['Speed_Y']
                            closest['name'] = obj['name']
                            closest['idx'] = idx
    if closest['name'] != '':
        return closest


def warning(closest):
    if 1.5 <= closest['t'] < 3:
        print("*** Tactile WARNING ***", closest['name'])
        print(f"Possible collision {closest['t']} seconds to notice", closest['name'])

        return {'warning': 'Tactile warning', 'x': closest['Speed_X'], 'y': closest['Speed_Y']}
    elif closest['t'] < 1.5:
        print("*** Tactile WARNING ***")
        print("*** Flashig lights and horn effects ***", closest['name'])
        print(f"Possible collision {closest['t']} seconds to notice", closest['name'])

        return {'warning': 'Tactile & sound warning', 'x': closest['Speed_X'], 'y': closest['Speed_Y']}
    elif closest['t'] < 0.2:
        print("*** EMERGENCY BREAK ***", closest['name'])
        print(f"Possible collision {closest['t']} seconds to notice", closest['name'])
        return {'warning': 'Emergency break', 'x': closest['Speed_X'], 'y': closest['Speed_Y']}
    else:
        print(f"Possible collision danger {closest['t']} seconds to notice", closest['name'])
        return {'warning': 'Not dangerous'}
