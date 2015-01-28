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

    def draw_vehicle(self, vehicle, edge, startloc=0, endloc=-1):
        if(endloc == -1):
            endloc = self.max_edge
        if(startloc > vehicle.location or endloc < vehicle.location):
            return

        x_scale = self.screen.get_width() / (endloc - startloc)
        road_pos_ratio = vehicle.location / edge.edgesize

        edge_x = int((edge.locations[1][0] - edge.locations[0][0])
                     * road_pos_ratio + edge.locations[0][0])
        edge_y = int((edge.locations[1][1] - edge.locations[0][1])
                     * road_pos_ratio + edge.locations[0][1])

        vehicle_screen_xsize = int(vehicle.length * x_scale)
        vehicle_screen_ysize = int(2 * x_scale)

        scaled_car = pygame.transform.scale(self.car_image,
                                            (vehicle_screen_xsize,
                                             vehicle_screen_ysize))

        screen_x = int((edge_x - startloc) * x_scale)
        screen_y = int((self.screen.get_height() / 2.) + edge_y)

        self.screen.blit(scaled_car,
                         (screen_x - int(vehicle_screen_xsize / 2.),
                          screen_y - vehicle_screen_ysize))

    def draw_edge(self, edge, startloc=0, endloc=-1):
        if endloc == -1:
            endloc = edge.edgesize

        # start position on screen.
        startx = 0
        # End pos of the road on the screen
        scaled_road_x = int((self.screen.get_width() / (endloc - startloc))
                            * endloc - startloc)

        for wall in edge.walls:
            if wall[0] < endloc:
                # End pos of the road on the screen
                scaled_road_x = int((self.screen.get_width() /
                                     (endloc - startloc)) *
                                    (wall[0] - startloc))

        for i in range(startx, startx + scaled_road_x,
                       self.scaled_road_image.get_width()):
            self.screen.blit(self.scaled_road_image,
                             (i, int(self.screen.get_height() / 2. +
                                     edge.locations[0][1] -
                              self.scaled_road_image.get_height() / 2.)))

    def clear_screen(self, color):
        self.screen.fill(color)

    def update_screen(self):
        pygame.display.update()
