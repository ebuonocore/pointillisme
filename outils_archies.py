def organise_palette(refs):
    """Trie les références par ordre décroissant de poids
    et arrondit les coordonnées de la couleur à l'entier le plus proche"""
    refs.sort(key=lambda x: x[3], reverse=True)
    for i, ref in enumerate(refs):
        # arrondit les coordonnées de la couleur à l'entier le plus proche
        refs[i] = tuple([round(x) for x in ref])
    return refs

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

def déplace_ref(ref, couleur):
    """Calcule les nouvelles coordonnées de la référence déplacée par rapport à la couleur"""
    x, y, z, p = ref
    x = (x * p + couleur[0]) / (p + 1)
    y = (y * p + couleur[1]) / (p + 1)
    z = (z * p + couleur[2]) / (p + 1)
    p = p + 1
    return (x, y, z, p)


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




