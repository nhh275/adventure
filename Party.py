from console_utils import cprint as print
class Party:
    def __init__(self):
        self.members = [] # members[0] is always the user-created character
    
    def add_member(self, character):
        self.members.append(character)
    
    def remove_member(self, character):
        if character in self.members:
            self.members.remove(character)
        
    def heal_party(self):
        for member in self.members:
            member.hp = member.maxHP # reset to full health, typically after combat win
            member.alive = True
            if len(member.ammo) > 0:
                member.ammo['quantity'] = member.ammo['maxQuantity'] # refill ammo
    
    def give_xp(self, xpList):
        print(f"The party gained {sum(xpList)}XP!\n", style="bold yellow")
        for member in self.members:
            member.xp += sum(xpList)
            member.check_level_up() # check for a ding
    
    def level_party_up(self):
        for member in self.members:
            member.check_level_up(freeLevel=True)
    
    def show_party_names(self):
        print("Your party is now as follows:",style="cyan")
        for member in self.members:
            print(f"{member.name} (lv{member.level})",style="green")
    
    def get_member_by_name(self, name):
        for member in self.members:
            if member.name.lower().strip() == name.lower().strip():
                return member # Character object