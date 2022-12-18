import random
import math

class Entity():
    def __init__(self, pv_max: int, atk: float, crit_luck: float, crit_multiplier: float, speed: float) -> None:
        self._pv_max = int(pv_max)
        self._atk = float(atk)
        self._pv = self._pv_max
        self._crit_luck = float(crit_luck)
        self._crit_multiplier = float(crit_multiplier)
        self.speed = float(speed)

    def isalive(self) -> bool:
        return self._pv <= 0

    def attack(self) -> float:
        damage = self._atk
        if random.random() < self._crit_luck:
            damage *= self._crit_multiplier
        return damage

    def get_attacked(self, damage: float) -> None:
        self._pv -= damage

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
        self.player = player
        enemy_level = random.choice(level_range)
        self.enemy = Entity(
            pv_max=enemy_level*1000,
            atk=enemy_level*10,
            crit_luck=0.5,
            crit_multiplier=0.2,
            speed=enemy_level*10
            )
    
    def player_atk_first(self):
        self.enemy.get_attacked(self.player.attack())
        self.player.get_attacked(self.enemy.attack())

    def enemy_atk_first(self):
        self.player.get_attacked(self.enemy.attack())
        self.enemy.get_attacked(self.player.attack())
        
    def process_round(self):
        if self.player.speed > self.enemy.speed:
            self.player_atk_first()
        elif self.player.speed < self.enemy.speed:
            self.enemy_atk_first()
        else:
            if random.random() > 0.5:
                self.player_atk_first()
            else:
                self.enemy_atk_first()
