import os

# Récupérer le chemin absolu du script
chemin_absolu = os.path.abspath(__file__)

# Récupérer le chemin relatif du script
chemin_relatif = os.path.relpath(chemin_absolu)

print("Chemin absolu du script :", chemin_absolu)
print("Chemin relatif du script :", chemin_relatif)

# Spécifiez le chemin vers le dossier contenant les fichiers
dossier = os.path.dirname(chemin_absolu)

for nom_fichier in os.listdir(dossier):
    if nom_fichier.endswith('.ogg'):
        print(nom_fichier)
        try :
            id, _ = nom_fichier.split(' - ')
            nouveau_nom = f"{id}.ogg"
            os.rename(os.path.join(dossier, nom_fichier), os.path.join(dossier, nouveau_nom))
        except :
            pass

print("Renommage terminé !")
