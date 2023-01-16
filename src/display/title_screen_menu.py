from __future__ import annotations # permet d'ajouter certaines choses non disponibles sur les vielles versions du lycée de python

from display.ui import UI, Button, Label, Default_font, Image
from gameplay.equipment import Equipment
from display.graphics import Objects_picture
from utils import number_to_str

import pygame
class Title_screen_menu(UI):
    """
    Cette classe gère le menu de titre et se sert de la classe UI pour afficher les éléments
    """
    def __init__(self, draw_surface: pygame.Surface, player_equipment:Equipment, first_game:bool) -> None:
        super().__init__(draw_surface)
        # On choisi la couleur de fond
        self.set_background_color(pygame.Color(50,40,20))
        self.draw_surface = draw_surface
        
        # On charge les sprites des objets et armures
        self.objects_images = Objects_picture("../graphics/weapons_and_armors")
        
        # On définit des attributs
        self.must_start = False
        self.must_quit = False
        
        self.images = []
        self.prices_labels = []
        self.upgrade_buttons = {}
        
        self.equipment = player_equipment
        # Si le menu de titre est ouvert suite à la fin de partie, c'est le menu d'équipment qui est ouvert
        if first_game:
            self.play_menu()
        else:
            self.equipment_menu()
        
        
    def play_menu(self):
        """
        Affichage du menu jouer
        """
        # On vide la fenêtre
        self.clear_widget()
        
        # On crée et affiche tous les éléments
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
     
    def update_equipment_widgets(self):
        """
        Met à jours l'affichage des images des objets, de leurs prix ainsi que de l'argent possédé
        """
        for image,k in self.images:
            image.update_image(self.objects_images.get_object_picture(k, self.equipment.level[k], 7))
        for label,k in self.prices_labels:
            label.update_text(f"Price : {number_to_str(self.equipment.get_price(k,self.equipment.level[k]))} $")
            if self.equipment.level[k] == Equipment.max_level[k]:
                self.unbind_widget(self.upgrade_buttons[k])
                max_button = Button(self.upgrade_buttons[k].rect,"max",Default_font(20),callback=None,text_color=pygame.Color(255,255,255),color=pygame.Color(90,90,90))
                self.bind_widget(max_button)
        self.money_label.update_text(f"You have : {number_to_str(self.equipment.money)} $")
    
    def equipment_menu(self) -> None:
        """
        Affichage du menu équipement
        """
        self.clear_widget()
        
        # On crée et affiche tous les éléments
        self.rect = pygame.Rect(0,20,40,40)
        self.rect.x = self.draw_surface.get_width() - self.rect.width - 20

        close_button = Button(self.rect,"X",Default_font(20),callback=self.play_menu, text_color=pygame.Color(255, 255, 255), color=pygame.Color(120, 120, 120),  hover_color= pygame.Color(70, 70, 70))
        
        equipment_label = Label(pygame.Vector2(40, 40), "EQUIPMENT",Default_font(30), pygame.Color(255, 255, 255))
        self.money_label = Label(pygame.Vector2(400, 40), f"You have : {number_to_str(self.equipment.money)} $", Default_font(20), pygame.Color(255, 255, 255))
            
        self.bind_several_widget(
            equipment_label,
            close_button,
            self.money_label
        )

        self.images = []
        self.prices_labels = []
        self.upgrade_buttons = {}
        
        x = 150
        # Pour tous les objets et leur niveau :
        for k,v in self.equipment.level.items():
            # On affiche leur image, leur prix et le bouton pour les améliorer
            object_image = Image(self.objects_images.get_object_picture(k, v, 7), pygame.Vector2(x+60, 200))
            self.images.append((object_image,k))
            
            price_label = Label(pygame.Vector2(x, 350), f"Price : {number_to_str(self.equipment.get_price(k,v))} $", Default_font(20), pygame.Color(255,255,255))
            self.prices_labels.append((price_label,k))
            
            upgrade_button = Button(pygame.Rect(x, 400, 250, 100), "Upgrade", Default_font(20), callback=None, text_color=pygame.Color(255, 255, 255), color=pygame.Color(120, 120, 120),  hover_color= pygame.Color(70, 70, 70))
            upgrade_button.set_callback(self.upgrade_object, k)
            self.upgrade_buttons[k] = upgrade_button
            
            self.bind_several_widget(
                object_image,
                price_label,
                upgrade_button
            )
            # Chaque objet est décalé verticalement
            x += 350

        self.update_equipment_widgets()
        
    def upgrade_object(self,object_type):
        """
        Améliore l'objet
        """
        self.equipment.upgrade_object(object_type)
        self.update_equipment_widgets()
    
    def set_game_starting(self):
        """
        Permet de lancer la partie
        """
        self.must_start = True    
    
    def set_must_quit(self):
        """
        Permet de fermer la fenêtre
        """
        self.must_quit = True