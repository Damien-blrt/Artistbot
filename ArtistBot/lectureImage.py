from osgeo import gdal #permet de lire les images
from osgeo.gdalconst import * #permet d'utiliser les constantes de gdal
import numpy as np #importation de numpy pour les calculs
import matplotlib
matplotlib.use('TkCairo') #utilisation de TkCairo pour l'affichage des images
import matplotlib.pyplot as plt
import pyautogui
import time 

filename = "./image.png"  #chemin de l'image
ds = gdal.Open(filename, GA_ReadOnly) #ouverture de l'image
if ds is None:
    print("Impossible d'ouvrir l'image") #verification de l'ouverture de l'image
    exit(1) #sortie du programme (il n'y a pas de raison de continuer)
print("L'image a été ouverte avec succès") #message de confirmation

nbColonnes = ds.RasterXSize #nombre de colonnes
nbLignes = ds.RasterYSize #nombre de lignes
nbBands = ds.RasterCount #nombre de bandes

'''

Explication des bandes :
    Une image en niveaux de gris contient une seule bande (intensité lumineuse par pixel).
    Une image RGB contient 3 bandes :
        Bande 1 : Rouge (R)
        Bande 2 : Vert (G)
        Bande 3 : Bleu (B)
Une image satellite ou multispectrale peut contenir plusieurs bandes,
chacune correspondant à une longueur d'onde spécifique (infrarouge, UV, etc.).
ici ce programme ne prend en compte que les images RGB (3 bandes).

'''

print("Nombre de colonnes : ", nbColonnes) #affichage du nombre de colonnes
print("Nombre de lignes : ", nbLignes) #affichage du nombre de lignes
print("Nombre de bandes : ", nbBands) #affichage du nombre de bandes




# Lire toutes les bandes (R, G, B)
data = ds.ReadAsArray()  # Lire toutes les bandes

# Si 4 bandes sont présentes, on garde uniquement les trois premières
if data.shape[0] == 4:
    data = data[:3, :, :] #on garde les 3 premières bandes


# Transposer pour passer à l'ordre (lignes, colonnes, bandes)
data = np.transpose(data, (1, 2, 0)) #on pourrait renverser l'image en mettant (2, 1, 0) mais ce n'est pas ce qu'on veut ici




# Définition des couleurs fixes (RGB) on peut ajouter d'autres couleurs si on veut
colors = {
    "Rouge": (255, 0, 0),
    "Jaune": (255, 255, 0),
    "Bleu": (0, 0, 255),
    "Vert": (0, 255, 0),
    "Violet": (128, 0, 128),
    "Rose": (255, 105, 180),
    "Noir": (0, 0, 0),
    "Gris": (128, 128, 128),
    "Blanc": (255, 255, 255),
}

# Convertir le dictionnaire en un tableau NumPy (N, 3) avec N le nombre de couleurs
color_names = list(colors.keys())
color_values = np.array(list(colors.values()))

''' 
Explication du code ci-dessus

On a créé un dictionnaire de couleurs.
Dans ce dictionnaire, chaque clé est le nom d'une couleur en français,
et chaque valeur est un tuple représentant les composantes RGB (Rouge, Vert, Bleu) de cette couleur.

En Python, un dictionnaire est une structure de données qui associe des clés à des valeurs.
Les clés doivent être uniques et immuables, tandis que les valeurs peuvent être de n'importe quel type.
Les dictionnaires sont définis en utilisant des accolades "{}" et les paires clé-valeur sont séparées par des deux-points ":". 

Ensuite, on a créé deux listes à partir du dictionnaire :
- color_names : une liste contenant les noms des couleurs
- color_values : une liste contenant les valeurs RGB des couleurs

Enfin, on a converti la liste color_values en un tableau NumPy de dimensions (N, 3) où N est le nombre de couleurs.
Chaque ligne du tableau correspond à une couleur et contient les valeurs RGB de cette couleur.

'''


# Fonction pour trouver la couleur la plus proche d'un pixel donné
def normalisation_couleur(pixel):
    ecart = np.linalg.norm(color_values - pixel, axis=1) # calcule l'écart entre le pixel et chaque couleur (distance euclidienne)
    return color_values[np.argmin(ecart)] # np.argmin(distances) retourne l'indice de la couleur la plus proche, et color_values[...] renvoie la couleur correspondante.

new_data = np.zeros_like(data) # Créer un tableau de zéros de même taille que data
for i in range(nbLignes): # Parcourir les lignes
    for j in range(nbColonnes): # Parcourir les colonnes
        new_data[i, j] = normalisation_couleur(data[i, j]) # Remplacer chaque pixel par la couleur

# Affichage de l'image
plt.imshow(new_data)
plt.show()

'''
Petit point sur le travail des matrices qu'il est possible de faire avec numpy

data[data > 5] = 0
ça nous permettra de mettre à 0 toutes les valeurs de data qui sont supérieures à 5
data[data < 5] = 0
ça nous permettra de mettre à 0 toutes les valeurs de data qui sont inférieures à 5

concrètement, on peut faire des calculs sur les matrices de données pour les modifier,
ici on a juste modifier les valeurs de data pour que l'affichage sois différent (on a ignoré certaines valeurs)


voir l'artiste bot pour voir l'ensemble du programme sans commentaires

'''
