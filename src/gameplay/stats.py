from __future__ import annotations
from typing import TYPE_CHECKING

import math

from gameplay.battle import Entity

if TYPE_CHECKING:
    from gameplay.equipment import Equipment

class Stats:
    # default values
    default_pv = 100
    default_atk = 100
    default_crit_luck = 0
    default_speed = 100

    def __init__(self, equipment: Equipment) -> None:
        
        # l'équipement
        self.equipment = equipment

        # les points
        self.pv = 0
        self.atk = 0
        self.crit_luck = 0
        self.speed = 0

        self.remaining_points = 0
        
        # l'argent
        self.money = 0

        # l'experience
        self.xp = 1

    def get_player_entity(self):
        player = Entity(
            pv_max = (self.pv + Stats.default_pv)*(1 + self.equipment.armor_level),
            atk = (self.atk + Stats.default_atk)*(1 + self.equipment.sword_level / 7),
            crit_luck = 1-(1/math.sqrt(1 + self.crit_luck + Stats.default_crit_luck)),
            crit_multiplier = 1 + self.equipment.ring_level / 7,
            speed = self.speed + self.default_speed
            )
        return player

    def handle_win(self, enemy_level: int):
        level_difference = enemy_level - self.xp
        print(self.xp, enemy_level, level_difference, 2**(level_difference + 5))
        self.xp += 2**(level_difference + 5) # équation à vérifier
        self.remaining_points += math.sqrt(self.xp) - (self.pv + self.atk + self.crit_luck + self.speed)

        self.money = self.xp # temporaire aussi


    
