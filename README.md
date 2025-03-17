# ArtistBot

## Description
Ce projet est une application Python qui permet de recréer une image en dessinant automatiquement sur une application externe. L'utilisateur sélectionne les couleurs de la palette et définit la zone de dessin, puis le programme se charge de dessiner l'image pixel par pixel.

## Fonctionnalités
- Chargement d'une image à partir d'un fichier PNG.
- Sélection automatique des couleurs les plus proches en fonction d'une palette définie.
- Définition interactive des couleurs de la palette à l'aide de clics.
- Sélection de la zone de dessin via des clics de l'utilisateur.
- Automatisation du dessin en utilisant `pyautogui`.

## Prérequis
Avant d'exécuter ce programme, assurez-vous d'avoir installé les bibliothèques suivantes :

Gdal, osgeo

## Utilisation
1. Lancez le script Python :
   ```sh
   python ArtistBot.py
   ```
2. Suivez les instructions affichées dans l'interface graphique pour :
   - Définir les couleurs de la palette en cliquant sur chaque couleur.
   - Définir la zone de dessin en sélectionnant les coins de la toile.
   - Lancer le processus de dessin automatique.

## Structure du Code
- `DrawingApp` : Classe principale gérant l'interface et l'automatisation.
- `get_palette_coordinates()` : Permet de récupérer les positions des couleurs dans la palette.
- `get_canvas_size()` : Définit les dimensions de la toile où l'image sera dessinée.
- `start_drawing()` : Effectue le dessin automatique en cliquant sur les pixels correspondants.

## Limitations
- Nécessite une application de dessin ouverte et prête à l'emploi.
- La reconnaissance des couleurs est basée sur une correspondance approximative, ce qui peut entraîner de légères variations.
- La vitesse de dessin dépend du temps de réponse de l'ordinateur.

## Auteur
Développé par Damien Ballerat.

