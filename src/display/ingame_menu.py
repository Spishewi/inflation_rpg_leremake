from __future__ import annotations

from display.ui import UI, Label, Button, Progressbar, Default_font, Image
import pygame
from display.graphics import Objects_picture
from utils import int_to_str
from gameplay.equipment import Equipment
from gameplay.stats import Stats

class Ingame_menu(UI):
    def __init__(self, draw_surface, equipment):
        super().__init__(draw_surface)

        self.draw_surface = draw_surface
        self.objects_images = Objects_picture("../graphics/weapons_and_armors")
        
        self.equipment = equipment
        self.equipment_dict = self.get_equipment()
        
        # TODO
        # to remove -----------------
        self._points = 50
        self._money = 100
        self._stats = {
            "Health": 0,
            "Attack": 0,
            "Agility": 0,
            "Crit Luck": 0
        }
        # --------------------------

        self.main_display()

    def get_money(self):
        return self._money

    def set_money(self, value):
        self._money = value

    def update(self, **kwargs):
        # s'il n'y a pas d'args, on update en général
        if len(kwargs) == 0:
            super().update()
        else:
            # On met a jour les arguments
            for k, v in kwargs.items():
                if k == "fps":
                    self.fps_label.update_text(f"fps: {v:.2f}")

                elif k == "distance":
                    self.fight_bar.update_value(v)
                elif k == "battle_count":
                    self.battle_count.update_text(f"Remaining battles : {v[0]}/{v[1]}")
                elif k == "stats":
                    self._stats = {
                        "Health": v.pv + Stats.default_pv,
                        "Attack": v.atk + Stats.default_atk,
                        "Agility": v.speed + Stats.default_speed,
                        "Crit Luck": v.crit_luck + Stats.default_crit_luck
                    }
                    self._points = v.remaining_points
                    self._money = v.money

    def main_display(self):
        self.clear_widget()
        self.set_background_color(None)
        self.set_grab(False)

        self.fps_label = Label(pygame.Vector2(10, 10), "", Default_font(15), pygame.Color(255, 255, 255))

        button_rect = pygame.Rect((0, 20, 100, 40))
        button_rect.x = self.draw_surface.get_width() - button_rect.width - 20

        button_menu = Button(button_rect, "Menu", Default_font(20), callback=self.main_menu, text_color=pygame.Color(
            255, 255, 255), color=pygame.Color(120, 120, 120),  hover_color=pygame.Color(70, 70, 70))

        progressbar_rect = pygame.Rect((0, 0, 0, 0))
        progressbar_rect.x = 10
        progressbar_rect.y = self.draw_surface.get_height() - 25
        progressbar_rect.width = self.draw_surface.get_width()-20
        progressbar_rect.height = 15

        self.fight_bar = Progressbar(progressbar_rect, 0, pygame.Color(85, 160, 39), pygame.Color(134, 221, 81))
        self.battle_count = Label(pygame.Vector2(progressbar_rect.x, progressbar_rect.y-25),
                                  "Remaining battles : 0/0", Default_font(15), pygame.Color(255, 255, 255))

        self.bind_several_widget(
            self.fps_label,
            button_menu,
            self.fight_bar,
            self.battle_count
        )

    def main_menu(self):
        self.clear_widget()
        self.set_background_color(pygame.Color(20, 20, 20, 150))
        self.set_grab(True)

        previous_button = Previous_button(self.draw_surface, self.main_display)
        close_button = Close_button(self.draw_surface, self.main_display)

        stats_button_rect = pygame.Rect(0, 200, 130, 40)
        stats_button_rect.x = self.draw_surface.get_width()/2 - stats_button_rect.width/2
        stats_button = Button(stats_button_rect, "Stats", Default_font(20), callback=self.stats_menu, text_color=pygame.Color(
            255, 255, 255), color=pygame.Color(120, 120, 120),  hover_color=pygame.Color(70, 70, 70))

        equipment_button_rect = pygame.Rect(0, 300, 200, 40)
        equipment_button_rect.x = self.draw_surface.get_width()/2 - equipment_button_rect.width/2
        equipment_button = Button(equipment_button_rect, "Equipment", Default_font(20), callback=self.equipment_menu, text_color=pygame.Color(
            255, 255, 255), color=pygame.Color(120, 120, 120),  hover_color=pygame.Color(70, 70, 70))

        menu_label = Label(pygame.Vector2(40, 40), "MENU", Default_font(30), pygame.Color(255, 255, 255))

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

        previous_button = Previous_button(self.draw_surface, self.main_menu)
        close_button = Close_button(self.draw_surface, self.main_display)

        stats_title = Label(pygame.Vector2(40, 40), "STATS", Default_font(30), pygame.Color(255, 255, 255))

        point_label = Label(pygame.Vector2(900, 150), "Points :", Default_font(25), pygame.Color(255, 255, 255))
        self.point_value_label = Label(pygame.Vector2(915, 200), str(
            self.points), Default_font(40), pygame.Color(255, 255, 255))

        done_button = Button(pygame.Rect(925, 350, 100, 40), "Done", Default_font(20), callback=lambda: self.set_stats_and_points(
            self.points, self.stats), text_color=pygame.Color(255, 255, 255), color=pygame.Color(120, 120, 120),  hover_color=pygame.Color(70, 70, 70))
        cancel_button = Button(pygame.Rect(900, 400, 150, 40), "Cancel", Default_font(20), callback=self.main_menu, text_color=pygame.Color(
            255, 255, 255), color=pygame.Color(120, 120, 120),  hover_color=pygame.Color(70, 70, 70))

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
        for stat, value in self.stats.items():
            self.value[stat] = value
            self.to_add_value[stat] = 0

            stats_label = Label(pygame.Vector2(70, y+10), stat+" :", Default_font(20), pygame.Color(255, 255, 255))

            plus_button = Button(pygame.Rect(500, y, 40, 40), "+", Default_font(20), callback=None, text_color=pygame.Color(
                255, 255, 255), color=pygame.Color(120, 120, 120),  hover_color=pygame.Color(70, 70, 70), multiclick=True)
            minus_button = Button(pygame.Rect(650, y, 40, 40), "-", Default_font(20), callback=None, text_color=pygame.Color(
                255, 255, 255), color=pygame.Color(120, 120, 120),  hover_color=pygame.Color(70, 70, 70), multiclick=True)

            # indispensable : sinon tous les bouttons changent la même stat, la dernière, à cause de la boucle
            plus_button.set_callback(self.add_point, stat)
            minus_button.set_callback(self.remove_point, stat)

            stats_value_label = Label(pygame.Vector2(300, y+10),
                                      str(self.value[stat]), Default_font(20), pygame.Color(255, 255, 255))
            to_add_value_label = Label(pygame.Vector2(
                575, y+10), str(self.to_add_value[stat]), Default_font(20), pygame.Color(255, 255, 255))

            self.stats_labels[stat] = (stats_value_label, to_add_value_label)

            self.bind_several_widget(
                stats_label,
                stats_value_label,
                to_add_value_label,
                plus_button,
                minus_button
            )
            y += 70

    def add_point(self, stat) -> int:
        '''return the new val'''
        if self.points > 0:
            self.to_add_value[stat] += 1
            self.points -= 1

            self.stats[stat] = self.value[stat] + self.to_add_value[stat]
            self.stats_labels[stat][1].update_text(str(self.to_add_value[stat]))
            self.stats_labels[stat][0].update_text(str(self.stats[stat]))
            self.point_value_label.update_text(str(self.points))
            return

    def remove_point(self, stat):
        if self.to_add_value[stat] != 0:
            self.points += 1
            self.to_add_value[stat] -= 1

            self.stats_labels[stat][1].update_text(str(self.to_add_value[stat]))
            self.stats_labels[stat][0].update_text(str(self.value[stat] + self.to_add_value[stat]))
            self.point_value_label.update_text(str(self.points))

    def equipment_menu(self):
        self.clear_widget()

        previous_button = Previous_button(self.draw_surface, self.main_menu)
        close_button = Close_button(self.draw_surface, self.main_display)

        equipment_label = Label(pygame.Vector2(40,40),"EQUIPMENT",Default_font(30),pygame.Color(255,255,255))
        
        money_label = Label(pygame.Vector2(400,40),f"You have : {int_to_str(self.get_money())} $",Default_font(20),pygame.Color(255,255,255))
            
        self.bind_several_widget(
            equipment_label,
            money_label,
            close_button,
            previous_button
        )
        
        y=150
        for k,v in self.equipment_dict.items():
            image = Image(self.objects_images.get_object_picture(k,v,7),pygame.Vector2(100,y))
            label = Label(pygame.Vector2(300,y+50),f"{k} lvl {v}",Default_font(20),pygame.Color(255,255,255))
            self.bind_several_widget(
                image,
                label
            )
            y += 150


    def get_stats_and_points(self): # renvoie un int et un dict {"nom_stat":valeur,...}
        return self._points,self._stats.copy()

    def set_stats_and_points(self,points:int,stats:dict) -> None:
        self.main_menu()
        self._points = points
        self._stats = stats

    def get_equipment(self):
        return {
            "armor":self.equipment.armor_level,
            "sword":self.equipment.sword_level,
            "ring":self.equipment.ring_level
        }


    def do_nothing(self):
        return


class Close_button(Button):
    def __init__(self, draw_surface: pygame.Surface, main_menu):
        self.rect = pygame.Rect(0, 20, 40, 40)
        self.rect.x = draw_surface.get_width() - self.rect.width - 20

        super().__init__(self.rect, "X", Default_font(20), callback=main_menu, text_color=pygame.Color(
            255, 255, 255), color=pygame.Color(120, 120, 120),  hover_color=pygame.Color(70, 70, 70))


class Previous_button(Button):
    def __init__(self, draw_surface: pygame.Surface, main_menu):
        self.rect = pygame.Rect(0, 20, 40, 40)
        self.rect.x = draw_surface.get_width() - self.rect.width - 80

        super().__init__(self.rect, "<", Default_font(20), callback=main_menu, text_color=pygame.Color(
            255, 255, 255), color=pygame.Color(120, 120, 120),  hover_color=pygame.Color(70, 70, 70))
