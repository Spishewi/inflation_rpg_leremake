from __future__ import annotations

from display.ui import UI, Label, Button, Progressbar
import pygame

class Font(pygame.font.Font):
    def __init__(self,size):
        super().__init__("../graphics/PublicPixel.ttf",size)

class Ingame_menu(UI):
    def __init__(self, draw_surface):
        super().__init__(draw_surface)

        self.draw_surface = draw_surface
        
        self.main_display()
        
    def update(self, fps:float | None = None, distance:int | None= None):
        super().update()
        
        if fps != None:
            self.fps_label.update_text(f"fps: {fps:.2f}")
        
        if distance != None:
            self.fight_bar.update_value((self.fight_bar.value+distance)%100)   

        
    def main_display(self):
        self.clear_widget()
        self.set_background_color(None)

        self.fps_label  = Label(pygame.Vector2(10, 10), "", Font(15), pygame.Color(255, 255, 255))
        
        button_rect = pygame.Rect((0,20,100,40))
        button_rect.x = self.draw_surface.get_width() - button_rect.width - 20
        
        self.button_menu = Button(button_rect, "Menu", Font(20), callback=self.main_menu, text_color=pygame.Color(255, 255, 255), color=pygame.Color(120, 120, 120),  hover_color= pygame.Color(70, 70, 70))
        
        progressbar_rect = pygame.Rect((0, 0, 0, 0))
        progressbar_rect.x = 10
        progressbar_rect.y = self.draw_surface.get_height() - 25
        progressbar_rect.width = self.draw_surface.get_width()-20
        progressbar_rect.height = 15

        self.fight_bar = Progressbar(progressbar_rect, 0, 100, pygame.Color(85, 160, 39), pygame.Color(134, 221, 81))

        self.bind_widget(self.fps_label)
        self.bind_widget(self.button_menu)
        self.bind_widget(self.fight_bar)
    
    def main_menu(self):
        self.clear_widget()
        self.set_background_color(pygame.Color(20,20,20,150))
        
        self.previous_button = Previous_button(self.draw_surface,self.main_display)
        self.close_button = Close_button(self.draw_surface,self.main_display)
        self.bind_widget(self.close_button)
        self.bind_widget(self.previous_button)


        stats_button_rect = pygame.Rect(0,200,130,40)
        stats_button_rect.x = self.draw_surface.get_width()/2 - stats_button_rect.width/2
        self.stats_button = Button(stats_button_rect,"Stats",Font(20),callback=self.stats_menu, text_color=pygame.Color(255, 255, 255), color=pygame.Color(120, 120, 120),  hover_color= pygame.Color(70, 70, 70))

        equipment_button_rect = pygame.Rect(0,300,200,40)
        equipment_button_rect.x = self.draw_surface.get_width()/2 - equipment_button_rect.width/2
        self.equipment_button = Button(equipment_button_rect,"Equipment",Font(20),callback=self.equipment_menu, text_color=pygame.Color(255, 255, 255), color=pygame.Color(120, 120, 120),  hover_color= pygame.Color(70, 70, 70))
        
        self.bind_widget(self.stats_button)
        self.bind_widget(self.equipment_button)

        menu_label = Label(pygame.Vector2(40,40),"MENU",Font(30),pygame.Color(255,255,255))
        self.bind_widget(menu_label)
    
    def stats_menu(self):
        self.clear_widget()

        stats = [
            "Health",
            "Attack",
            "Defense",
            "Agility",
            "Luck"
        ]
        
        previous_button = Previous_button(self.draw_surface,self.main_menu)
        close_button = Close_button(self.draw_surface,self.main_display)

        stats_title = Label(pygame.Vector2(40,40),"STATS",Font(30),pygame.Color(255,255,255))

        self.bind_several_widget(close_button,previous_button,stats_title)

        value = 1000
        y = 140
        for stat in stats:
            stats_label = Label(pygame.Vector2(70,y+10),stat,Font(20),pygame.Color(255,255,255))

            plus_button = Button(pygame.Rect(500,y,40,40),"+", Font(20), callback=self.do_sth, text_color=pygame.Color(255, 255, 255), color=pygame.Color(120, 120, 120),  hover_color= pygame.Color(70, 70, 70))
            minus_button = Button(pygame.Rect(650,y,40,40),"-", Font(20),callback=self.do_sth, text_color=pygame.Color(255, 255, 255), color=pygame.Color(120, 120, 120),  hover_color= pygame.Color(70, 70, 70))

            stats_value = Label(pygame.Vector2(300,y+10),str(value),Font(20),pygame.Color(255,255,255))
            to_add_value = Label(pygame.Vector2(565,y+10),"100",Font(20),pygame.Color(255,255,255))

            self.bind_several_widget(stats_label,plus_button,minus_button,stats_value,to_add_value)

            y += 70

    def equipment_menu(self):
        self.clear_widget()
        
        self.previous_button = Previous_button(self.draw_surface,self.main_menu)
        self.close_button = Close_button(self.draw_surface,self.main_display)

        self.bind_widget(self.close_button)
        self.bind_widget(self.previous_button)

        equipment_label = Label(pygame.Vector2(40,40),"EQUIPMENT",Font(30),pygame.Color(255,255,255))
        self.bind_widget(equipment_label)

    def do_sth(self):
        pass




class Close_button(Button):
    def __init__(self,draw_surface:pygame.Surface,main_menu):
        self.rect = pygame.Rect(0,20,40,40)
        self.rect.x = draw_surface.get_width() - self.rect.width - 20

        super().__init__(self.rect,"X",pygame.font.Font("../graphics/PublicPixel.ttf", 20),callback=main_menu, text_color=pygame.Color(255, 255, 255), color=pygame.Color(120, 120, 120),  hover_color= pygame.Color(70, 70, 70))


class Previous_button(Button):
    def __init__(self,draw_surface:pygame.Surface,main_menu):
        self.rect = pygame.Rect(0,20,40,40)
        self.rect.x = draw_surface.get_width() - self.rect.width - 80

        super().__init__(self.rect,"<",pygame.font.Font("../graphics/PublicPixel.ttf", 20),callback=main_menu, text_color=pygame.Color(255, 255, 255), color=pygame.Color(120, 120, 120),  hover_color= pygame.Color(70, 70, 70))