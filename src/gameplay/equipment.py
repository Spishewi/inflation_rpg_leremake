import json


class Equipment():
    # constantes
    max_armor_level = 4
    max_sword_level = 14
    max_ring_level = 14

    def __init__(self) -> None:
        # niveaux d'équipement par défaut
        self.money = 0
        self.level = {
            "armor":0,
            "sword":0,
            "ring":0
        }
        self.prices = {
            "sword":[1,10,100,1000,10000,100000,1000000,10000000,100000000,1000000000,10000000000,100000000000,1000000000000,10000000000000,100000000000000],
            "armor":[1, 100, 1500, 25000,100000],
            "ring":[i for i in range(15)]
        }

    def save(self):
        """
        sauvegarde l'équipement actuel dans un fichier json
        """
        with open("../saves/equipment.json", "w") as f:
            json.dump(vars(self), f)

    def load(self):
        """
        charge l'equipement depuis un fichier json
        """
        with open("../saves/equipment.json", "r") as f:
            save = json.load(f)
        for k, v in save.items():
            setattr(self, k, v)
            
    def upgrade_object(self, object_type:str):
        if self.prices[object_type][self.level[object_type]+1] <= self.money:
            self.level += 1

    def __str__(self) -> str:
        return "\n".join([f"{k}: {v}" for k, v in vars(self).items()])


if __name__ == "__main__":
    e = Equipment()
    e.armor_level = 5
    e.save()
    del e

    e = Equipment()
    e.load()
    print(e)
