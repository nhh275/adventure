from console_utils import cprint as print
class Party:
    def __init__(self):
        self.members = []
    
    def add_member(self, character):
        self.members.append(character)
    
    def remove_member(self, character):
        if character in self.members:
            self.members.remove(character)
    
    def get_member_by_name(self, name):
        for member in self.members:
            if member.name == name:
                return member
        return None
    
    def heal_party(self):
        for member in self.members:
            member.hp = member.maxHP # reset to full health, typically after combat win
            member.alive = True
    
    def give_xp(self, xpList):
        print(f"The party gained {sum(xpList)}XP!\n", style="bold yellow")
        for member in self.members:
            member.xp += sum(xpList)
            member.check_level_up() # check for a ding