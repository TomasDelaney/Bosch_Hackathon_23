df = pd.read_csv('developmentData.csv' )
print(df.to_string())
object_names = ['FirstObject', 'SecondObject', 'ThirdObject', 'FourthObject']
object_params = ['Distance_X', 'Distance_Y', 'Speed_X', 'Speed_Y']
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
        obj_dict = {'name': obj}
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



