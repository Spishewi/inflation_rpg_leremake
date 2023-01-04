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
        "atk":10,
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
        

        # l'experience
        self.lvl = 10
        self.remaining_points = 15 * self.lvl
        self.xp = 1
        self.xp_needed_lvl_up = 1000 * self.lvl


    def get_player_entity(self):
        player = Entity(
            pv_max = (self.stats["pv"] + Stats.default_value["pv"])*(1 + self.equipment.level["armor"]/5*10),
            atk = (self.stats["atk"] + Stats.default_value["atk"])*(1 + self.equipment.level["sword"]/15*10),
            crit_luck = math.sin((1-1/((self.stats["crit_luck"] + Stats.default_value["crit_luck"])/30+1))**10)*1.25,
            crit_multiplier = 1 + self.equipment.level["ring"] / 7,
            speed = self.stats["speed"] + self.default_value["speed"]
            )
        return player

    def handle_win(self, enemy_level: int):
        self.xp += enemy_level*2000 # équation à vérifier

        while self.xp >= self.xp_needed_lvl_up:
            self.lvl += 1
            self.xp -= self.xp_needed_lvl_up
            self.xp_needed_lvl_up = 1000 * self.lvl
            self.remaining_points += 15

        self.equipment.money = self.lvl**2


    
