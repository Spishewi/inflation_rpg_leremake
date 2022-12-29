from __future__ import annotations # permet d'ajouter certaines choses non disponibles sur les vielles versions du lycée de python

from display.ui import UI, Button, Label, Default_font

import pygame
class Title_screen_menu(UI):
    def __init__(self, draw_surface: pygame.Surface) -> None:
        super().__init__(draw_surface)
        self.set_background_color(pygame.Color(50,40,20))
        self.draw_surface = draw_surface
        
        self.must_start = False
        self.must_quit = False
        
        self.play_menu()
        
        
    def play_menu(self):
        self.clear_widget()
        
        welcome_label_1st_line = Label(pygame.Vector2(300, 50), "WELCOME TO THIS INCREDIBLE", Default_font(25), pygame.Color(255, 255, 255))
        welcome_label_2nd_line = Label(pygame.Vector2(320, 100), "REMIX OF INFLATION RPG !!", Default_font(25), pygame.Color(255, 255, 255))
        
        start_button = Button(pygame.Rect(500, 200, 250, 100), "Play", Default_font(20), callback=self.set_game_starting, text_color=pygame.Color(255, 255, 255), color=pygame.Color(120, 120, 120),  hover_color= pygame.Color(70, 70, 70))
        equipment_button = Button(pygame.Rect(450, 400, 150, 50), "Equipment", Default_font(15), self.equipment_menu, text_color=pygame.Color(255, 255, 255), color=pygame.Color(120, 120, 120),  hover_color= pygame.Color(70, 70, 70))
        exit_button = Button(pygame.Rect(650, 400, 150, 50), "Exit", Default_font(15), self.set_must_quit, text_color=pygame.Color(255, 255, 255), color=pygame.Color(120, 120, 120),  hover_color= pygame.Color(70, 70, 70))

        self.bind_several_widget(
            welcome_label_1st_line,
            welcome_label_2nd_line,
            start_button,
            equipment_button,
            exit_button
        )
     

    
    def equipment_menu(self) -> None:
        self.clear_widget()
        
        self.rect = pygame.Rect(0,20,40,40)
        self.rect.x = self.draw_surface.get_width() - self.rect.width - 20

        close_button = Button(self.rect,"X",Default_font(20),callback=self.play_menu, text_color=pygame.Color(255, 255, 255), color=pygame.Color(120, 120, 120),  hover_color= pygame.Color(70, 70, 70))
        
        equipment_label = Label(pygame.Vector2(40,40),"EQUIPMENT",Default_font(30),pygame.Color(255,255,255))
       
        self.bind_several_widget(
            equipment_label,
            close_button
        )
    
    def set_game_starting(self):
        self.must_start = True
        
    
    def set_must_quit(self):
        self.must_quit = True