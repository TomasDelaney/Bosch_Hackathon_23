# -*- coding: utf-8 -*-
"""Classification

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DDnAaHhgFbqF10znrJtRTmuRTPLUwTBc
"""

def classification(vector_obj):
    vector_car=[1, 0];
    up=vector_obj[0]*vector_car[0]+vector_obj[1]*vector_car[1]
    down=math.sqrt(math.pow(vector_car[0],2)+math.pow(vector_car[1],2))*math.sqrt(math.pow(vector_obj[0],2)+math.pow(vector_obj[1],2))
    scalarp=math.acos(up/down)*180/math.pi
    vec_p=math.asin(np.cross(vector_car, vector_obj)/down)*180/math.pi
    #if a kanyarodós az nincs implementálva
    if scalarp>=90 & scalarp<=120:
        print("The car is perpendicular to the object")
    elif vec_p>=0 & vec_p<=20:
         print("Parallel the car to the object")