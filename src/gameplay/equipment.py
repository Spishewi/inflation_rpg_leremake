import json

class Equipment():
    def __init__(self) -> None:
        self.armor_level = 0
        self.max_armor_level = 4
        self.weapon_level = 0
        self.max_weapon_level = 14
        self.ring_level = 0
        self.max_ring_level = 14

    def save(self):
        """
        sauvegarde l'équipement actuel dans un fichier json
        """
        with open("equipment.json", "w") as f:
            json.dump(vars(self), f)
    def load(self):
        """
        charge l'equipement depuis un fichier json
        """
        with open("equipment.json", "r") as f:
            save = json.load(f)
        for k,v in save.items():
            setattr(self, k, v)

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