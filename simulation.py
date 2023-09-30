import pygame
import os
import pandas as pd
import numpy as np
import math

# initializing BEGINNING

pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1000, 800

SIMULATION = pygame.display.set_mode((WIDTH, HEIGHT))
display_surface = pygame.display.get_surface()
SIMULATION.blit(pygame.transform.flip(SIMULATION, False, True), dest=(0, 0))

WARNING_LIST = ['NOT DANGEROUS', 'TACTILE WARNING', 'TACTILE & SOUND WARNING', 'EMERGENCY BREAK']
dataset = []
objects_dataset = []

Status = []
Timestamps = []
YawRates = []
VehicleSpeed = []

TEXT_FONT = pygame.font.SysFont('arial', 30)
WARNING_TEXT_FONT = pygame.font.SysFont('arial', 50)

FPS = 60
VEHICLE_WIDTH = 100
VEHICLE_HEIGHT = 50
OBJECT_WIDTH = 16
OBJECT_HEIGHT = 16

BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'asphalt.png')), (WIDTH, HEIGHT))


# initializing END

# Movement of vehicle and rotation class:
class Vehicle:
    # class initialisation
    def __init__(self, vehicle_x=0, vehicle_y=int(HEIGHT / 2 - VEHICLE_WIDTH / 2), rotate=0, vehicle_front_x=0,
                 vehicle_front_y=0):
        self.vehicle_x = vehicle_x
        self.vehicle_y = vehicle_y
        self.vehicle_front_x = VEHICLE_WIDTH
        self.vehicle_front_y = VEHICLE_HEIGHT / 2
        self.rotate = rotate

    # vehicle rotation
    def rotate_vehicle(self, rotate):
        self.rotate = rotate

    # vehicle movement
    def move(self, speed_x, speed_y, rotate):
        self.vehicle_x += speed_x * math.cos(rotate)
        self.vehicle_y -= speed_y * 20 * math.sin(rotate)
        self.vehicle_front_x = VEHICLE_WIDTH * math.cos(rotate) - (VEHICLE_HEIGHT / 2) * math.sin(rotate) + self.vehicle_x
        self.vehicle_front_y = -(VEHICLE_WIDTH * math.sin(rotate) + (VEHICLE_HEIGHT / 2) * math.cos(rotate)) + self.vehicle_y


    # car picture loading and rotation
    def load_image(self, vehicle_image):
        vehicle = pygame.transform.rotate(pygame.transform.scale(vehicle_image, (VEHICLE_WIDTH, VEHICLE_HEIGHT)), np.rad2deg(self.rotate))
        return vehicle

    # vehicle drawing
    def draw_vehicle(self, vehicle_image):
        vehicle = self.load_image(vehicle_image)
        car = pygame.Rect(self.vehicle_x, self.vehicle_y, VEHICLE_WIDTH, VEHICLE_HEIGHT)
        SIMULATION.blit(vehicle, (car.x, car.y))

    # getter functions:
    def get_vehicle_coords(self):
        return self.vehicle_x, self.vehicle_y

    def get_vehicle_front_coords(self):
        return self.vehicle_front_x, self.vehicle_front_y


# class for detected objects:
class Object:
    # class initialisation
    def __init__(self, name="Object", distance_x=0, distance_y=0, object_width=16, object_height=16):
        self.name = name
        self.distance_x = distance_x
        self.distance_y = distance_y
        self.object_width = object_width
        self.object_height = object_height

    # object movement realtive to the front of the car
    def move(self, car_front_x, car_front_y, angle, new_x, new_y):
        self.distance_x = int(car_front_x + new_x * math.cos(angle) - new_y * math.sin(angle))
        self.distance_y = int(car_front_y + new_x * math.sin(angle) + new_y * math.cos(angle))

    # object image loading
    def load_image(self, object_image):
        object = pygame.transform.rotate(pygame.transform.scale(object_image, (self.object_width, self.object_width)),
                                         0)
        return object

    # object drawing
    def draw_object(self, object_image):
        object = self.load_image(object_image)
        obj = pygame.Rect(self.distance_x, self.distance_y, self.object_width, self.object_height)
        SIMULATION.blit(object, (obj.x, obj.y))


