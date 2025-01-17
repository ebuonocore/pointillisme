from PIL import Image
from math import sqrt
from random import randint
import numpy as np
from sklearn.cluster import KMeans


def ouvre(fichier):
    """Ouvre le fichier image au format PNG ou JPEG et renvoie l'objet image correspondant"""
    return Image.open(fichier)


def distance(couleur_A, couleur_B):
    """Calcule la distance entre deux couleurs (R,V,B)"""
    return sqrt(
        (couleur_A[0] - couleur_B[0]) ** 2
        + (couleur_A[1] - couleur_B[1]) ** 2
        + (couleur_A[2] - couleur_B[2]) ** 2
    )


def ref_plus_proche(couleur, refs):
    """Renvoie la référence la plus proche de la couleur"""
    dist_min = distance(couleur, refs[0])
    ref_min = refs[0]
    for ref in refs:
        dist = distance(couleur, ref)
        if dist < dist_min:
            dist_min = dist
            ref_min = ref
    return ref_min


def rep_palette(refs):
    """Affiche dans une fenêtre Tkinter de carrés de dimension 50x50 les couleurs de la palette"""
    import tkinter as tk

    fen = tk.Tk()
    fen.title("Palette de couleurs")
    i_max = round(sqrt(len(refs))) + 1
    for i, ref in enumerate(refs):
        x, y, z = ref
        x, y, z = int(min(255, x)), int(min(255, y)), int(min(255, z))
        couleur = "#%02x%02x%02x" % (x, y, z)
        cadre = tk.Frame(fen, bg=couleur, width=50, height=50)
        cadre.grid(row=i // i_max, column=i % i_max)
    fen.mainloop()


def construit_destination(img, palette, pas, alea=4):
    """Construit une image de destination de mêmes dimensions que l'image source sur fond blanc"""
    dim_x, dim_y = img.size
    img_dest = Image.new("RGB", (dim_x, dim_y), (255, 255, 255))
    for x in range(pas // 2, dim_x, pas):
        for y in range(pas // 2, dim_y, pas):
            var_x = randint(-pas // alea, pas // alea)
            var_y = randint(-pas // alea, pas // alea)
            var_r = randint(0, pas // alea)
            couleur_pixel = img.getpixel((x, y))
            ref_proche = ref_plus_proche(couleur_pixel, palette)
            couleur = (int(x) for x in ref_proche)
            print("*** *** ", couleur, ref_proche)
            # Dessine un cercle de couleur (x, y, z) de rayon pas//2
            for dx in range(-pas // 2, pas // 2):
                for dy in range(-pas // 2 - var_r, pas // 2 + var_r):
                    if dx**2 + dy**2 < ((pas // 2) + var_r) ** 2:
                        X = x + dx + var_x
                        Y = y + dy + var_y
                        if 0 <= X < dim_x and 0 <= Y < dim_y:
                            img_dest.putpixel((X, Y), couleur)
    return img_dest


def sélectionne_fichier():
    """Ouvre une fenêtre de dialogue pour sélectionner un fichier image"""
    from tkinter import filedialog

    fichier = filedialog.askopenfilename(
        title="Ouvrir une image",
        filetypes=[("Fichiers JPEG", "*.jpg"), ("Fichiers PNG", "*.png")],
    )
    return fichier


def sépare_dossier_fichier(chemin):
    """Renvoie le tuple constitué du dossier et du fichier et de son extension"""
    import os

    dossier, fichier = os.path.split(chemin)
    dossier = dossier + "/" if dossier else ""
    nom, extension = os.path.splitext(fichier)
    return dossier, nom, extension


def enregistre(img, fichier):
    img.save(fichier)


def échantillon(img, N):
    """Renvoie N pixels de l'image img afin de créer un échantillon"""
    dim_x, dim_y = img.size
    nb_pixels = dim_x * dim_y
    if N >= nb_pixels:
        pas = 1
    else:
        pas = sqrt(nb_pixels // N)
    domaine_x = [int(i * pas) for i in range(int(dim_x // pas) + 1)]
    if domaine_x[-1] > dim_x:
        domaine_x = domaine_x[:-1]
    domaine_y = [int(i * pas) for i in range(int(dim_y // pas) + 1)]
    if domaine_y[-1] > dim_y:
        domaine_y = domaine_y[:-1]
    couleurs = []
    for x in domaine_x:
        for y in domaine_y:
            couleur_pixel = img.getpixel((x, y))
            couleurs.append(couleur_pixel)
    return np.array(couleurs)


def construit_palette(image, nb_pixels_echantillon=10000, nb_couleurs=16):
    """Construit une palette de nb_couleurs couleurs à partir d'un échantillon selon l'algorithme de KMeans
    image : image source
    nb_couleurs : nombre de couleurs souhaitées de la palette
    nb_pixels_echantillon : nombre de pixels de l'échantillon
    """
    couleurs_échantillon = échantillon(image, nb_pixels_echantillon)
    model_KMeans = KMeans(n_clusters=nb_couleurs, random_state=0)
    model_KMeans.fit(couleurs_échantillon)
    centroids = model_KMeans.cluster_centers_
    # rep_palette(centroids)
    return centroids


if __name__ == "__main__":
    NB_COULEURS_PALETTE = 16
    NB_PIXELS_ECHANTILLON = 1000

    # Sélection du fichier
    fichier = sélectionne_fichier()
    dossier, nom_fichier, extension = sépare_dossier_fichier(fichier)
    chemin = dossier + nom_fichier + extension
    photo = ouvre(chemin)
    taille_image = photo.size

    print(f"Dimension de {nom_fichier} : {taille_image}")
    palette = construit_palette(photo, NB_PIXELS_ECHANTILLON, NB_COULEURS_PALETTE)
    rep_palette(palette)
