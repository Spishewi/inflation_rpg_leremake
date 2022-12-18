from display.ui import UI, Button, Label, Default_font

import pygame
class Title_screen_menu(UI):
    def __init__(self, draw_surface: pygame.Surface) -> None:
        super().__init__(draw_surface)

        
        self.welcome_label = Label(pygame.Vector2(50, 50), "WELCOME TO THIS INCREDIBLE REMIX OF THE GAME INFLATION RPG !!", Default_font(25), pygame.Color(255, 255, 255))
        
        self.start_button = Button(pygame.Rect(50, 150, 150, 50), "Play", Default_font(15), self.do_nothing, text_color=pygame.Color(255, 255, 255), color=pygame.Color(120, 120, 120),  hover_color= pygame.Color(70, 70, 70))
        self.equipment_button = Button(pygame.Rect(50, 250, 150, 50), "Equipment", Default_font(15), self.do_nothing, text_color=pygame.Color(255, 255, 255), color=pygame.Color(120, 120, 120),  hover_color= pygame.Color(70, 70, 70))
        self.exit_button = Button(pygame.Rect(50, 350, 150, 50), "Exit", Default_font(15), self.do_nothing, text_color=pygame.Color(255, 255, 255), color=pygame.Color(120, 120, 120),  hover_color= pygame.Color(70, 70, 70))

        self.bind_several_widget(self.welcome_label, self.start_button, self.equipment_button, self.exit_button)
    
    def do_nothing(self) -> None:
        pass