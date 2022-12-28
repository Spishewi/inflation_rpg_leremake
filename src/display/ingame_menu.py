from __future__ import annotations

from display.ui import UI, Label, Button, Progressbar, Default_font, Image
import pygame
from display.graphics import Objects_picture
from utils import int_to_str

class Ingame_menu(UI):
    def __init__(self, draw_surface):
        super().__init__(draw_surface)

        self.draw_surface = draw_surface
        self.objects_images = Objects_picture("../graphics/weapons_and_armors")

        # TODO
        # to remove -----------------
        self._points = 50
        self._stats = {
            "Health":500,
            "Attack":200,
            "Defense":1500,
            "Agility":128,
            "Luck":56
        }
        self._equipment_equiped = {
            "sword":0,
            "armor":0,
            "ring1":0,
            "ring2":0,
            "ring3":0,
            "ring4":0
        }
        self._prices = {
            "sword":[],
            "armor":[0, 100, 1500, 25000,100000],
            "ring":[]
        }
        # --------------------------

        self.main_display()
        
    def update(self, fps:float | None = None, distance:int | None= None):
        super().update()
        
        if fps != None:
            self.fps_label.update_text(f"fps: {fps:.2f}")
        
        if distance != None:
            self.fight_bar.update_value(distance)   

        
    def main_display(self):
        self.clear_widget()
        self.set_background_color(None)
        self.set_grab(False)


        self.fps_label  = Label(pygame.Vector2(10, 10), "", Default_font(15), pygame.Color(255, 255, 255))
        
        button_rect = pygame.Rect((0,20,100,40))
        button_rect.x = self.draw_surface.get_width() - button_rect.width - 20
        
        button_menu = Button(button_rect, "Menu", Default_font(20), callback=self.main_menu, text_color=pygame.Color(255, 255, 255), color=pygame.Color(120, 120, 120),  hover_color= pygame.Color(70, 70, 70))
        
        progressbar_rect = pygame.Rect((0, 0, 0, 0))
        progressbar_rect.x = 10
        progressbar_rect.y = self.draw_surface.get_height() - 25
        progressbar_rect.width = self.draw_surface.get_width()-20
        progressbar_rect.height = 15

        self.fight_bar = Progressbar(progressbar_rect, 0, pygame.Color(85, 160, 39), pygame.Color(134, 221, 81))

        self.bind_several_widget(
            self.fps_label,
            button_menu,
            self.fight_bar
        )
    
    def main_menu(self):
        self.clear_widget()
        self.set_background_color(pygame.Color(20,20,20,150))
        self.set_grab(True)
        
        previous_button = Previous_button(self.draw_surface,self.main_display)
        close_button = Close_button(self.draw_surface,self.main_display)

        stats_button_rect = pygame.Rect(0,200,130,40)
        stats_button_rect.x = self.draw_surface.get_width()/2 - stats_button_rect.width/2
        stats_button = Button(stats_button_rect,"Stats",Default_font(20),callback=self.stats_menu, text_color=pygame.Color(255, 255, 255), color=pygame.Color(120, 120, 120),  hover_color= pygame.Color(70, 70, 70))

        equipment_button_rect = pygame.Rect(0,300,200,40)
        equipment_button_rect.x = self.draw_surface.get_width()/2 - equipment_button_rect.width/2
        equipment_button = Button(equipment_button_rect,"Equipment",Default_font(20),callback=self.equipment_menu, text_color=pygame.Color(255, 255, 255), color=pygame.Color(120, 120, 120),  hover_color= pygame.Color(70, 70, 70))

        menu_label = Label(pygame.Vector2(40,40),"MENU",Default_font(30),pygame.Color(255,255,255))
       
        self.bind_several_widget(
            menu_label,
            stats_button,
            equipment_button,
            close_button,
            previous_button
        )

    def stats_menu(self):
        self.clear_widget()


        self.points, self.stats = self.get_stats_and_points()
        
        previous_button = Previous_button(self.draw_surface,self.main_menu)
        close_button = Close_button(self.draw_surface,self.main_display)

        stats_title = Label(pygame.Vector2(40,40),"STATS",Default_font(30),pygame.Color(255,255,255))

        point_label = Label(pygame.Vector2(900,150),"Points :",Default_font(25),pygame.Color(255,255,255))
        self.point_value_label = Label(pygame.Vector2(915,200),str(self.points),Default_font(40),pygame.Color(255,255,255))

        done_button = Button(pygame.Rect(925,350,100,40),"Done", Default_font(20), callback=lambda:self.set_stats_and_points(self.points,self.stats), text_color=pygame.Color(255, 255, 255), color=pygame.Color(120, 120, 120),  hover_color= pygame.Color(70, 70, 70))
        cancel_button = Button(pygame.Rect(900,400,150,40),"Cancel", Default_font(20), callback=self.main_menu, text_color=pygame.Color(255, 255, 255), color=pygame.Color(120, 120, 120),  hover_color= pygame.Color(70, 70, 70))

        self.bind_several_widget(
            close_button,
            previous_button,
            stats_title,
            point_label,
            self.point_value_label,
            done_button,
            cancel_button
        )

        self.value = {}
        self.to_add_value = {}
        self.stats_labels = {}
        y = 140
        for stat,value in self.stats.items():
            self.value[stat] = value
            self.to_add_value[stat] = 0

            stats_label = Label(pygame.Vector2(70,y+10),stat+" :",Default_font(20),pygame.Color(255,255,255))
            
            plus_button = Button(pygame.Rect(500,y,40,40),"+", Default_font(20),callback=None, text_color=pygame.Color(255, 255, 255), color=pygame.Color(120, 120, 120),  hover_color= pygame.Color(70, 70, 70))
            minus_button = Button(pygame.Rect(650,y,40,40),"-", Default_font(20),callback=None, text_color=pygame.Color(255, 255, 255), color=pygame.Color(120, 120, 120),  hover_color= pygame.Color(70, 70, 70))

            plus_button.set_callback(self.add_point,stat) # indispensable : sinon tous les bouttons changent la même stat, la dernière, à cause de la boucle
            minus_button.set_callback(self.remove_point,stat)

            stats_value_label = Label(pygame.Vector2(300,y+10),str(self.value[stat]),Default_font(20),pygame.Color(255,255,255))
            to_add_value_label = Label(pygame.Vector2(575,y+10),str(self.to_add_value[stat]),Default_font(20),pygame.Color(255,255,255))

            self.stats_labels[stat] = (stats_value_label,to_add_value_label)

            self.bind_several_widget(
                stats_label,
                stats_value_label,
                to_add_value_label,
                plus_button,
                minus_button
            )
            y += 70

    def add_point(self,stat)->int:
        '''return the new val'''
        if self.points != 0:
            self.to_add_value[stat] += 1
            self.points -= 1
            
            self.stats[stat] = self.value[stat] + self.to_add_value[stat]
            self.stats_labels[stat][1].update_text(str(self.to_add_value[stat]))
            self.stats_labels[stat][0].update_text(str(self.stats[stat]))
            self.point_value_label.update_text(str(self.points))
            return 

    def remove_point(self,stat):
        if self.to_add_value[stat] != 0:
            self.points += 1
            self.to_add_value[stat] -= 1

            self.stats_labels[stat][1].update_text(str(self.to_add_value[stat]))
            self.stats_labels[stat][0].update_text(str(self.value[stat] + self.to_add_value[stat]))
            self.point_value_label.update_text(str(self.points))

    def equipment_menu(self):
        self.clear_widget()
        
        previous_button = Previous_button(self.draw_surface,self.main_menu)
        close_button = Close_button(self.draw_surface,self.main_display)

        equipment_label = Label(pygame.Vector2(40,40),"EQUIPMENT",Default_font(30),pygame.Color(255,255,255))
        
        sword_button = Button(pygame.Rect(100,200,150,150),"", Default_font(20), callback=self.sword_menu, text_color=pygame.Color(255, 255, 255), color=pygame.Color(120, 120, 120),  hover_color= pygame.Color(70, 70, 70),image_background=self.objects_images.get_object_picture("sword",self._equipment_equiped["sword"],7))
        armor_button = Button(pygame.Rect(100,400,150,150),"", Default_font(20), callback=self.armor_menu, text_color=pygame.Color(255, 255, 255), color=pygame.Color(120, 120, 120),  hover_color= pygame.Color(70, 70, 70),image_background=self.objects_images.get_object_picture("armor",self._equipment_equiped["armor"],7))

        y = 200
        num = 1
        for i in range(2):
            x = 500
            for j in range(2):
                image = self.objects_images.get_object_picture("ring",self._equipment_equiped[f"ring{num}"],7)
                ring_button = Button(pygame.Rect(x,y,150,150),"", Default_font(20), callback=None, text_color=pygame.Color(255, 255, 255), color=pygame.Color(120, 120, 120),  hover_color= pygame.Color(70, 70, 70),image_background=image)
                ring_button.set_callback(self.ring_menu,num)
                
                self.bind_widget(ring_button)
                num += 1
                x += 200
            y += 200
            
        self.bind_several_widget(
            equipment_label,
            close_button,
            previous_button,
            sword_button,
            armor_button
        )
      
    def sword_menu(self):
        self.clear_widget()
        
        sword_label = Label(pygame.Vector2(40,40),"SWORDS",Default_font(30),pygame.Color(255,255,255))
        
        previous_button = Previous_button(self.draw_surface,self.equipment_menu)
        close_button = Close_button(self.draw_surface,self.main_display)
        
        self.bind_several_widget(
            sword_label,
            close_button,
            previous_button
        )
        
    def armor_menu(self):
        self.clear_widget()
        
        armor_label = Label(pygame.Vector2(40,40),"ARMORS",Default_font(30),pygame.Color(255,255,255))
        
        previous_button = Previous_button(self.draw_surface,self.equipment_menu)
        close_button = Close_button(self.draw_surface,self.main_display)
        
        self.bind_several_widget(
            armor_label,
            close_button,
            previous_button
        )
        
        y = 100
        for i in range(5):
            armor_button = Button(pygame.Rect(150,y,75,75),"", Default_font(20), callback=None, text_color=pygame.Color(255, 255, 255), color=pygame.Color(120, 120, 120),  hover_color= pygame.Color(70, 70, 70),image_background=self.objects_images.get_object_picture("armor", i,3))
            armor_button.set_callback(self.buy_menu,("armor",i))
            price_label = Label(pygame.Vector2(300,y+25),f"Price : {int_to_str(self._prices['armor'][i])}",Default_font(20),pygame.Color(255,255,255))
            
            self.bind_several_widget(
                armor_button,
                price_label
            )
            y += 100
    
        
    def ring_menu(self,num):
        self.clear_widget()
        
        armor_label = Label(pygame.Vector2(40,40),f"RING {num}",Default_font(30),pygame.Color(255,255,255))
        
        previous_button = Previous_button(self.draw_surface,self.equipment_menu)
        close_button = Close_button(self.draw_surface,self.main_display)
        
        self.bind_several_widget(
            armor_label,
            close_button,
            previous_button
        )
        
    def buy_menu(self,object:tuple):
        '''open the buy menu

        Args:
            object (object_type:str, object_id:int): example -> ("armor",3)
        '''
        self.clear_widget()
        object_type,object_id = object
        
        armor_label = Label(pygame.Vector2(40,40),"BUY",Default_font(30),pygame.Color(255,255,255))
        
        previous_button = Previous_button(self.draw_surface,self.armor_menu)
        close_button = Close_button(self.draw_surface,self.main_display)
        
        price_label = Label(pygame.Vector2(100,100),f"Do you want to buy this {object_type} for {self._prices[object_type][object_id]}€",Default_font(20),pygame.Color(255,255,255))
        
        self.bind_several_widget(
            armor_label,
            close_button,
            previous_button,
            price_label
        )

    def get_stats_and_points(self): # renvoie un int et un dict {"nom_stat":valeur,...}
        return self._points,self._stats.copy()

    def set_stats_and_points(self,points:int,stats:list) -> None:
        self.main_menu()
        self._points = points
        self._stats = stats


    def do_nothing(self):
        return


class Close_button(Button):
    def __init__(self,draw_surface:pygame.Surface,main_menu):
        self.rect = pygame.Rect(0,20,40,40)
        self.rect.x = draw_surface.get_width() - self.rect.width - 20

        super().__init__(self.rect,"X",Default_font(20),callback=main_menu, text_color=pygame.Color(255, 255, 255), color=pygame.Color(120, 120, 120),  hover_color= pygame.Color(70, 70, 70))


class Previous_button(Button):
    def __init__(self,draw_surface:pygame.Surface,main_menu):
        self.rect = pygame.Rect(0,20,40,40)
        self.rect.x = draw_surface.get_width() - self.rect.width - 80

        super().__init__(self.rect,"<",Default_font(20),callback=main_menu, text_color=pygame.Color(255, 255, 255), color=pygame.Color(120, 120, 120),  hover_color= pygame.Color(70, 70, 70))