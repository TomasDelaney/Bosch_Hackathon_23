import pandas as pd
import math
import breakdist
df = pd.read_csv('developmentData.csv' )
print(df.to_string())

object_params = ['Distance_X', 'Distance_Y', 'Speed_X', 'Speed_Y']


## Collect object names and params from header names
column_names = df.columns.tolist()
object_names = []
object_params = []
for column in column_names:
    if 'Object' in column:
        objEnd = (column.find('Object'))+len('Object')
        object_name = column[:objEnd]
        object_param = column[objEnd:]
        object_params.append(object_param)
        object_names.append(object_name)

object_names = list(set(object_names))
print(object_names)
object_params = list(set(object_params))
print(object_params)

#######
# Turn pandas dataset into a list
# dataset :list
#   data_dict : dictionary
#       Timestamp
#       VehicleSpeed
#       YawRate
#       objects: list
#           object: { 'name', 'status', 'Distance_X', 'Distance_Y', 'Speed_X', 'Speed_Y'}
dataset=[]

"""− ObjectDistances (X,Y) 🡪 divide by 128 🡪 unit will be [m]
− VehicleSpeed 🡪 divide by 256 🡪 unit will be [m/s]
− ObjectSpeeds (X,Y) 🡪 divide by 256 🡪 unit will be [m/s]"""
for index, row in df.iterrows():
    data_dict = {}
    data_dict['Timestamp'] = row['Timestamp']
    data_dict['VehicleSpeed'] = row['VehicleSpeed']/256 # m/s
    data_dict['YawRate'] = row['YawRate'] # Yaw rate radian/sec
    objects = []
    for obj in object_names:
        obj_dict = {'name': obj, 'state': True}
        for param in object_params:
            if 'Distance' in param:
                obj_dict[param] = row[(obj + param)]/128 # m
            elif 'Speed' in param:
                obj_dict[param] = row[(obj + param)]/256 # m/s
            else:
                obj_dict[param] = row[(obj + param)]
        objects.append(obj_dict)
    data_dict['objects'] = objects
    dataset.append(data_dict)

# print(dataset)
def calcNewLoc(x,y,Speed_X, Speed_Y, t, dt, yaw, v):

    alpha = - yaw * dt
    x = x - (v - Speed_X) *t
    y = y + Speed_Y * t
    new_x = math.cos(alpha)*x - math.sin(alpha)*y
    new_y = math.sin(alpha)*x + math.cos(alpha)*y
    return {'x': new_x, 'y': new_y }

CAR_WIDTH = 1.7 #m

def predictPath(situation, time_range , breakDist, dt):
    closest = {'x': 100000, 'y': 1000000, 't': 1000000, 'name':''}
    for obj in situation['objects']:
        done = False
        for t in range(0, time_range * 100, 1):
            t = float(t )/ 100

            if not done:
                if not (obj['Distance_X'] == 0 and obj['Distance_Y']==0):
                    loc = calcNewLoc( x=obj['Distance_X'], y=obj['Distance_Y'],
                                Speed_X= obj['Speed_X'], Speed_Y=obj['Speed_Y'],
                                t=t , dt =dt, yaw = situation["YawRate"], v = situation['VehicleSpeed'])
                    if abs(loc['y']) < CAR_WIDTH /2 and loc['x'] < breakDist * 1.5:
                        done = True
                        if closest['t']>t:
                            closest['x'] = obj['Distance_X']
                            closest['y'] = obj['Distance_Y']
                            closest['t'] = t
                            closest['name'] = obj['name']

                        print(f"Break needed in {t} seconds on object {obj['name']} obj location {obj['Distance_X']}  {obj['Distance_Y']}")

                        print(f"Break needed in {t} seconds on object {obj['name']} obj location {obj['Distance_X']}  {obj['Distance_Y']}")
    if closest['name']!='':
        print(closest['name'], closest['t'])


for id, situation in enumerate(dataset):
    print(id)
    if id>0:
        breakDist = breakdist.calculate_brake_distance(2.5, situation['VehicleSpeed'])
        predictPath(situation, 10, breakDist, situation['Timestamp']-dataset[id-1]['Timestamp'])







