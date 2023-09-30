# function that calculates the break distance based on the formula given by Bosch

def calculate_brake_distance_bosch(vEgo, t_lat, aEgo, v0):
    # constants
    max_jerk = 30  # m/s^2
    aMax = 9  # m/s^2  maximum deceleration

    # variables: aEgo: acc/dec of the vehicle, vEgo: speed of the vehicle
    t2 = (aMax - aEgo) / max_jerk
    delta_v1 = (max_jerk / 2) * (t2 ** 2) + aEgo * t2
    v1 = v0 + delta_v1
    delta_v2 = -v1
    t3 = delta_v2 / aMax

    # break distance parts
    d1 = vEgo * t_lat + (aEgo / 2) * (t2 ** 2) + vEgo * t2
    d2 = (max_jerk / 6) * (t2 ** 3) + (aEgo / 2) * (t2 ** 2) + vEgo * t2
    d3 = (aMax / 2) * (t3 ** 2) + v1 * t3

    break_distance = d1 + d2 + d3

    return break_distance


'''## Break Distance calculation
The AASHTO stopping distance formula is as follows:

s = (0.278 × t × v) + v² / (254 × (f + G))

where:

s – Stopping distance in meters;
t – Perception-reaction time in seconds;
v – Speed of the car in km/h;
G – Grade (slope) of the road, expressed as a decimal. Positive for an uphill grade and negative for a downhill road; and
f – Coefficient of friction between the tires and the road. It is assumed to be 0.7 on a dry road and between 0.3 and 0.4 on a wet road.
This formula is taken from the book "A Policy on Geometric Design of Highways and Streets". It is commonly used in road design for establishing the minimum stopping sight distance required on a given road. With correct parameters, it's a perfect equation for the accurate calculation of the stopping distance of your car. Clearly, it's different than the typical formula used in the speed calculator.

[https://www.omnicalculator.com/physics/stopping-distance](https://www.omnicalculator.com/physics/stopping-distance)'''


def calculate_brake_distance(t_reaction, v_ms):
    G = 0  # Grade(slope) of the road, expressed as a decimal.
    # Positive for an uphill grade and negative for a downhill road
    f = 0.7  # Coefficient of friction between the tires and the road.
    # It is assumed to be 0.7 on a dry road and between 0.3 and 0.4 on a wet road.
    v_kmh = v_ms * 3.6;
    break_dist = ((0.278 * t_reaction * v_kmh) + v_kmh * v_kmh) / (254 * (f + G))

    return break_dist
