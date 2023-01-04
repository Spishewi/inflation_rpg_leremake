import json
from math import floor

class Equipment():
    # constantes
    max_level = {
        "armor":4,
        "sword":14,
        "ring":14
    }

    def __init__(self) -> None:
        # niveaux d'équipement par défaut
        self.money = 0
        self.level = {
            "armor":0,
            "sword":0,
            "ring":0
        }

    def save(self):
        """
        sauvegarde l'équipement actuel dans un fichier json
        """
        with open("../saves/equipment.json", "w") as f:
            json.dump({"money": self.money, "level": self.level}, f)

    def load(self):
        """
        charge l'equipement depuis un fichier json
        """
        try:
            with open("../saves/equipment.json", "r") as f:
                save = json.load(f)
        except FileNotFoundError:
            pass
        else:
            for k, v in save.items():
                if k == "money":
                    self.money = v
                elif k == "level":
                    self.level = v
            
    def upgrade_object(self, object_type:str):
        price = self.get_price(object_type,self.level[object_type])
        if  price <= self.money :
            self.level[object_type] += 1
            self.money -= price
            self.save()
        
    def __str__(self) -> str:
        return "\n".join([f"{k}: {v}" for k, v in vars(self).items()])

    def get_price(self,object_type:str, nb:int):
        return floor((20*(1+nb*(10/(Equipment.max_level[object_type]+1))))/1.1)**2/2




if __name__ == "__main__":
    e = Equipment()
    e.armor_level = 5
    e.save()
    del e

    e = Equipment()
    e.load()
    print(e)
