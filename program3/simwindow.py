import pygame
import math
from pygame.locals import *

from program3.core import Core


class SimWindow(object):
    def __init__(self, logic):
        pygame.init()

        self.logic = Core()
        #  TEMP
        self.logic.read_file('inputs/testsize.data')

        #  Sizes
        self.width = 800
        self.height = 600
        self.shape_size = 60

        #  Colors
        self.resource_color = (109, 209, 224)
        self.process_color = (137, 237, 104)
        self.black = (0, 0, 0)
        self.red = (244, 44, 44)

        #  Screen logistics...
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill((255, 255, 255))

        #  Store location of each process and resource in x,y plane.
        self.location_r = []
        self.location_p = []

        #  Initialize the surface with processes and resources.
        self.draw_resource_process()
        self.draw_arrow((400, 500), (50,90))

    def loop(self):
        #  Keeps main loop running.
        running = True
        #  Main loop for pygame.
        while running:
            #  For loop through the event queue.
            for event in pygame.event.get():
                #  KEYDOWN is a constant from pygame.locals
                if event.type == KEYDOWN:
                    #  If the ESC key has be pressed, exit.
                    if event.key == K_ESCAPE:
                        running = False
                #  If the window was closed, exit.
                elif event.type == QUIT:
                    running = False
            #  Draw current state.
            self.render()

    def render(self):
        pygame.display.update()

    def draw_arrow(self, start, end):
        pygame.draw.line(self.screen, self.black, start, end, 3)
        rotation = math.degrees(math.atan2(start[1] - end[1], end[0] - start[0])) + 90
        pygame.draw.polygon(self.screen, (255, 0, 0), (
            (end[0] + 20 * math.sin(math.radians(rotation)), end[1] + 20 * math.cos(math.radians(rotation))),
            (end[0] + 20 * math.sin(math.radians(rotation - 120)), end[1] + 20 * math.cos(math.radians(rotation - 120))),
            (end[0] + 20 * math.sin(math.radians(rotation + 120)), end[1] + 20 * math.cos(math.radians(rotation + 120)))))

    def draw_resource_process(self):
        num_r = self.logic.get_resources()
        num_p = self.logic.get_processes()
        #  Draw resources
        for i in range(1, num_r + 1):
            pygame.draw.rect(
                self.screen,
                self.resource_color,
                (int(i * (self.width / (num_r + 1)) - (self.shape_size / 2)),
                 self.shape_size, self.shape_size,
                 self.shape_size))
            self.location_r.append((int(i * (self.width / (num_r + 1)) - (self.shape_size / 2)), self.shape_size))
        #  Draw processes
        for i in range(1, num_p + 1):
            pygame.draw.circle(
                self.screen,
                self.process_color,
                (int(i * (self.width / (num_p + 1))), 500), int(self.shape_size / 2))
            self.location_p.append((int(i * (self.width / (num_p + 1))), 500))