import pygame


class Canvas:
    white = (255, 255, 255)

    def __init__(self):
        # set up pygame
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))

        # set up the window
        modes = pygame.display.list_modes(32)
        if not modes:
            return
        else:
            self.screen = pygame.display.set_mode(modes[0],
                                                  pygame.FULLSCREEN, 32)
        self.road_image = pygame.image.load('roadtexture.jpg')
        self.scaled_road_image = pygame.transform.scale(self.road_image,
                                                        (20, 20))
        self.car_image = pygame.image.load('car.png')

    def draw_vehicle(self, vehicle, edge):
        ratio = vehicle.location / edge.edgesize

        edge_x = int((edge.locations[1][0] - edge.locations[0][0]) * ratio +
                     edge.locations[0][0])
        edge_y = int((edge.locations[1][1] - edge.locations[0][1]) * ratio +
                     edge.locations[0][1])

        scaled_x, scaled_y = self.scale_to_screen(edge, edge_x, edge_y)
        x_scale = self.screen.get_width() / edge.locations[1][0]
        scaled_car = pygame.transform.scale(self.car_image,
                                            (int(vehicle.length * x_scale),
                                                2 * x_scale))
        self.screen.blit(scaled_car, (scaled_x, scaled_y))

    def scale_to_screen(self, edge, x, y):
        scaled_x = int(x * (self.screen.get_width() /
                            float(edge.locations[1][0] -
                                  edge.locations[0][0])))
        scaled_y = int(self.screen.get_height() / 2.) + y

        return scaled_x, scaled_y

    def draw_edge(self, edge):
        scaled_road_x = \
            int(edge.locations[1][0] * (self.screen.get_width() /
                                        float(edge.locations[1][0] -
                                              edge.locations[0][0])))
        for i in range(0, scaled_road_x, self.scaled_road_image.get_width()):
            self.screen.blit(self.scaled_road_image,
                             (i, int(self.screen.get_height() / 2. +
                                     edge.locations[0][1]) -
                              self.scaled_road_image.get_height() / 2. + 5))

    def clear_screen(self, color):
        self.screen.fill(color)

    def update_screen(self):
        pygame.display.update()
