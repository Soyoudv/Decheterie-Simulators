import json

# Charger le fichier
with open("code/listeDechet.json", "r") as f:
    data = json.load(f)
    
nb = int(input("saisir le nombre de dechet que vous souhaitez ajouter "))
cpt = 0
while cpt!= nb:
    dechet = input("saisir votre dechet a rentrer ")
    bennes = input("saisir votre dechet a rentrer ")
    if dechet not in data["dechets"]:
        data["dechets"].append(str(dechet))
        cpt +=1
    else:
        print("le dechet est deja dans la base de donnée")
        

# Sauvegarder
with open("code/listeDechet.json", "w") as f:
    json.dump(data, f, indent=4)