import requests
from console_utils import cprint as print

def display_spell(spell_data):
    print(f"Name: {spell_data['name']}", style="bold")
    print(f"Level: {spell_data['level']}")
    print(f"Index: {spell_data['index']}")
    print(f"URL: {spell_data['url']}")
    print()

def main():
    url = "https://www.dnd5eapi.co/api/2014/spells"
    headers = {'Accept': 'application/json'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        spells_data = response.json()
        spells = spells_data['results']

        print("Welcome to the D&D 5e Spellbook!", style="bold green")
        print(f"Total Spells: {spells_data['count']}\n")

        while True:
            print("Commands:", style="bold cyan")
            print("1 - List all spells")
            print("2 - Search for a spell by name")
            print("3 - Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                print("\nList of Spells:", style="yellow")
                for spell in spells:
                    display_spell(spell)
            elif choice == '2':
                spell_name = input("Enter the spell name: ").lower()
                matching_spells = [spell for spell in spells if spell_name in spell['name'].lower()]
                print("\nMatching Spells:", style="yellow")
                for spell in matching_spells:
                    display_spell(spell)
            elif choice == '3':
                print("Goodbye!", style="bold green")
                break
            else:
                print("Invalid choice. Please select a valid option.\n", style="bold red")
                

if __name__ == "__main__":
    main()