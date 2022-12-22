import random
import math
import pygame

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
        enemy_level = random.choice(level_range)
        #print(enemy_level)
        # On crée l'ennemi
        self.enemy = Entity(
            pv_max=enemy_level*100,
            atk=enemy_level*10,
            crit_luck=0.5,
            crit_multiplier=0.2,
            speed=enemy_level*10
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
    def __init__(self) -> None:
        self.battle_chance = 0
        self.max_battle_chance = 100
        self.must_trigger_battle = False
        self.last_try_to_trigger_battle = pygame.time.get_ticks()

        self.remaining_battle = 30

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

            print(self.battle_chance)
            print(self.must_trigger_battle)
    
    def try_to_trigger_battle(self):
        # remet à jour cette variable (pour pas essayer 60 fois par secondes et lancer instantanément des combats)
        self.last_try_to_trigger_battle = pygame.time.get_ticks()
        # on prend un nombre aléatoire entre 0 et 2
        random_number = random.random() * 2

        # s'il est plus petit que le ratio entre la chance actuelle et la chance maximale
        if random_number < self.battle_chance / self.max_battle_chance:
            # un combat doit être lancé
            self.must_trigger_battle = True





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

