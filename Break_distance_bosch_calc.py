# function that calculates the break distance based on the formula given by Bosch

def calculate_brake_distance_bosch(vEgo, t_lat, aEgo, v0):
    # constants
    max_jerk = 30 # m/s^2
    aMax = 9 # m/s^2  maximum deceleration

    # variables: aEgo: acc/dec of the vehicle, vEgo: speed of the vehicle
    t2 = (aMax - aEgo) / max_jerk
    delta_v1 = (max_jerk/2) * (t2**2) + aEgo * t2
    v1 = v0 + delta_v1
    delta_v2 = -v1
    t3 = delta_v2 / aMax

    # break distance parts
    d1 = vEgo * t_lat + (aEgo/2) * (t2**2) + vEgo * t2
    d2 = (max_jerk/6) * (t2**3) + (aEgo/2) * (t2**2) + vEgo * t2
    d3 = (aMax/2) * (t3**2) + v1 * t3

    break_distance = d1 + d2 + d3

    return break_distance