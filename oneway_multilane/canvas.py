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
                                                  0, 32)
        self.road_image = pygame.image.load('roadtexture.jpg')
        self.scaled_road_image = pygame.transform.scale(self.road_image,
                                                        (20, 6))
        self.car_image = pygame.image.load('car.png')

    def draw_vehicle(self, vehicle, edge):
        x_scale = self.screen.get_width() / edge.locations[1][0]
        road_pos_ratio = vehicle.location / edge.edgesize

        edge_x = int((edge.locations[1][0] - edge.locations[0][0])
                     * road_pos_ratio + edge.locations[0][0])
        edge_y = int((edge.locations[1][1] - edge.locations[0][1])
                     * road_pos_ratio + edge.locations[0][1])

        scaled_x_loc, scaled_y_loc = self.scale_to_screen(edge, edge_x, edge_y)
        vehicle_screen_xsize = int(vehicle.length * x_scale)
        vehicle_screen_ysize = 2 * x_scale

        scaled_car = pygame.transform.scale(self.car_image,
                                            (vehicle_screen_xsize,
                                             vehicle_screen_ysize))
        self.screen.blit(scaled_car,
                         (scaled_x_loc - int(vehicle_screen_xsize / 2.),
                          scaled_y_loc - vehicle_screen_ysize))

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
                                     edge.locations[0][1] -
                              self.scaled_road_image.get_height() / 2.)))

    def clear_screen(self, color):
        self.screen.fill(color)

    def update_screen(self):
        pygame.display.update()
