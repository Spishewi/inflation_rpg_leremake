from __future__ import annotations
from typing import TYPE_CHECKING

import math

from gameplay.battle import Entity

if TYPE_CHECKING:
    from gameplay.equipment import Equipment

class Stats:
    # default values
    default_value = {
        "pv":100,
        "atk":100,
        "crit_luck":0,
        "speed":100 
    }
    

    def __init__(self, equipment: Equipment) -> None:
        
        # l'équipement
        self.equipment = equipment

        # les points
        self.stats = {
            "pv":0,
            "atk":0,
            "crit_luck":0,
            "speed":0
        }
        self.remaining_points = 0

        # l'experience
        self.xp = 1

    def get_player_entity(self):
        player = Entity(
            pv_max = (self.stats["pv"] + Stats.default_value["pv"])*(1 + self.equipment.level["armor"]),
            atk = (self.stats["atk"] + Stats.default_value["atk"])*(1 + self.equipment.level["sword"] / 7),
            crit_luck = 1-(1/math.sqrt(1 + self.stats["crit_luck"] + Stats.default_value["crit_luck"])),
            crit_multiplier = 1 + self.equipment.level["ring"] / 7,
            speed = self.stats["speed"] + self.default_value["speed"]
            )
        return player

    def handle_win(self, enemy_level: int):
        level_difference = enemy_level - self.xp
        print(self.xp, enemy_level, level_difference, 2**(level_difference + 5))
        self.xp += 2**(level_difference + 5) # équation à vérifier
        self.remaining_points += int(math.sqrt(self.xp) - (self.stats["pv"] + self.stats["atk"] + self.stats["crit_luck"] + self.stats["pv"]))
        
        print((self.xp,self.remaining_points))

        self.equipment.money = self.xp # temporaire aussi


    
