class Party:
    def __init__(self):
        self.members = []
    
    def add_member(self, character):
        self.members.append(character)
    
    def remove_member(self, character):
        if character in self.members:
            self.members.remove(character)
    
    def list_members(self):
        return [member.name for member in self.members]
    
    def get_member(self, name):
        for member in self.members:
            if member.name == name:
                return member
        return None