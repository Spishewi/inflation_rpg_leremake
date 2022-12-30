from __future__ import annotations # permet d'ajouter certaines choses non disponibles sur les vielles versions du lycée de python

from display.ui import UI, Button, Label, Default_font, Image
from gameplay.equipment import Equipment
from display.graphics import Objects_picture
from utils import int_to_str

import pygame
class Title_screen_menu(UI):
    def __init__(self, draw_surface: pygame.Surface, player_equipment:Equipment) -> None:
        super().__init__(draw_surface)
        self.set_background_color(pygame.Color(50,40,20))
        self.draw_surface = draw_surface
        
        self.objects_images = Objects_picture("../graphics/weapons_and_armors")
        
        self.must_start = False
        self.must_quit = False
        
        # TODO: to remove
        self._money = 100
        self._prices = {
            "sword":[1,10,100,1000,10000,100000,1000000,10000000,100000000,1000000000,10000000000,100000000000,1000000000000,10000000000000,100000000000000],
            "armor":[1, 100, 1500, 25000,100000],
            "ring":[i for i in range(15)]
        }
        #---------------
        
        self.equipment = player_equipment
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
        money_label = Label(pygame.Vector2(400,40),f"You have : {int_to_str(self._money)} $",Default_font(20),pygame.Color(255,255,255))
            
        self.bind_several_widget(
            equipment_label,
            close_button,
            money_label
        )
    
        x = 150
        for k,v in self.equipment.get_dict().items():
            object_image = Image(self.objects_images.get_object_picture(k,v,7),pygame.Vector2(x+60,200))
            price_label = Label(pygame.Vector2(x,350),f"Price : {self._prices[k][v+1]} $",Default_font(20),pygame.Color(255,255,255))
            upgrade_button = Button(pygame.Rect(x,400,250,100),"Upgrade",Default_font(20),callback=None, text_color=pygame.Color(255, 255, 255), color=pygame.Color(120, 120, 120),  hover_color= pygame.Color(70, 70, 70))
            upgrade_button.set_callback(self.upgrade_object,k)
            
            self.bind_several_widget(
                object_image,
                price_label,
                upgrade_button
            )
            x += 350
        
    def upgrade_object(self,object_type:str):
        pass
    
    def set_game_starting(self):
        self.must_start = True    
    
    def set_must_quit(self):
        self.must_quit = True