from __future__ import annotations

from display.ui import UI, Label, Button, Progressbar, Default_font, Image
import pygame
from display.graphics import Objects_picture
from utils import int_to_str
from gameplay.equipment import Equipment
from gameplay.stats import Stats

class Ingame_menu(UI):
    # cette classe gère tous les menus du jeu durant une partie
    
    STATS_NAMES = {
        "pv":"Health",
        "atk":"Attack",
        "speed":"Agility",
        "crit_luck":"Crit Luck"
    }
        
    def __init__(self, draw_surface:pygame.Surface, equipment:Equipment, stats:Stats):
        # on initialise la classe parent : UI
        super().__init__(draw_surface)

        # on définie la surface sur laquelle on va dessiner ainsi que les images des objets
        self.draw_surface = draw_surface
        self.objects_images = Objects_picture("../graphics/weapons_and_armors")
        
        # on stock les objets equipment et stats liés au joueur
        self.player_equipment = equipment
        self.player_stats = stats
        
        # on créé l'affichage principal : fps, nombre de combats restants, bouton menu,...
        self.main_display()

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
                

    def main_display(self): # affichage principal
        # on vide la fenêtre
        self.clear_widget()
        # on enlève la couleur d'arrière-plan
        self.set_background_color(None)
        # on permet au jeu et au joueur de capter les imput
        self.set_grab(False)

        # on créé tous les éléments
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


        # on affiche tous les éléments
        self.bind_several_widget(
            self.fps_label,
            button_menu,
            self.fight_bar,
            self.battle_count
        )

    def main_menu(self): # menu principal
        self.clear_widget()
        # on définie la couleur d'arrière avec un degré de transparence
        self.set_background_color(pygame.Color(20, 20, 20, 150))
        # on 'intercepte' les imputs pour que l'on ne puisse plus faire bouger le joueur
        self.set_grab(True)

        # on créé et affiche tous les éléments
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

    def stats_menu(self): # menu stats, permet de voir ses stats et d'attribuer ses points
        self.clear_widget()

        # on récupère les informations à afficher
        self.points, self.stats = self.get_stats_and_points()

        # on créé et affiche des éléments
        previous_button = Previous_button(self.draw_surface, self.main_menu)
        close_button = Close_button(self.draw_surface, self.main_display)

        stats_title = Label(pygame.Vector2(40, 40), "STATS", Default_font(30), pygame.Color(255, 255, 255))

        point_label = Label(pygame.Vector2(900, 150), "Points :", Default_font(25), pygame.Color(255, 255, 255))
        self.point_value_label = Label(pygame.Vector2(915, 200), str(self.points), Default_font(40), pygame.Color(255, 255, 255))

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
        # affiche autant de lignes que de stats
        for stat, value in self.stats.items():
            self.value[stat] = value
            self.to_add_value[stat] = 0

            stats_label = Label(pygame.Vector2(70, y+10), Ingame_menu.STATS_NAMES[stat]+" :", Default_font(20), pygame.Color(255, 255, 255))

            plus_button = Button(pygame.Rect(500, y, 40, 40), "+", Default_font(20), callback=None, text_color=pygame.Color(
                255, 255, 255), color=pygame.Color(120, 120, 120),  hover_color=pygame.Color(70, 70, 70), multiclick=True)
            minus_button = Button(pygame.Rect(650, y, 40, 40), "-", Default_font(20), callback=None, text_color=pygame.Color(
                255, 255, 255), color=pygame.Color(120, 120, 120),  hover_color=pygame.Color(70, 70, 70), multiclick=True)

            # indispensable : sinon tous les bouttons changent la même stat, la dernière, à cause de la boucle
            plus_button.set_callback(self.add_point, stat)
            minus_button.set_callback(self.remove_point, stat)

            stats_value_label = Label(pygame.Vector2(300, y+10),
                                      str(Stats.default_value[stat] + self.value[stat]), Default_font(20), pygame.Color(255, 255, 255))
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

    def add_point(self, stat):
        # ajoute un point si c'est possible à la stat choisie
        if self.points > 0:
            self.to_add_value[stat] += 1
            self.points -= 1

            self.stats[stat] = self.value[stat] + self.to_add_value[stat]
            self.stats_labels[stat][0].update_text(str(Stats.default_value[stat] + self.stats[stat]))
            self.stats_labels[stat][1].update_text(str(self.to_add_value[stat])) # to add label
            self.point_value_label.update_text(str(self.points))

    def remove_point(self, stat):
        # enlève un point si c'est possible à la stat choisie
        if self.to_add_value[stat] != 0:
            self.points += 1
            self.to_add_value[stat] -= 1

            self.stats[stat] = self.value[stat] + self.to_add_value[stat]
            self.stats_labels[stat][0].update_text(str(Stats.default_value[stat] + self.stats[stat]))
            self.stats_labels[stat][1].update_text(str(self.to_add_value[stat])) # to add label
            self.point_value_label.update_text(str(self.points))

    def equipment_menu(self):
        self.clear_widget()

        previous_button = Previous_button(self.draw_surface, self.main_menu)
        close_button = Close_button(self.draw_surface, self.main_display)

        equipment_label = Label(pygame.Vector2(40,40),"EQUIPMENT",Default_font(30),pygame.Color(255,255,255))
        
        money_label = Label(pygame.Vector2(400,40),f"You have : {int_to_str(self.player_equipment.money)} $",Default_font(20),pygame.Color(255,255,255))
            
        self.bind_several_widget(
            equipment_label,
            money_label,
            close_button,
            previous_button
        )
        
        y=150
        for k,v in self.player_equipment.level.items():
            image = Image(self.objects_images.get_object_picture(k,v,7),pygame.Vector2(100,y))
            label = Label(pygame.Vector2(300,y+50),f"{k} lvl {v}",Default_font(20),pygame.Color(255,255,255))
            self.bind_several_widget(
                image,
                label
            )
            y += 150


    def get_stats_and_points(self): # renvoie un int et un dict {"nom_stat":valeur,...}
        return self.player_stats.remaining_points,self.player_stats.stats.copy()

    def set_stats_and_points(self,points:int,stats:dict) -> None:
        self.main_menu()
        self.player_stats.remaining_points = points
        self.player_stats.stats = stats
        
