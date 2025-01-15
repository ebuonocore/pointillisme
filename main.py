from outils import *

if __name__ == "__main__":
    NB_COULEURS_PALETTE = 20
    fichier = sélectionne_fichier()
    dossier, nom_fichier, extension = sépare_dossier_fichier(fichier)
    chemin = dossier + nom_fichier + extension
    img = ouvre(chemin)
    taille_image = img.size
    print(f"Dimension de {chemin} : {taille_image}")
    min_dim = min(taille_image)
    pas = min_dim // 150
    refs = construit_palette(img, NB_COULEURS_PALETTE)
    print("Fin de la construction de la palette")
    for alea in [1, 3, 5, 10, 20]:
        print("Création du rendu avec un aléa de", alea)
        img_dest = construit_destination(img, refs, pas, alea)
        chemin = dossier + nom_fichier + "_points" + str(alea) + extension
        enregistre(img_dest, chemin)
    print("Fin de la construction des images de destination")
