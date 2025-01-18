from PIL import Image
from math import sqrt
from random import randint
import numpy as np
from sklearn.cluster import KMeans


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
    palette = []
    for centroid in centroids:
        x, y, z = centroid
        x, y, z = int(min(255, x)), int(min(255, y)), int(min(255, z))
        palette.append((x, y, z))
    return palette


def rep_palette(refs):
    """Affiche dans une fenêtre Tkinter de carrés de dimension 50x50 les couleurs de la palette"""
    import tkinter as tk

    fen = tk.Tk()
    fen.title("Palette de couleurs")
    i_max = round(sqrt(len(refs))) + 1
    for i, ref in enumerate(refs):
        x, y, z = ref
        couleur = "#%02x%02x%02x" % (x, y, z)
        cadre = tk.Frame(fen, bg=couleur, width=50, height=50)
        cadre.grid(row=i // i_max, column=i % i_max)
    fen.mainloop()


def construit_matrice_disque(rayon_max):
    """Construit une matrice de disque de rayon pas//2"""
    matrice = []
    for rayon in range(rayon_max):
        matrice_disque = []
        for dx in range(-rayon, rayon):
            for dy in range(-rayon, rayon):
                if dx**2 + dy**2 < rayon**2:
                    matrice_disque.append((dx, dy))
        matrice.append(matrice_disque)
    return matrice


def construit_destination(img, palette, pas, alea=4):
    """Construit une image de destination de mêmes dimensions que l'image source sur fond blanc"""
    alea = max(1, alea)
    dim_x, dim_y = img.size
    img_dest = Image.new("RGB", (dim_x, dim_y), (255, 255, 255))
    rayon_max = max(2, round(2 * pas)) + 1
    matrice_disques = construit_matrice_disque(rayon_max)
    print("  Fin de la construction de la matrice de disques")
    for x in range(pas // 2, dim_x, pas):
        for y in range(pas // 2, dim_y, pas):
            var_x = randint(-pas // alea, pas // alea)
            var_y = randint(-pas // alea, pas // alea)
            rayon = round(2 * pas - randint(0, 10 * pas // alea) / 20)
            couleur_pixel = img.getpixel((x, y))
            ref_proche = ref_plus_proche(couleur_pixel, palette)
            # Dessine un cercle de couleur (x, y, z) de rayon aléatoire
            for dx, dy in matrice_disques[rayon]:
                X = x + dx + var_x
                Y = y + dy + var_y
                if 0 <= X < dim_x and 0 <= Y < dim_y:
                    img_dest.putpixel((X, Y), ref_proche)
    return img_dest


if __name__ == "__main__":
    from fichiers import *

    NB_COULEURS_PALETTE = 8
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
