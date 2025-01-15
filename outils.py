from PIL import Image
from math import sqrt
from random import randint


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


def ref_palette(nb_ref):
    """Renvoie la liste de nb_ref couleurs placées régulièrement dans un espace à 3 dimensions"""
    nb_ref = max(8, nb_ref)
    # Une référence est caractérise par (x, y, z, p). Où x, y, z sont les coordonnées et p le poids.
    ref = []
    # Calcul du nombre de segments unitaires par dimension
    nb_segments = max(1, int(nb_ref ** (1 / 3)))
    matrice = [[1, 1, 1], [0, 1, 1], [0, 0, 1]]
    nb_segments_x, nb_segments_y, nb_segments_z = nb_segments, nb_segments, nb_segments
    for dx, dy, dz in matrice:
        if nb_ref >= nb_segments * (nb_segments + dy) * (nb_segments + dz):
            nb_segments_x = nb_segments
            nb_segments_y = nb_segments + dy
            nb_segments_z = nb_segments + dz
            # print(nb_ref, nb_segments, nb_segments_x, nb_segments_y, nb_segments_z)
            break
    dim_segment_x = 255 // nb_segments_x
    dim_segment_y = 255 // nb_segments_y
    dim_segment_z = 255 // nb_segments_z
    for i in range(nb_segments_x):
        for j in range(nb_segments_y):
            for k in range(nb_segments_z):
                x = i * dim_segment_x + dim_segment_x // 2
                y = j * dim_segment_y + dim_segment_y // 2
                z = k * dim_segment_z + dim_segment_z // 2
                ref.append((x, y, z, 0))
    return ref


def ref_plus_poche(couleur, refs):
    """Renvoie la référence la plus proche de la couleur et son indice"""
    dist_min = distance(couleur, refs[0][0:3])
    ref_min = refs[0]
    i_min = 0
    for i, ref in enumerate(refs):
        dist = distance(couleur, ref[0:3])
        if dist < dist_min:
            dist_min = dist
            ref_min = ref
            i_min = i
    return ref_min, i_min


def déplace_ref(ref, couleur):
    """Calcule les nouvelles coordonnées de la référence déplacée par rapport à la couleur"""
    x, y, z, p = ref
    x = (x * p + couleur[0]) / (p + 1)
    y = (y * p + couleur[1]) / (p + 1)
    z = (z * p + couleur[2]) / (p + 1)
    p = p + 1
    return (x, y, z, p)


def construit_palette(img, nb_ref):
    """Renvoie la liste des nb_ref couleurs les plus représentées dans l'image"""
    refs = ref_palette(nb_ref)
    dim_x, dim_y = img.size
    pas_x, pas_y = dim_x // 20, dim_y // 20
    for x in range(0, dim_x, pas_x):
        for y in range(0, dim_y, pas_y):
            couleur_pixel = img.getpixel((x, y))
            ref_proche, indice_ref = ref_plus_poche(couleur_pixel, refs)
            nouvelle_ref = déplace_ref(ref_proche, couleur_pixel)
            refs[indice_ref] = nouvelle_ref
    refs = organise_palette(refs)
    return refs


def organise_palette(refs):
    """Trie les références par ordre décroissant de poids
    et arrondit les coordonnées de la couleur à l'entier le plus proche"""
    refs.sort(key=lambda x: x[3], reverse=True)
    for i, ref in enumerate(refs):
        # arrondit les coordonnées de la couleur à l'entier le plus proche
        refs[i] = tuple([round(x) for x in ref])
    return refs


def rep_palette(refs):
    """Affiche dans une fenêtre Tkinter de carrés de dimension 50x50 les couleurs de la palette"""
    import tkinter as tk

    fen = tk.Tk()
    fen.title("Palette de couleurs")
    i_max = round(sqrt(len(refs))) + 1
    for i, ref in enumerate(refs):
        x, y, z, p = ref
        couleur = "#%02x%02x%02x" % (x, y, z)
        cadre = tk.Frame(fen, bg=couleur, width=50, height=50)
        cadre.grid(row=i // i_max, column=i % i_max)
    fen.mainloop()


def construit_destination(img, refs, pas, alea=4):
    """Construit une image de destination de mêmes dimensions que l'image source sur fond blanc"""
    dim_x, dim_y = img.size
    img_dest = Image.new("RGB", (dim_x, dim_y), (255, 255, 255))
    for x in range(pas // 2, dim_x, pas):
        for y in range(pas // 2, dim_y, pas):
            var_x = randint(-pas // alea, pas // alea)
            var_y = randint(-pas // alea, pas // alea)
            var_r = randint(0, pas // alea)
            couleur_pixel = img.getpixel((x, y))
            ref_proche, indice_ref = ref_plus_poche(couleur_pixel, refs)
            i, j, k, p = ref_proche
            # Dessine un cercle de couleur (x, y, z) de rayon pas//2
            for dx in range(-pas // 2, pas // 2):
                for dy in range(-pas // 2 - var_r, pas // 2 + var_r):
                    if dx**2 + dy**2 < ((pas // 2) + var_r) ** 2:
                        X = x + dx + var_x
                        Y = y + dy + var_y
                        if 0 <= X < dim_x and 0 <= Y < dim_y:
                            img_dest.putpixel((X, Y), (i, j, k))
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
