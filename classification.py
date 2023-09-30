import math
import numpy
import numpy as np


def classifySituation(VehicleSpeed, Speed_X, Speed_Y, Yaw):
    ''' Classify warning situations  '''
    car_vec_x = VehicleSpeed
    car_vec_y = 0

    #
    scalar = car_vec_x * Speed_X + car_vec_y * Speed_Y
    cos_alpha = scalar / (VehicleSpeed * math.sqrt(Speed_X ** 2 + Speed_Y ** 2))
    alpha = np.rad2deg(np.arccos(cos_alpha))

    print(alpha)
    print(np.rad2deg(Yaw))

    print('radius', calcTurnRadius(Yaw, VehicleSpeed))
    if calcTurnRadius(Yaw, VehicleSpeed) < 30:
        return 'Turn'
    elif calcTurnRadius(Yaw, VehicleSpeed) < 200:
        if alpha <= 25 or alpha >= 160:
            return 'Parallel'
        elif 75 <= alpha < 115:
            return 'Perpendicular'
        else:
            return 'Turn'
    elif alpha <= 25 or alpha >= 160:
        return 'Parallel'
    elif 75 <= alpha < 115:
        return 'Perpendicular'
    else:
        return 'Unclassified'


def calcTurnRadius(YawRate, VehicleSpeed):
    return VehicleSpeed / YawRate
