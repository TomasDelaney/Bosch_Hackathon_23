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

dataset=[]

"""− ObjectDistances (X,Y) 🡪 divide by 128 🡪 unit will be [m]
− VehicleSpeed 🡪 divide by 256 🡪 unit will be [m/s]
− ObjectSpeeds (X,Y) 🡪 divide by 256 🡪 unit will be [m/s]"""
for index, row in df.iterrows():
    data_dict = {}
    data_dict['Timestamp'] = row['Timestamp']
    data_dict['VehicleSpeed'] = row['VehicleSpeed']/256
    data_dict['YawRate'] = row['YawRate']
    objects = []
    for obj in object_names:
        obj_dict = {'name': obj, 'state': True}
        for param in object_params:
            if 'Distance' in param:
                obj_dict[param] = row[(obj + param)]/128
            elif 'Speed' in param:
                obj_dict[param] = row[(obj + param)]/256
            else:
                obj_dict[param] = row[(obj + param)]
        objects.append(obj_dict)
    data_dict['objects'] = objects
    dataset.append(data_dict)

print(dataset)



