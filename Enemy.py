class Enemy:
    def __init__(self, name, type, hp, dmg):
        self.name = name
        self.type = type
        self.hp = hp
        self.dmg = dmg
        self.alive = True
    
    def attack(self, target):
        target.hp -= self.dmg # armour calc
        if target.hp < 0:
            target.hp = 0
            target.die()
        
    def die(self):
        self.alive = False
        print(f"{self.name} has died.")