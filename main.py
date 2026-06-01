import requests

print("\nWelcome to your grand adventure!")
playerName = input("What is your name, adventurer? ").title() # unsanitised 
url = "https://www.dnd5eapi.co/api/2014/classes"
response = requests.get(url)
data = response.json()
print("\n")
for i in range(data['count']):
    print(data['results'][i]['name'])

chosenClass = str(input("\nWhich class takes your fancy today? ")).strip().lower()
url = f"https://www.dnd5eapi.co/api/2014/classes/{chosenClass}"
response = requests.get(url)
classData = response.json()


url = "https://www.dnd5eapi.co/api/2014/races"
response = requests.get(url)
data = response.json()
print("\n")
for i in range(data['count']):
    print(data['results'][i]['name'])
    
chosenRace = str(input("\nWhich race are you? ")).strip().lower()
url = f"https://www.dnd5eapi.co/api/2014/races/{chosenRace}"
response = requests.get(url)
raceData = response.json()

print(f"\n{playerName} the mighty {raceData['name']} {classData['name']}! A wonderful choice.")

