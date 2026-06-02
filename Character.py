class Character:
    def __init__(self, name, player_class, race, equipment, proficiencies, hp=10):
        self.name = name
        self.player_class = player_class
        self.race = race
        self.equipment = equipment
        self.proficiencies = proficiencies
        self.hp = hp
        self.alive = True
    
    def die(self):
        self.alive = False
        print(f"{self.name} has died.")
    
    def attack(self, target):
        # placeholder attack method, will be fleshed out later
        print(f"{self.name} attacks {target.name}!")