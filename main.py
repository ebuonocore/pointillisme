from fichiers import *
from traitement_image import *
from time import time

if __name__ == "__main__":
    NB_COULEURS_PALETTE = 64
    NB_PIXELS_ECHANTILLON = 1000

    # Sélection du fichier
    fichier = sélectionne_fichier()
    dossier, nom_fichier, extension = sépare_dossier_fichier(fichier)
    chemin = dossier + nom_fichier + extension
    photo = ouvre(chemin)
    taille_image = photo.size
    print(f"Dimension de {chemin} : {taille_image}")

    # Initialisation
    min_dim = min(taille_image)
    pas = min_dim // 100
    palette = construit_palette(photo, NB_PIXELS_ECHANTILLON, NB_COULEURS_PALETTE)
    # rep_palette(palette)
    print("Fin de la construction de la palette")

    # Génération des images de destination
    for alea in [1, 3, 5, 10]:
        print("Création du rendu avec un aléa de", alea)
        temps_début = time()
        image_dest = construit_destination(photo, palette, pas, alea)
        temps_fin = time()
        print("  Temps de calcul :", round(temps_fin - temps_début, 2))
        chemin = dossier + nom_fichier + "_points" + str(alea) + extension
        enregistre(image_dest, chemin)
    print("Fin de la construction des images de destination")
