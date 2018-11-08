import pygame
import math
from pygame.locals import *

from program3.helpers.button import Button

import tkinter as tk
from tkinter import filedialog


class SimWindow(object):
    def __init__(self, logic):
        """
        Initialize the window variables and GUI.
        :param logic: core logic.
        """

        #  Use tkinter for the load function.
        root = tk.Tk()
        root.withdraw()

        #  Initialize pygame and copy over logic object.
        pygame.init()
        pygame.display.set_caption('Resource Manager Sim')
        self.logic = logic

        #  Sizes and positions
        self.width = 1100
        self.height = 600
        self.menu_width = 300
        self.shape_size = 60

        #  Colors
        self.resource_color = (109, 209, 224)
        self.process_color = (137, 237, 104)
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.dark_blue = (33, 123, 165)
        self.dark_green = (74, 165, 74)
        self.light_grey = (232, 232, 232)
        self.red = (255, 0, 0)
        self.dark_grey = (130, 130, 130)

        #  Fonts
        self.font_pr = pygame.font.Font('program3/assets/AsapCondensed-Bold.ttf', 35)
        self.font_menu = pygame.font.Font('program3/assets/AsapCondensed-Regular.ttf', 24)
        self.font_menu_b = pygame.font.Font('program3/assets/AsapCondensed-Bold.ttf', 30)

        #  Screen and other logistics...
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill(self.white)
        self.screen_rect = self.screen.get_rect()

        #  Menu Stuff
        self.menu = pygame.Surface((self.menu_width, self.height))
        self.menu.fill(self.light_grey)
        self.screen.blit(self.menu, (self.width - self.menu_width, 0))
        pygame.draw.line(self.screen, self.dark_grey, (800, 0), (800, 600), 1)

        #  Initial text.
        self.status_text1 = self.font_menu.render("Load file to start simulation.", False, self.black)
        self.screen.blit(self.status_text1, (820, 60))
        self.status_text2 = self.font_menu.render(" ", False, self.black)
        self.screen.blit(self.status_text2, (820, 85))

        #  Store location of each process and resource in x,y plane.
        self.location_r = []
        self.location_p = []

        #  Initialize the surface with processes and resources.
        self.button_load = Button((850, 500, 200, 50), self.dark_grey, self.load, text="Load")
        self.button_next = Button((850, 300, 200, 50), self.dark_grey, self.step_forward, text="Step Forward")
        self.button_reset = Button((850, 400, 200, 50), self.dark_grey, self.reset, text="Reset")

        #  Update display.
        pygame.display.update()

        self.button_load.update(self.screen)
        self.button_next.update(self.screen)
        self.button_reset.update(self.screen)

    def load(self):
        """
        Load file and initialize game state.
        """

        #  Reset location r and p in case of new load.
        self.location_r = []
        self.location_p = []

        #  Load and initialize new state.
        file_path = filedialog.askopenfilename()

        self.logic.reset()
        self.logic.read_file(file_path)
        self.logic.init_state()

        #  Render core GUI pieces.
        self.render_main()

        self.status_text1 = self.font_menu.render("Step forward to start.", False, self.black)
        self.screen.blit(self.status_text1, (820, 60))
        self.status_text2 = self.font_menu.render(" ", False, self.black)
        self.screen.blit(self.status_text2, (820, 85))

        pygame.display.update()

    def reset(self):
        """
        Reset back to beginning state.
        """

        #  Reset core logic back to beginning.
        self.logic.reset()
        self.logic.init_state()

        #  Render core GUI pieces.
        self.render_main()

        self.status_text1 = self.font_menu.render("Step forward to start.", False, self.black)
        self.screen.blit(self.status_text1, (820, 60))
        self.status_text2 = self.font_menu.render(" ", False, self.black)
        self.screen.blit(self.status_text2, (820, 85))

        pygame.display.update()

    def loop(self):
        """
        Main loop for GUI.
        """

        running = True
        while running:
            #  For loop through the event queue.
            for event in pygame.event.get():
                #  Check if button was clicked.
                self.button_load.check_event(event)
                self.button_next.check_event(event)
                self.button_reset.check_event(event)
                #  KEYDOWN is a constant from pygame.locals
                if event.type == KEYDOWN:
                    #  If the ESC key has be pressed, exit.
                    if event.key == K_ESCAPE:
                        running = False
                    elif event.key == K_SPACE:
                        self.step_forward()
                #  If the window was closed, exit.
                elif event.type == QUIT:
                    running = False
            #  Draw current state.
            pygame.display.update()

    def render_main(self):
        """
        Main GUI render helper function.
        """

        #  Reset/clear the canvas.
        self.screen.fill(self.white)
        self.menu.fill(self.light_grey)
        self.screen.blit(self.menu, (self.width - self.menu_width, 0))
        pygame.draw.line(self.screen, self.dark_grey, (800, 0), (800, 600), 1)

        self.draw_resource_process()

        self.button_load.update(self.screen)
        self.button_next.update(self.screen)
        self.button_reset.update(self.screen)

    def draw_arrow(self, start, end, edge_type):
        """
        Draw an arrow from start to end.
        :param start: (x,y) tuple representing start of the arrow.
        :param end: (x,y) tuple representing end of the arrow (where it points).
        :param edge_type: string type of edge that determines color.
        """

        #  Check for the color of the arrow.
        edge_color = self.black
        if edge_type == "HOLD":
            edge_color = self.process_color
        elif edge_type == "REQUEST":
            edge_color = self.resource_color
        elif edge_type == "DEADLOCK":
            edge_color = self.red

        #  Draw arrow with a little bit of math.
        pygame.draw.line(self.screen, edge_color, start, end, 3)
        rotation = math.degrees(math.atan2(start[1] - end[1], end[0] - start[0])) + 90
        pygame.draw.polygon(self.screen, edge_color, (
            (end[0] + 20 * math.sin(math.radians(rotation)),
             end[1] + 20 * math.cos(math.radians(rotation))),
            (end[0] + 20 * math.sin(math.radians(rotation - 120)),
             end[1] + 20 * math.cos(math.radians(rotation - 120))),
            (end[0] + 20 * math.sin(math.radians(rotation + 120)),
             end[1] + 20 * math.cos(math.radians(rotation + 120)))))

    def draw_resource_process(self):
        """
        Render the resources and processes on the screen.
        """

        #  Number of resources and processes.
        num_r = self.logic.get_resources()
        num_p = self.logic.get_processes()

        #  Padding adjustments.
        r_xpad = 15
        r_ypad = 10
        p_xpad = -15
        p_ypad = -22

        #  Draw resources.
        for i in range(1, num_r + 1):

            #  Store location for future use.
            self.location_r.append((int(i * ((self.width - self.menu_width) / (num_r + 1)) - (self.shape_size / 2)),
                                    self.shape_size))

            #  Draw rectangle.
            pygame.draw.rect(
                self.screen,
                self.resource_color,
                (self.location_r[i - 1][0],
                 self.shape_size, self.shape_size,
                 self.shape_size))

            #  Render on the screen with padding.
            self.render_text(self.font_pr, "R" + str(i - 1),
                             (self.location_r[i - 1][0] + r_xpad, self.location_r[i - 1][1] + r_ypad), self.dark_blue)

        #  Draw processes.
        for i in range(1, num_p + 1):

            #  Store location for future use.
            self.location_p.append((int(i * ((self.width - self.menu_width) / (num_p + 1))), 500))

            #  Draw circle.
            pygame.draw.circle(
                self.screen,
                self.process_color,
                self.location_p[i - 1], int(self.shape_size / 2))

            #  Render on the screen with padding.
            self.render_text(self.font_pr, "P" + str(i - 1),
                             (self.location_p[i - 1][0] + p_xpad, self.location_p[i - 1][1] + p_ypad), self.dark_green)

    def render_text(self, font, text, xy_location, text_color):
        """
        General render text helper.
        :param font: pygame font object to be used.
        :param text: string text to be rendered.
        :param xy_location: (x,y) tuple location on canvas.
        :param text_color: color text should be rendered.
        """
        text = font.render(text, False, text_color)
        self.screen.blit(text, xy_location)

    def step_forward(self):
        """
        Step forward the core logic, then render that action.
        """

        #  Render the core GUI.
        self.render_main()
        #  Step forward logic.
        self.logic.step_forward()
        #  Run deadlock detection.
        deadlocked_t = self.logic.deadlock_detection()

        #  Get variables from logic.
        l_str = self.logic.get_state_string()
        num_p = self.logic.get_processes()
        num_r = self.logic.get_resources()

        #  State title.
        self.status_text3 = self.font_menu_b.render("STATE", False, self.black)
        self.screen.blit(self.status_text3, (820, 20))

        #  Step text.
        self.status_text1 = \
            self.font_menu.render("Step " + str(self.logic.get_state_num()) + " of " + str(len(self.logic.get_steps())),
                                  False, self.black)
        self.screen.blit(self.status_text1, (820, 60))

        #  Num processes and resources.
        self.status_text2 = \
            self.font_menu.render("Processes: " + str(num_p) + "  Resources: " + str(num_r), False, self.black)
        self.screen.blit(self.status_text2, (820, 85))

        #  Step title.
        self.status_text3 = self.font_menu_b.render("STEP " + str(self.logic.get_state_num()), False, self.black)
        self.screen.blit(self.status_text3, (820, 120))

        #  Step forward text.
        self.status_text1 = self.font_menu.render(l_str[0], False, self.black)
        self.screen.blit(self.status_text1, (820, 160))

        #  Process request/release text.
        self.status_text2 = self.font_menu.render(l_str[1], False, self.black)
        self.screen.blit(self.status_text2, (820, 185))

        #  Padding adjustments.
        p_padh = -30
        p_padr = -45
        r_padyh = 80
        r_padyr = 70
        r_padx = 30

        #  Get the adjacency matrices.
        holders = self.logic.get_hold_edges()
        requesters = self.logic.get_request_edges()

        #  Run through hold and request edges then render arrows.
        for resource in range(num_r):
            for process in range(num_p):
                if holders[resource][process]:
                    print("Resource %d being held by process %d." % (resource, process))
                    self.draw_arrow((self.location_p[process][0], self.location_p[process][1] + p_padh),
                                    (self.location_r[resource][0] + r_padx, self.location_r[resource][1] + r_padyh),
                                    "HOLD")
                if requesters[resource][process]:
                    print("Resource %d being requested by process %d." % (resource, process))
                    self.draw_arrow((self.location_r[resource][0] + r_padx, self.location_r[resource][1] + r_padyr),
                                    (self.location_p[process][0], self.location_p[process][1] + p_padr), "REQUEST")

        #  Check if we are deadlocked at this state.
        if deadlocked_t[0]:
            #  We are deadlocked and set text state.
            self.status_text3 = self.font_menu_b.render("STATUS: DEADLOCKED", False, self.red)
            self.screen.blit(self.status_text3, (820, 235))

            #  Padding adjustments.
            p_xpad = -15
            p_ypad = -22

            #  Highlight each deadlocked process and make them red.
            for vertex in deadlocked_t[1]:
                pygame.draw.circle(
                    self.screen,
                    self.red,
                    self.location_p[vertex], int(self.shape_size / 2))
                self.render_text(self.font_pr, "p" + str(vertex),
                                 (self.location_p[vertex][0] + p_xpad, self.location_p[vertex][1] + p_ypad),
                                 self.black)

        else:
            #  We are not deadlocked and set text state.
            self.status_text3 = self.font_menu_b.render("STATUS: OK", False, self.process_color)
            self.screen.blit(self.status_text3, (820, 235))