# pygame base window visualisation /w timestamp and step#
def draw_window(timestamp=0, index=0):
    SIMULATION.blit(BACKGROUND, (0, 0))
    timestamp_text = TEXT_FONT.render("Timestamp: " + str(timestamp) + "  Index: " + str(index), 1, (255, 255, 255))
    SIMULATION.blit(timestamp_text, (WIDTH - 500, 10))


# pygame warning visualisation
def draw_warning(index=0,ObjectName = 'name'):
    position = 100

    if ObjectName == 'FirstObject':
        position = 100
    elif ObjectName == 'SecondObject':
        position = 150
    elif ObjectName == 'ThirdObject':
        position = 200
    elif ObjectName == 'FourthObject':
        position = 250

    if index == 0:
        warning_text = WARNING_TEXT_FONT.render(str(WARNING_LIST[index]), 1, (0, 255, 0))
        SIMULATION.blit(warning_text, (50, HEIGHT - position))
    elif index == 1:
        warning_text = WARNING_TEXT_FONT.render(str(WARNING_LIST[index]), 1, (255, 100, 100))
        SIMULATION.blit(warning_text, (50, HEIGHT - position))
    elif index == 2:
        warning_text = WARNING_TEXT_FONT.render(str(WARNING_LIST[index]), 1, (255, 50, 50))
        SIMULATION.blit(warning_text, (50, HEIGHT - position))
    elif index == 3:
        warning_text = WARNING_TEXT_FONT.render(str(WARNING_LIST[index]), 1, (255, 0, 0))
        SIMULATION.blit(warning_text, (50, HEIGHT - position))


# end sim
def end_simulation(keys_pressed):
    if keys_pressed[pygame.K_ESCAPE]:
        pygame.quit()


# data loader function /w scaling
def load_data():
    df = pd.read_csv(os.path.join('statusdevelopmentData.csv'))

    ## Collect object names and params from header names
    column_names = df.columns.tolist()
    object_names = []
    for column in column_names:
        if 'Object' in column:
            objEnd = (column.find('Object')) + len('Object')
            object_name = column[:objEnd]
            object_names.append(object_name)

    object_names = list(dict.fromkeys(object_names))
    object_params = ['Distance_X', 'Distance_Y', 'Speed_X', 'Speed_Y']

    number_of_objects = len(object_names)

    """− ObjectDistances (X,Y) 🡪 divide by 128 🡪 unit will be [m]
    − VehicleSpeed 🡪 divide by 256 🡪 unit will be [m/s]
    − ObjectSpeeds (X,Y) 🡪 divide by 256 🡪 unit will be [m/s]"""
    for index, row in df.iterrows():
        data_dict = {}
        data_dict['Timestamp'] = row['Timestamp']
        data_dict['VehicleSpeed'] = row['VehicleSpeed'] / 256 * 7
        data_dict['YawRate'] = row['YawRate']
        data_dict['status'] = row['status']

        Status.append(row['status'])
        Timestamps.append(row['Timestamp'])
        VehicleSpeed.append(float(row['VehicleSpeed']) / 256 * 7)
        if (row['YawRate'] == '0'):
            YawRates.append(float(row['YawRate']))
        else:
            YawRates.append(float(row['YawRate']))
        objects = []

        for obj in object_names:
            obj_dict = {'name': obj}
            for param in object_params:
                if 'Distance' in param:
                    obj_dict[param] = row[(obj + param)] / 128 * 7
                elif 'Speed' in param:
                    obj_dict[param] = row[(obj + param)] / 256 * 7
                else:
                    obj_dict[param] = row[(obj + param)]
            objects.append(obj_dict)
        data_dict['objects'] = objects
        dataset.append(data_dict)

    for obj in object_names:
        object_coord = []
        for element in dataset:  # an element in a list of dictionaries, so an element is a dictionary
            coord = []
            for instance in element['objects']:
                if instance['name'] == obj:
                    coord = (
                        obj, instance['Distance_X'], instance['Distance_Y'], instance['Speed_X'], instance['Speed_Y'])
                    object_coord.append(coord)
        objects_dataset.append(object_coord)

    return number_of_objects


