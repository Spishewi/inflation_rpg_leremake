import json

class Equipment():
    # constantes
    max_armor_level = 4
    max_sword_level = 14
    max_ring_level = 14

    def __init__(self) -> None:
        # niveaux d'équipement par défaut
        self.armor_level = 0
        self.sword_level = 0
        self.ring_level = 0

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
        for k,v in save.items():
            setattr(self, k, v)

    def __str__(self) -> str:
        return "\n".join([f"{k}: {v}" for k, v in vars(self).items()])
    
    def get_dict(self):
        return{"sword":self.sword_level,"armor":self.armor_level,"ring":self.ring_level}

if __name__ == "__main__":
    e = Equipment()
    e.armor_level = 5
    e.save()
    del e

    e = Equipment()
    e.load()
    print(e)