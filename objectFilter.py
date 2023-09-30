import math
import breakdist


def calcNewLoc(x, y, Speed_X, Speed_Y, t, dt, yaw, v):
    alpha = - yaw * dt
    x = x - (v - Speed_X) * t
    y = y + Speed_Y * t
    new_x = math.cos(alpha) * x - math.sin(alpha) * y
    new_y = math.sin(alpha) * x + math.cos(alpha) * y
    return {'x': new_x, 'y': new_y}


def predictPath(situation, time_range, break_dist, dt, CAR_WIDTH):
    closest = {'x': 100000, 'y': 1000000, 't': 1000000, 'name': ''}
    for obj in situation['objects']:
        done = False
        for t in range(0, time_range * 100, 1):
            t = float(t) / 100

            if not done:
                if not (obj['Distance_X'] == 0 and obj['Distance_Y'] == 0):
                    loc = calcNewLoc(x=obj['Distance_X'], y=obj['Distance_Y'],
                                     Speed_X=obj['Speed_X'], Speed_Y=obj['Speed_Y'],
                                     t=t, dt=dt, yaw=situation["YawRate"], v=situation['VehicleSpeed'])

                    if abs(loc['y']) < CAR_WIDTH / 2 and loc['x'] < break_dist * 1.5:
                        done = True
                        if closest['t'] > t:
                            closest['x'] = obj['Distance_X']
                            closest['y'] = obj['Distance_Y']
                            closest['t'] = t
                            closest['Speed_x'] = obj['Speed_X']
                            closest['Speed_Y'] = obj['Speed_Y']
                            closest['name'] = obj['name']

                        print(
                            f"Break needed in {t} seconds on object {obj['name']} obj location {obj['Distance_X']}  {obj['Distance_Y']}")

                        print(
                            f"Break needed in {t} seconds on object {obj['name']} obj location {obj['Distance_X']}  {obj['Distance_Y']}")
    if closest['name'] != '':
        return closest


def warning(closest):
    if closest['t'] < 1.5:
        print("*** Flashig lights and sound effects ***")
        return [closest['Speed_X'], closest['Speed_Y']]
    elif closest['t'] < 3:
        print("*** Tactile WARNING ***")
        return [closest['Speed_X'], closest['Speed_Y']]
    else:
        print(f"Possible collision but still {closest['t']} seconds to notice")
        return []


