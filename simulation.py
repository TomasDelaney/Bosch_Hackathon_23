import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
SIMULATION = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("START SIMULATION")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

TEXT_FONT = pygame.font.SysFont('comicsans', 40)

FPS = 60
VEHICLE_WIDTH = 50
VEHICLE_HEIGHT = 60

BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'asphalt.png')), (WIDTH, HEIGHT))

class Vehicle:
    def __init__(self, vehicle_x=10, vehicle_y=10, rotate=180):
        self.vehicle_x = vehicle_x
        self.vehicle_y = vehicle_y
        self.rotate = rotate
        # draw_vehicle()

    def load_image(self):
        vehicle_image = pygame.image.load(os.path.join('Assets', 'car.png'))
        vehicle = pygame.transform.rotate(pygame.transform.scale(vehicle_image, (VEHICLE_WIDTH, VEHICLE_HEIGHT)), self.rotate)
        return vehicle

    def draw_vehicle(self):
        vehicle = self.load_image()
        car = pygame.Rect(100, 300, VEHICLE_WIDTH, VEHICLE_HEIGHT)
        SIMULATION.blit(vehicle, (car.x, car.y))
        # pygame.display.update()

def draw_window():
    SIMULATION.blit(BACKGROUND, (0,0))

    timestamp_text = TEXT_FONT.render("Timestamp: " + str("T"), 1, WHITE)
    SIMULATION.blit(timestamp_text, (WIDTH - timestamp_text.get_width() - 10, 10))

    vehicle = Vehicle()
    vehicle.draw_vehicle()


def end_simulation(keys_pressed):
    if keys_pressed[pygame.K_ESCAPE]:
        pygame.quit()


def main():
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        keys_pressed = pygame.key.get_pressed()

        end_simulation(keys_pressed)

        draw_window()

        pygame.display.update()

    main()

if __name__ == "__main__":
    main()