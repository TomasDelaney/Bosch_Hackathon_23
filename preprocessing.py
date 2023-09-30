import pandas as pd
import classification
import objectFilter
from functional_layer import Break_distance_bosch_calc as breakdist


def load_data(filepath):
    df = pd.read_csv(filepath)
    column_names = df.columns.tolist()
    object_names = []
    for column in column_names:
        if 'Object' in column:
            objEnd = (column.find('Object')) + len('Object')
            object_name = column[:objEnd]
            object_names.append(object_name)

    object_names = list(dict.fromkeys(object_names))
    print(object_names)
    object_params = ['Distance_X', 'Distance_Y', 'Speed_X', 'Speed_Y']

    # print(object_params)
    number_of_objects = len(object_names)

    object_params = ['Distance_X', 'Distance_Y', 'Speed_X', 'Speed_Y']
    dataset = []

    """− ObjectDistances (X,Y) 🡪 divide by 128 🡪 unit will be [m]
    − VehicleSpeed 🡪 divide by 256 🡪 unit will be [m/s]
    − ObjectSpeeds (X,Y) 🡪 divide by 256 🡪 unit will be [m/s]"""
    for index, row in df.iterrows():
        # load and normalize data into a list of dictionaries
        data_dict = {'Timestamp': row['Timestamp'],
                     'VehicleSpeed': row['VehicleSpeed'] / 256,
                     'YawRate': row['YawRate']}
        if index > 0:
            data_dict['dt'] = data_dict['Timestamp'] - prev_t
        prev_t = data_dict['Timestamp']

        objects = []
        for obj in object_names:
            obj_dict = {'name': obj}
            for param in object_params:
                if 'Distance' in param:
                    obj_dict[param] = row[(obj + param)] / 128
                elif 'Speed' in param:
                    obj_dict[param] = row[(obj + param)] / 256
                else:
                    obj_dict[param] = row[(obj + param)]
            objects.append(obj_dict)
        data_dict['objects'] = objects
        dataset.append(data_dict)

    return dataset

