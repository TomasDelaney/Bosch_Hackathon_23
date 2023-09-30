import pandas as pd
import math
import Break_distance_bosch_calc
import classification
import objectFilter
import preprocessing

CAR_WIDTH = 1.7 #m
INPUT_FILE = 'developmentData.csv'
dataset = preprocessing.load_data(INPUT_FILE)

filteredObjects = []

WARNING_LIST = [ 'Not dangerous', ' *** TACTILE WARNING *** ', ' *** TACTILE & SOUND & FLASHING LIGHTS WARNING *** ', ' *** EMERGENCY BREAK *** ']
WARNING_DICT = {'Not dangerous': 0, 'Tactile warning': 1, 'Tactile & sound warning': 2, 'Emergency break':3}
warnings_timestamped = []
classifydict = dict(  Paraleel=0, Perpendicular=0, Turn=0, Unclassified=0)

for id, situation in enumerate(dataset):
    if id > 0:
        breakDist = breakdist.calculate_brake_distance(2.5, situation['VehicleSpeed'])

        closest = objectFilter.predictPath(situation, 10, breakDist, situation['dt'], CAR_WIDTH)

        # slect imprtant object ->
        #   the closest object from predicted path or if nothing in predicted path the closest object
        if closest:
            filtered = closest['idx']
            speedVect = objectFilter.warning(closest)

            if speedVect['warning'] != 'Not dangerous':
                '''if warning exists for object store it and classify the sitation'''
                warnings_timestamped.append( {'Timestamp': situation['Timestamp'], 'status': WARNING_DICT[speedVect['warning']], 'object_id': closest['idx']} )
                sitName = classification.classifySituation(situation['VehicleSpeed'], closest['Speed_X'], closest['Speed_Y'], situation['YawRate']*situation['dt'])
                print(sitName)
                if sitName in classifydict:
                    classifydict[sitName] = classifydict[sitName]+1
                else:
                    classifydict[sitName] = 1

                if sitName == "Turn":
                    print('Calculated radius ', classification.calcTurnRadius(situation['YawRate'], situation['VehicleSpeed']))
        else:
            filtered = objectFilter.filterClosest(situation)

        dataset[id]['objects'][filtered]['state'] = True
        obj = dataset[id]['objects'][filtered]

        filteredObjects.append(obj)


'''Add warnings with timestamps to the csv file'''
#print(warnings_timestamped)

# Load the CSV data into a DataFrame
df = pd.read_csv(INPUT_FILE)

#print(df.to_string())
warning_df = pd.DataFrame.from_dict(warnings_timestamped)
merged_df = pd.merge(df, warning_df, on='Timestamp', how='left').fillna(0)
#print(merged_df.to_string())# Write the updated DataFrame back to a CSV file
merged_df.to_csv('status'+INPUT_FILE, index=False)

'''Type of situation'''
#print(classifydict)
print(f'Type of situation: {max(classifydict, key=classifydict.get)}')
