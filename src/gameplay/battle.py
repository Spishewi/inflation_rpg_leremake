from __future__ import annotations
from typing import TYPE_CHECKING

import random
import pygame

# Import seulement pour les type-hint (opti)
if TYPE_CHECKING:
    from gameplay.equipment import Equipment
    from engine.map_manager import MapManager
    from gameplay.stats import Stats

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
    def __init__(self, player: Entity, level_range) -> None:
        # on stock le joueur 
        self.player = player
        # on choisi le niveau de l'ennemi
        self.enemy_level = random.choice(level_range)
        #print(enemy_level)
        # On crée l'ennemi
        self.enemy = Entity(
            pv_max=self.enemy_level*10,
            atk=self.enemy_level*10,
            crit_luck=0.5,
            crit_multiplier=1.2,
            speed=self.enemy_level*10
            )
    
    def player_atk_first(self):
        self.enemy.get_attacked(self.player.attack())
        if self.enemy.isalive():
            self.player.get_attacked(self.enemy.attack())

    def enemy_atk_first(self):
        # on fait attaquer l'ennemi en premier
        self.player.get_attacked(self.enemy.attack())
        if self.player.isalive():
            self.enemy.get_attacked(self.player.attack())

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
    number_of_battles = 15
    def __init__(self, equipment: Equipment) -> None:

        self.equipment = equipment

        self.battle_chance = 0
        self.max_battle_chance = 100
        self.must_trigger_battle = False
        self.last_try_to_trigger_battle = pygame.time.get_ticks()

        self.remaining_battle = Battle_manager.number_of_battles

        self.current_battle = None
        
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
            self.current_battle = Battle(player_stats.get_player_entity(), map_manager.get_level_range("map", player_coords))

        elif self.current_battle != None:
            round_result = self.current_battle.process_round()
            if round_result.status == Round_result.WIN:
                self.remaining_battle -= 1
                player_stats.handle_win(self.current_battle.enemy_level)
            elif round_result.status == Round_result.LOST:
                self.remaining_battle -= 3
            if round_result.status != Round_result.NOT_COMPLETED:
                print(round_result.status)
                self.current_battle = None
                if self.remaining_battle <= 0:
                    print("FIN DU JEU")
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

