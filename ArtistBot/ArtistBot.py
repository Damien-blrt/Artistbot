from osgeo.gdalconst import *
from osgeo import gdal
import numpy as np
import pyautogui
import time
import tkinter as tk
from tkinter import messagebox
from pynput import mouse  # Importation de pynput pour détecter les clics


class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Menu de configuration")

        # Variables pour stocker les coordonnées et la taille
        self.palette_positions = {}
        self.canvas_width = None
        self.canvas_height = None
        self.canvas_top_left = None  # Coin supérieur gauche de la toile

        # Charger l'image à recréer
        self.filename = "./image.png"
        self.ds = gdal.Open(self.filename, GA_ReadOnly)
        if self.ds is None:
            messagebox.showerror("Erreur", "Impossible d'ouvrir l'image")
            exit(1)
        print("L'image a été ouverte avec succès")
        self.nbColonnes = self.ds.RasterXSize
        self.nbLignes = self.ds.RasterYSize
        self.nbBands = self.ds.RasterCount

        # Lire les bandes (RGB)
        self.data = self.ds.ReadAsArray()
        if self.data.shape[0] == 4:
            self.data = self.data[:3, :, :]
        self.data = np.transpose(self.data, (1, 2, 0))

        # Définition des couleurs fixes (RGB)
        self.colors = {
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

        self.color_names = list(self.colors.keys())
        self.color_values = np.array(list(self.colors.values()))

        # Interface
        self.instruction_label = tk.Label(root, text="Cliquez sur les boutons pour configurer.", font=("Arial", 14))
        self.instruction_label.pack(pady=10)

        # Récupérer les coordonnées des couleurs
        self.get_palette_button = tk.Button(root, text="Récupérer les coordonnées de la palette", command=self.get_palette_coordinates)
        self.get_palette_button.pack(pady=5)

        # Définir la taille de la toile
        self.get_canvas_button = tk.Button(root, text="Définir la taille de la toile", command=self.get_canvas_size)
        self.get_canvas_button.pack(pady=5)

        # Commencer à dessiner
        self.start_drawing_button = tk.Button(root, text="Commencer à dessiner", command=self.start_drawing)
        self.start_drawing_button.pack(pady=5)

    def on_click(self, x, y, button, pressed):
        """
        Fonction appelée lorsqu'un clic de souris est détecté.
        """
        if pressed:  # On ne s'intéresse qu'au moment où le bouton est pressé
            self.last_click_position = (x, y)
            return False  # Arrêter l'écouteur après un clic

    def get_click_position(self):
        """
        Attend un clic de souris et retourne la position du clic.
        """
        self.last_click_position = None
        with mouse.Listener(on_click=self.on_click) as listener:
            listener.join()  # Attendre un clic
        return self.last_click_position

    def get_palette_coordinates(self):
        self.palette_positions = {}
        self.instruction_label.config(text="Cliquez sur chaque couleur de la palette.")
        time.sleep(2)  # Laisser le temps à l'utilisateur de se préparer

        for color in self.color_names:
            self.instruction_label.config(text=f"Cliquez sur la couleur: {color}")
            messagebox.showinfo("Récupérer la couleur", f"Cliquez sur la couleur {color} dans l'application externe.")
            x, y = self.get_click_position()  # Attendre un clic
            if x is not None and y is not None:
                self.palette_positions[color] = (x, y)
                print(f"{color}: ({x}, {y})")  # Debug

        self.instruction_label.config(text="Les positions de la palette sont enregistrées.")

    def get_canvas_size(self):
        self.instruction_label.config(text="Cliquez sur les coins de la toile.")
        messagebox.showinfo("Coin supérieur gauche", "Cliquez sur le coin supérieur gauche de la toile, puis appuyez sur OK.")
        x1, y1 = self.get_click_position()  # Attendre un clic
        messagebox.showinfo("Coin inférieur droit", "Cliquez sur le coin inférieur droit de la toile, puis appuyez sur OK.")
        x2, y2 = self.get_click_position()  # Attendre un clic

        self.canvas_width = x2 - x1
        self.canvas_height = y2 - y1
        self.canvas_top_left = (x1, y1)  # Enregistrer le coin supérieur gauche

        self.instruction_label.config(text=f"Dimensions de la toile : Largeur={self.canvas_width}, Hauteur={self.canvas_height}")
        print(f"Toile : Coin supérieur gauche=({x1}, {y1}), Largeur={self.canvas_width}, Hauteur={self.canvas_height}")  # Debug

    def normalisation_couleur(self, pixel):
        ecart = np.linalg.norm(self.color_values - pixel, axis=1)
        return self.color_values[np.argmin(ecart)]

    def start_drawing(self):
        if not self.palette_positions:
            messagebox.showerror("Erreur", "Les coordonnées de la palette doivent être définies avant de dessiner.")
            return
        if self.canvas_top_left is None or self.canvas_width is None or self.canvas_height is None:
            messagebox.showerror("Erreur", "La taille de la toile doit être définie avant de dessiner.")
            return

        self.instruction_label.config(text="Démarrage du dessin...")
        time.sleep(2)  # Laisser le temps à l'utilisateur de se préparer

        x1, y1 = self.canvas_top_left
        last_color = None  # Stocke la dernière couleur sélectionnée

        for i in range(self.nbLignes):
            for j in range(self.nbColonnes):
                # Trouver la couleur la plus proche
                pixel_color = self.data[i, j]
                normalized_color = self.normalisation_couleur(pixel_color)
                color_index = np.argmin(np.linalg.norm(self.color_values - normalized_color, axis=1))
                color_name = self.color_names[color_index]

                # Sélectionner la couleur si elle a changé
                if color_name != last_color:
                    palette_x, palette_y = self.palette_positions[color_name]
                    pyautogui.click(palette_x, palette_y)
                    last_color = color_name  # Mettre à jour la dernière couleur utilisée
                    time.sleep(0.02)  # Délai court pour éviter les erreurs

                # Calculer la position du pixel sur la toile
                pixel_x = x1 + j * (self.canvas_width // self.nbColonnes) + (self.canvas_width // self.nbColonnes) // 2
                pixel_y = y1 + i * (self.canvas_height // self.nbLignes) + (self.canvas_height // self.nbLignes) // 2
                pyautogui.click(pixel_x, pixel_y)
                time.sleep(0.005)  # Réduction du délai pour accélérer le dessin

        self.instruction_label.config(text="Dessin terminé.")



# Lancer l'interface graphique Tkinter
root = tk.Tk()
app = DrawingApp(root)
root.mainloop()

