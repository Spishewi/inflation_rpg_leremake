from display.ui import UI, Button, Label, Default_font

import pygame
class Title_screen_menu(UI):
    def __init__(self, draw_surface: pygame.Surface) -> None:
        super().__init__(draw_surface)
        self.set_background_color(pygame.Color(100,100,0))
        self.must_start = False
        
        welcome_label_1st_line = Label(pygame.Vector2(300, 50), "WELCOME TO THIS INCREDIBLE", Default_font(25), pygame.Color(255, 255, 255))
        welcome_label_2nd_line = Label(pygame.Vector2(320, 100), "REMIX OF INFLATION RPG !!", Default_font(25), pygame.Color(255, 255, 255))
        
        start_button = Button(pygame.Rect(500, 200, 250, 100), "Play", Default_font(20), callback=self.set_game_starting, text_color=pygame.Color(255, 255, 255), color=pygame.Color(120, 120, 120),  hover_color= pygame.Color(70, 70, 70))
        equipment_button = Button(pygame.Rect(450, 400, 150, 50), "Equipment", Default_font(15), self.do_nothing, text_color=pygame.Color(255, 255, 255), color=pygame.Color(120, 120, 120),  hover_color= pygame.Color(70, 70, 70))
        exit_button = Button(pygame.Rect(650, 400, 150, 50), "Exit", Default_font(15), self.do_nothing, text_color=pygame.Color(255, 255, 255), color=pygame.Color(120, 120, 120),  hover_color= pygame.Color(70, 70, 70))

        self.bind_several_widget(
            welcome_label_1st_line,
            welcome_label_2nd_line,
            start_button,
            equipment_button,
            exit_button
        )
    

    
    def do_nothing(self) -> None:
        pass
    
    def set_game_starting(self):
        print("a")
        self.must_start = True
        
    def must_start_game(self):
        return self.must_start