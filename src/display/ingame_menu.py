from __future__ import annotations
from typing import TYPE_CHECKING


from display.ui import UI, Label, Button, Progressbar, Default_font, Image
import pygame
from display.graphics import Objects_picture
from utils import int_to_str
from gameplay.stats import Stats

# Import seulement pour les type-hint (opti)
if TYPE_CHECKING:
    from gameplay.equipment import Equipment
    from engine.game import Game
    

class Ingame_menu(UI):
    # cette classe gère tous les menus du jeu durant une partie
    
    STATS_NAMES = {
        "pv":"Health",
        "atk":"Attack",
        "speed":"Agility",
        "crit_luck":"Crit Luck"
    }
        
    def __init__(self, draw_surface:pygame.Surface, game:Game):
        # on initialise la classe parent : UI
        super().__init__(draw_surface)

        # on définie la surface sur laquelle on va dessiner ainsi que les images des objets
        self.draw_surface = draw_surface
        self.objects_images = Objects_picture("../graphics/weapons_and_armors")
        
        # on récupère le jeu pour avoir les infos voulues
        self.game = game
        
        # on stock les objets equipment et stats liés au joueur
        self.player_equipment = self.game.equipment
        self.player_stats = self.game.stats
        
        # on créé l'affichage principal : fps, nombre de combats restants, bouton menu,...
        self.main_display()
        self.main_menu()        # pour le set grab et le background
        self.stats_menu()

    def update(self, **kwargs):
        # s'il n'y a pas d'args, on update en général
        if len(kwargs) == 0:
            super().update()
        else:
            # On regarde ce qu'il faut update
            for k, v in kwargs.items():
                # on s'occupe des fps
                if k == "fps":
                    self.fps_label.update_text(f"fps: {v:.2f}")
                # on s'occupe de la fightbar
                elif k == "distance":
                    self.fight_bar.update_value(v)
                # On s'occupe du battle count
                elif k == "battle_count":
                    self.battle_count.update_text(f"Remaining battles : {v[0]}/{v[1]}")
                # On s'occupe du level display
                elif k == "level":
                    self.level_display.update_text(f"Level : {v}")
                # On s'occupe de l'update de l'affichage des stats
                elif k == "stats":
                    self.hp_display.update_text(f"Health:{int_to_str(v._pv_max).rjust(6)}") # oui on a mis pv dans le code au lieu de hp
                    self.atk_display.update_text(f"Attack:{int_to_str(v._atk).rjust(6)}")
                    self.crit_multiplier_display.update_text(f"Crit multiplier:{int_to_str(v._crit_multiplier).rjust(6)}")
                    self.crit_luck_display.update_text(f"Crit luck:{int_to_str(v._crit_luck).rjust(6)}")
                    self.agility_display.update_text(f"Agility:{int_to_str(v.speed).rjust(6)}")
                    self.stats_display_update_positions()
                
    def stats_display_update_positions(self):
        """
            On met a jour les positions des stats (car suivant leurs longueur ça peut changer)
        """
        stats_display_list = [
            self.hp_display,
            self.atk_display,
            self.crit_multiplier_display,
            self.crit_luck_display,
            self.agility_display
        ]

        window_width, window_height = pygame.display.get_window_size()
        for i, label in enumerate(reversed(stats_display_list)):
            label.coords.x = window_width - label.box.width - 10
            label.coords.y = window_height - (50 + i*(label.box.height + 10))


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

        # on défini des par paramètres par défaut pour pas avoir à les réécrire
        stats_display_params = {
            "font": Default_font(15),
            "text_color": pygame.Color(255, 255, 255),
            "text": ""
        }

        self.battle_count = Label(pygame.Vector2(progressbar_rect.x, progressbar_rect.y-25), **stats_display_params)
        self.level_display = Label(pygame.Vector2(progressbar_rect.x, progressbar_rect.y-50), **stats_display_params)

        # on défini des par paramètres par défaut pour pas avoir à les réécrire
        stats_display_params = {
            "font": Default_font(15),
            "text_color": pygame.Color(255, 255, 255, 127),
            "text": ""
        }

        self.hp_display = Label(pygame.Vector2(), **stats_display_params)
        self.atk_display = Label(pygame.Vector2(), **stats_display_params)
        self.crit_multiplier_display = Label(pygame.Vector2(), **stats_display_params)
        self.crit_luck_display = Label(pygame.Vector2(), **stats_display_params)
        self.agility_display = Label(pygame.Vector2(), **stats_display_params)

        # on affiche tous les éléments
        self.bind_several_widget(
            self.fps_label,
            button_menu,

            self.fight_bar,
            self.battle_count,

            self.level_display,

            self.hp_display,
            self.atk_display,
            self.crit_multiplier_display,
            self.crit_luck_display,
            self.agility_display
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

        stats_button_rect = pygame.Rect(0, 170, 130, 40)
        stats_button_rect.x = self.draw_surface.get_width()/2 - stats_button_rect.width/2
        stats_button = Button(stats_button_rect, "Stats", Default_font(20), callback=self.stats_menu, text_color=pygame.Color(
            255, 255, 255), color=pygame.Color(120, 120, 120),  hover_color=pygame.Color(70, 70, 70))

        equipment_button_rect = pygame.Rect(0, 270, 200, 40)
        equipment_button_rect.x = self.draw_surface.get_width()/2 - equipment_button_rect.width/2
        equipment_button = Button(equipment_button_rect, "Equipment", Default_font(20), callback=self.equipment_menu, text_color=pygame.Color(
            255, 255, 255), color=pygame.Color(120, 120, 120),  hover_color=pygame.Color(70, 70, 70))
        
        play_menu_button_rect = pygame.Rect(0, 470, 100, 40)
        play_menu_button_rect.x = self.draw_surface.get_width()/2 - play_menu_button_rect.width/2
        play_menu_button = Button(play_menu_button_rect, "Quit", Default_font(20), callback=self.quit, text_color=pygame.Color(
            255, 255, 255), color=pygame.Color(120, 120, 120),  hover_color=pygame.Color(70, 70, 70))

        menu_label = Label(pygame.Vector2(40, 40), "MENU", Default_font(30), pygame.Color(255, 255, 255))

        self.bind_several_widget(
            menu_label,
            stats_button,
            equipment_button,
            close_button,
            previous_button,
            play_menu_button
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
        self.main_display()
        self.player_stats.remaining_points = points
        self.player_stats.stats = stats
        
    def quit(self):
        self.game.restart = True
        self.game.running = False
        
class Battle_ui:
    def __init__(self, ingame_menu:Ingame_menu):
        self.ingame_menu = ingame_menu
        self.x_max = self.ingame_menu.draw_surface.get_width()
        self.y_max = self.ingame_menu.draw_surface.get_height()

        self.last_time_row = 0
        self.printing = False 
        self.battle_ui_opened = False

    def update(self):
        if self.last_time_row + 400 < pygame.time.get_ticks() and self.printing:
            self.last_time_row = pygame.time.get_ticks()
            self.draw_rounds()
        
    def start_battle(self, last_battle=False):
        self.rounds = []
        self.rounds_labels = []
        self.displayed_rows = -1
        self.printing = True
        self.battle_ui_opened = True
        self.last_time_row = pygame.time.get_ticks()
        self.draw(last_battle)
        
    def draw(self, last_battle=False):
        self.ingame_menu.clear_widget()
        self.ingame_menu.set_background_color(pygame.Color(20, 20, 20, 150))
        self.ingame_menu.set_grab(True)
        
        close_or_skip_button = Button(pygame.Rect(0, 0, self.x_max, self.y_max), "", Default_font(20), self.close_or_skip_battle_ui, text_color=pygame.Color(
            0, 0, 0, 0), color=pygame.Color(0, 0, 0, 0),  hover_color=pygame.Color(0, 0, 0, 0))
        battle_label = Label(pygame.Vector2(40, 40), "BATTLE", Default_font(30), pygame.Color(255, 255, 255))
        
        if last_battle:
            self.ingame_menu.set_background_color(pygame.Color(50,40,20))
            battle_label.update_text("BOSS BATTLE")
        
        self.ingame_menu.bind_several_widget(
            close_or_skip_button,
            battle_label
        )
        
    def draw_rounds(self):
        for label in self.rounds_labels:
            self.ingame_menu.unbind_widget(label)
        self.rounds_labels = []
        self.displayed_rows += 1
        
        y = self.y_max - 100
        rows_nb = len(self.rounds)-1

        if rows_nb-self.displayed_rows == 0:
            self.printing = False

        for i in range(rows_nb-min(self.displayed_rows,rows_nb),rows_nb+1):
            window_width, window_height = pygame.display.get_window_size()
            
            if y > 50 and self.rounds != []:  # évite d'afficher des textes non visibles
                if self.rounds[i]["is_player"] == True:
                    label = Label(pygame.Vector2(100, y), self.rounds[i]["message"], Default_font(20), pygame.Color(127,255,127))
                else:
                    label = Label(pygame.Vector2(100, y), self.rounds[i]["message"], Default_font(20), pygame.Color(255,127,127))
                    label.coords.x = window_width - label.box.width - 100
                self.rounds_labels.append(label)
                self.ingame_menu.bind_widget(label)
                y -= 50
            else:
                return
    
    def add_round(self, is_player: bool, message: str):
        self.rounds.insert(0, {"is_player": is_player, "message": message})

    def close_or_skip_battle_ui(self):
        self.printing = False

        if self.displayed_rows < len(self.rounds)-1:
            self.displayed_rows = len(self.rounds)-1
            self.draw_rounds()
        else:
            self.battle_ui_opened = False
            self.ingame_menu.main_display()
            
class End_menu:
    def __init__(self, ingame_menu:Ingame_menu):
        self.ingame_menu = ingame_menu
    
    def start(self):
        self.ingame_menu.clear_widget()
        self.ingame_menu.set_background_color(pygame.Color(50, 40, 20))
        self.ingame_menu.set_grab(True)
        
        win_label = Label(pygame.Vector2(80,100), "YOU WIN !", Default_font(30),pygame.Color(255,255,255))
        thanks_label = Label(pygame.Vector2(40,200), "Thanks for playing our game !", Default_font(20),pygame.Color(255,255,255))
        credit_label = Label(pygame.Vector2(40,250), "Created by Spishewi and Mouthanos", Default_font(20),pygame.Color(255,255,255))
        
        self.ingame_menu.bind_several_widget(
            win_label,
            thanks_label,
            credit_label
        )


# des widgets custom souvent utilisé dans l'interface
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
