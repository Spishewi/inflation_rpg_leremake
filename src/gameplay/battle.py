from __future__ import annotations
from typing import TYPE_CHECKING

import random
import pygame

#from display.ingame_menu import Ingame_menu
# Import seulement pour les type-hint (opti)
if TYPE_CHECKING:
    from gameplay.equipment import Equipment
    from engine.map_manager import MapManager
    from gameplay.stats import Stats
    from display.ingame_menu import Battle_ui
    

class Entity():
    def __init__(self, pv_max: int, atk: float, crit_luck: float, crit_multiplier: float, speed: float) -> None:
        self._pv_max = int(pv_max)
        self._atk = float(atk)
        self._pv = self._pv_max
        self._crit_luck = float(crit_luck)
        self._crit_multiplier = float(crit_multiplier)
        self.speed = float(speed)

    def isalive(self) -> bool:
        return self._pv > 0

    def attack(self) -> float:
        damage = self._atk
        if random.random() < self._crit_luck:
            damage *= self._crit_multiplier
        return damage

    def get_attacked(self, damage: float) -> None:
        self._pv -= damage

    def __str__(self) -> str:
        return f"""
        pv: {self._pv}/{self._pv_max}
        atk: {self._atk}
        crit_luck: {self._crit_luck}
        crit_multiplier: {self._crit_multiplier}
        speed: {self.speed}
        """

class Round_result:
    # status constants
    LOST = "lost"
    WIN = "win"
    NOT_COMPLETED = "not_completed"

    def __init__(self, player: Entity, enemy: Entity) -> None:
        self.player = player
        self.enemy = enemy
        if not player.isalive():
            self.status = Round_result.LOST
        elif not enemy.isalive():
            self.status = Round_result.WIN
        else:
            self.status = Round_result.NOT_COMPLETED

class Battle():
    def __init__(self, player: Entity, level_range, battle_ui) -> None:
        # on stock le joueur 
        self.player = player
        # on choisi le niveau de l'ennemi
        self.enemy_level = random.choice(level_range)
        print(self.enemy_level)
        # On crée l'ennemi

        enemy_points = self.enemy_level*15
        enemy_points_repartitions = random.random()/2 + 0.25

        self.enemy = Entity(
            pv_max=100+(11/2000)*(enemy_points*enemy_points_repartitions)**2,
            atk=10+(11/2000)*(enemy_points*(1-enemy_points_repartitions))**2,
            crit_luck=random.random()/2,
            crit_multiplier=1.2,
            speed=self.enemy_level*10
            )
        # on stock l'interface de bataille pour y afficher les informations
        self.battle_ui = battle_ui
    
    def player_atk_first(self):
        player_damages = self.player.attack()
        self.battle_ui.add_round(True, f"You attack, the enemy loses {int(player_damages)} hp")
        self.enemy.get_attacked(player_damages)
        
        if self.enemy.isalive():
            enemy_damages = self.enemy.attack()
            self.player.get_attacked(enemy_damages)
            self.battle_ui.add_round(False, f"The enemy attacks, you lose {int(enemy_damages)} hp")

    def enemy_atk_first(self):
        # on fait attaquer l'ennemi en premier
        enemy_damages = self.enemy.attack()
        self.player.get_attacked(enemy_damages)
        self.battle_ui.add_round(False, f"The enemy attacks, you lose {int(enemy_damages)} hp")
        
        if self.player.isalive():
            player_damages = self.player.attack()
            self.enemy.get_attacked(player_damages)
            self.battle_ui.add_round(True, f"You attack, the enemy loses {int(player_damages)} hp")

    def process_round(self):
        # on défini qui attaque en premier, et on fait attaquer.
        if self.player.speed > self.enemy.speed:
            self.player_atk_first()
        elif self.player.speed < self.enemy.speed:
            self.enemy_atk_first()
        else:
            if random.random() > 0.5:
                self.player_atk_first()
            else:
                self.enemy_atk_first()

        return Round_result(self.player, self.enemy)

class Battle_manager():
    number_of_battles = 30
    def __init__(self, battle_ui:Battle_ui) -> None:

        self.battle_chance = 0
        self.max_battle_chance =  25 # 100 TODO
        self.must_trigger_battle = False
        self.last_try_to_trigger_battle = pygame.time.get_ticks()

        self.remaining_battle = Battle_manager.number_of_battles

        self.current_battle = None
        
        self.battle_ui = battle_ui
        
        self.game_end = False

    def handle_player_movement(self, player_relative_movement: float) -> None:
        # on s'est déplacé, on a donc plus de chance de lancer un combat
        self.battle_chance += player_relative_movement

        # si la chance est au maximum, on lance le combat
        if self.battle_chance > self.max_battle_chance:
            self.must_trigger_battle = True
        # sinon, si ça fait plus d'une seconde qu'on a testé et que un déplacement a été effectué
        elif self.last_try_to_trigger_battle + 1000 < pygame.time.get_ticks() and player_relative_movement != 0:
            # on essaye de lancer un combat
            self.try_to_trigger_battle()
    
    def try_to_trigger_battle(self):
        # remet à jour cette variable (pour pas essayer 60 fois par secondes et lancer instantanément des combats)
        self.last_try_to_trigger_battle = pygame.time.get_ticks()
        # on prend un nombre aléatoire entre 0 et 2
        random_number = random.random() * 2

        # si la chance est plus grande que 1/4 de la chance max, et que le nb random est plus petit que le ratio entre la chance actuelle et la chance maximale
        if self.battle_chance > 0.25*self.max_battle_chance and random_number < self.battle_chance / self.max_battle_chance:
            # un combat doit être lancé
            self.must_trigger_battle = True
    
    def handle_battle(self, player_coords, map_manager: MapManager, player_stats: Stats):
        if self.must_trigger_battle and self.current_battle == None:
            # mise a jour des variables
            self.must_trigger_battle = False
            self.battle_chance = 0

            # demarrage d'un combat
            self.current_battle = Battle(player_stats.get_player_entity(), map_manager.get_level_range("map", player_coords), self.battle_ui)
            self.battle_ui.start_battle()

        elif self.current_battle != None:
            round_result = self.current_battle.process_round()
            if round_result.status == Round_result.WIN:
                self.remaining_battle -= 1
                player_stats.handle_win(self.current_battle.enemy_level)
                self.battle_ui.add_round(True, "YOU WIN")
            elif round_result.status == Round_result.LOST:
                self.remaining_battle -= 3
                self.battle_ui.add_round(False, "YOU LOOSE")
                
            if round_result.status != Round_result.NOT_COMPLETED:
                print(round_result.status)
                self.current_battle = None
                
        if self.remaining_battle <= 0:
            return True
                
        return False

            





# du debug
if __name__ == "__main__":
    player = Entity(
        pv_max=1500,
        atk=150,
        crit_luck=0.5,
        crit_multiplier=0.2,
        speed=150
    )

    battle = Battle(player, level_range=range(10, 15))
    round_result = battle.process_round()
    while round_result.status == Round_result.NOT_COMPLETED:
        round_result = battle.process_round()
    print(round_result.status)

