import pandas as pd
import math
import breakdist
import objectFilter
import preprocessing


CAR_WIDTH = 1.7 #m

dataset = preprocessing.load_data('developmentData.csv')


for id, situation in enumerate(dataset):
    print(id)
    if id > 0:
        breakDist = breakdist.calculate_brake_distance(2.5, situation['VehicleSpeed'])
        closest = objectFilter.predictPath(situation, 10, breakDist, situation['dt'], CAR_WIDTH)

        if closest:
            dataset[id]['objects'][closest['name']]['state'] = True
            speedVect = objectFilter.warning(closest)


