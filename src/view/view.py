import sys
import pygame
from text import Text
from button import Button
from color_selector import ColorSelector
from input_box import InputBox
from nest import Nest
from ant import Ant


# import numpy as np
import ctypes

# View
class View:


    STARTVIEW = 'start-view'
    GAMEVIEW = 'game-view'

    def __init__(self):
        pygame.init()
        display_info = pygame.display.Info()
        width = display_info.current_w
        height = display_info.current_h
        self.state = None
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        self.background_color = pygame.Color("white")
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_event = pygame.mouse.get_pressed()
        self.elements = {}
        self.FONT = pygame.font.Font(None, 32)

    def change_view_state(self, state):
        if self.state == state:
            return
        # Destroy all UI elements that are no longer needed and clear screen
        self.elements = {}
        self.screen.fill(self.background_color)
        # Construct new UI elements for the requested state
        if state == View.STARTVIEW:
            self.state = View.STARTVIEW
            self._start_view()
        if state == View.GAMEVIEW:
            self.state = View.GAMEVIEW
            self._game_view()

    def _start_view(self):
        self.elements = {}
        # add elements for the main text
        text = Text(self, "headline", 0+int(0.15*self.width), 0+int(0.10*self.height), -1, -1, 115)
        text.set_text("ElegANT")
        self.add_element(text)

        # Add elemt for choosing players color
        player_colors = [
            (220, 0, 0),
            (255, 160, 125),
            (0, 0, 255),
            (255, 20, 147),
            (178, 58, 238),
            (0, 245, 255),
            (0, 200, 0),
            (255, 165, 0)
        ]
        self.add_element(ColorSelector(self, "colour_selector", 850, 350, 150, player_colors))

        # add element for start button and the text on it
        start_button = Button(self, "start_button", 0+int(0.15*self.width), 0+int(0.80*self.height), 250, 100, -1, (100, 100, 100), (150, 150, 150), 'square')
        self.add_element(start_button)

        starttext = Text(self, "starttext", 0+int(0.22*self.width), 0+int(0.82*self.height), -1, -1, 50)
        starttext.set_text("START")
        self.add_element(starttext)

        inputname = Text(self, "inputname", 220, 250, -1, -1, 30)
        inputname.set_text("Please enter your name")
        self.add_element(inputname)

        # add element for the input box name
        self.add_element(InputBox(self, "textbox", 100, 300, 250, 50, (0, 0, 0), (255, 100, 100), ''))

        def add_element(self, ui_element):
            self.elements[ui_element.identifier] = ui_element

    def _game_view(self):
        self.elements = {}

        # add a nest and an ant
        self.add_element(Nest(self, "nest", 650, 400, 30, (220, 0, 0)))  # red
        self.add_element(Ant(self, "ant", 660, 500, 10, (220, 0, 0)))  # peach

        # TODO add sliders to the game view
        # self.add_element(
        # Button(self, "start_button", 100, 600, 250, 100, -1, (100, 100, 100), (150, 150, 150), 'square'))  # orange
        # starttext = Text(self, "starttext", 225, 650, -1, -1, 50)
        # starttext.set_text("START")
        # self.add_element(starttext)

    def add_element(self, ui_element):
        self.elements[ui_element.identifier] = ui_element

    def get_element_by_id(self, identifier):
        if identifier in self.elements:
            return self.elements[identifier]
        else:
            print("Element does not exist")

    def draw(self, model_state=None):
        self.screen.fill(self.background_color)
        for element in self.elements.values():
            element.draw()
        pygame.display.flip()

    def events(self):
        self.mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            else:
                for element in self.elements.values():
                    element.event_handler(event)