def main():
    number_of_objects = load_data()
    clock = pygame.time.Clock()
    run = True
    # initialising/loading data BEGINNING

    vehicle_image = pygame.image.load(os.path.join('Assets', 'car.png'))
    object_image_green = pygame.image.load(os.path.join('Assets', 'object_green.png'))
    object_image_black = pygame.image.load(os.path.join('Assets', 'object.png'))
    object_image_red = pygame.image.load(os.path.join('Assets', 'object_red.png'))

    timestamp = Timestamps[0]
    rotate = YawRates[0]
    rotate_object = YawRates[0]

    draw_window(timestamp)
    # initialising/loading data END
    # vehicle and object loading (NOTE: this could be sequencialised, we had limited time)
    vehicle = Vehicle(rotate=rotate)
    vehicle.draw_vehicle(vehicle_image)

    FirstObject = Object()
    FirstObject.draw_object(object_image_green)

    SecondObject = Object()
    SecondObject.draw_object(object_image_black)

    ThirdObject = Object()
    ThirdObject.draw_object(object_image_black)

    FourthObject = Object()
    FourthObject.draw_object(object_image_black)

    index = 0
    max_index = len(Timestamps) - 1
    while run:
        # failsafe: make run false -> program stops
        clock.tick(FPS)
        pygame.init()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        # failsafe
        keys_pressed = pygame.key.get_pressed()
        end_simulation(keys_pressed)

        if index > max_index:
            # index = 0
            run = False
            pygame.quit()
            exit(0)

        timestamp = Timestamps[index]
        speed_x = 0
        speed_y = 0

        if index > 0:
            dt = float(Timestamps[index]) - float(Timestamps[index - 1])

            # rotation and placement of vehicle based on dataset
            rotate += YawRates[index - 1] * dt
            rotate_object = YawRates[index - 1] * dt

            speed_x = VehicleSpeed[index - 1] * dt
            speed_y = VehicleSpeed[index - 1] * dt

            vehicle_x, vehicle_y = vehicle.get_vehicle_coords()
            # we need to differentiate about the vehicle's center and it's front camera
            car_front_x, car_front_y = vehicle.get_vehicle_front_coords()

            # position of objects relative to car
            new_x_first = objects_dataset[0][index][1]
            new_y_first = objects_dataset[0][index][2]

            new_x_second = objects_dataset[1][index][1]
            new_y_second = objects_dataset[1][index][2]

            new_x_third = objects_dataset[2][index][1]
            new_y_third = objects_dataset[2][index][2]

            new_x_fourth = objects_dataset[3][index][1]
            new_y_fourth = objects_dataset[3][index][2]

            # rotation of objects relative to car
            if (new_x_first != 0 and new_y_first != 0):
                FirstObject.move(car_front_x, car_front_y, -rotate, new_x_first, -new_y_first)

            if (new_x_second != 0 and new_y_second != 0):
                SecondObject.move(car_front_x, car_front_y, -rotate, new_x_second, -new_y_second)

            if (new_x_third != 0 and new_y_third != 0):
                ThirdObject.move(car_front_x, car_front_y, -rotate, new_x_third, -new_y_third)

            if (new_x_fourth != 0 and new_y_fourth != 0):
                FourthObject.move(car_front_x, car_front_y, -rotate, new_x_fourth, -new_y_fourth)

        # visualisation:
        draw_window(timestamp, index)

        if VehicleSpeed[index - 1] != 0:
            vehicle.rotate_vehicle(rotate)

        vehicle.move(speed_x, speed_y, rotate_object)
        vehicle.draw_vehicle(vehicle_image)

        # Checking if danger of collision has been detected
        state_FirstObject = int(Status[index])

        if state_FirstObject == 0:
            FirstObject.draw_object(object_image_green)
            draw_warning(state_FirstObject, 'FirstObject')
        else:
            FirstObject.draw_object(object_image_red)
            draw_warning(state_FirstObject, 'FirstObject')

        SecondObject.draw_object(object_image_black)
        ThirdObject.draw_object(object_image_black)
        FourthObject.draw_object(object_image_black)

        pygame.display.update()
        pygame.time.wait(15)

        # ending
        index += 1

    main()


if __name__ == "__main__":
    main()