class Battle_ui:
    def __init__(self, ingame_menu:Ingame_menu):
        self.ingame_menu = ingame_menu
        self.y_max = self.ingame_menu.draw_surface.get_height()
        
    def start_battle(self):
        self.rounds = []
        self.rounds_labels = []
        self.draw()
        
    def draw(self):
        self.ingame_menu.clear_widget()
        self.ingame_menu.set_background_color(pygame.Color(20, 20, 20, 150))
        self.ingame_menu.set_grab(True)
        
        close_button = Close_button(self.ingame_menu.draw_surface, self.ingame_menu.main_display)
        battle_label = Label(pygame.Vector2(40, 40), "BATTLE", Default_font(30), pygame.Color(255, 255, 255))
        
        
        self.ingame_menu.bind_several_widget(
            close_button,
            battle_label
        )
        self.draw_rounds()
        
    def draw_rounds(self):
        for label in self.rounds_labels:
            self.ingame_menu.unbind_widget(label)
        self.rounds_labels = []
        
        y = self.y_max - 100
        for round in self.rounds:
            if y > 0:  # évite d'afficher des textes non visibles
                label = Label(pygame.Vector2(100, y), round, Default_font(20), pygame.Color(255,255,255))
                self.rounds_labels.append(label)
                self.ingame_menu.bind_widget(label)
                y -= 50
            else:
                return
    
    def add_round(self, *args:str):
        self.rounds = list(args) + self.rounds
        self.draw_rounds()
        
    def battle_end(self):
        ...

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
