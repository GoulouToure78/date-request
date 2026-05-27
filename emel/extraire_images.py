"""
Script pour extraire les images base64 d'un fichier HTML
et les remplacer par des liens vers des fichiers image séparés.

Usage :
    python extraire_images.py mon_fichier.html

Résultat :
    - mon_fichier_light.html  → le HTML allégé avec des <img src="images/...">
    - images/                 → dossier contenant toutes les images extraites
"""

import re
import base64
import os
import sys
from pathlib import Path

def extraire_images(chemin_html):
    chemin_html = Path(chemin_html)
    if not chemin_html.exists():
        print(f"❌ Fichier introuvable : {chemin_html}")
        sys.exit(1)

    # Lire le fichier HTML
    with open(chemin_html, "r", encoding="utf-8") as f:
        contenu = f.read()

    # Créer le dossier images/ à côté du fichier HTML
    dossier_images = chemin_html.parent / "images"
    dossier_images.mkdir(exist_ok=True)

    compteur = 1
    extensions = {
        "image/png": "png",
        "image/jpeg": "jpg",
        "image/jpg": "jpg",
        "image/gif": "gif",
        "image/webp": "webp",
        "image/svg+xml": "svg",
    }

    # Regex pour trouver toutes les images base64
    patron = re.compile(r'src="data:(image/[^;]+);base64,([^"]+)"')

    def remplacer(match):
        nonlocal compteur
        mime = match.group(1)
        donnees_b64 = match.group(2)
        ext = extensions.get(mime, "png")
        nom_fichier = f"image_{compteur:03d}.{ext}"
        chemin_sortie = dossier_images / nom_fichier

        # Décoder et sauvegarder l'image
        try:
            donnees = base64.b64decode(donnees_b64)
            with open(chemin_sortie, "wb") as f:
                f.write(donnees)
            print(f"  ✅ {nom_fichier} ({len(donnees) // 1024} Ko)")
            compteur += 1
            return f'src="images/{nom_fichier}"'
        except Exception as e:
            print(f"  ⚠️  Erreur sur l'image {compteur} : {e}")
            compteur += 1
            return match.group(0)  # Garder l'original si erreur

    print(f"\n🔍 Analyse de : {chemin_html.name}")
    nouveau_contenu = patron.sub(remplacer, contenu)

    # Sauvegarder le HTML allégé
    nom_sortie = chemin_html.stem + "_light.html"
    chemin_sortie_html = chemin_html.parent / nom_sortie
    with open(chemin_sortie_html, "w", encoding="utf-8") as f:
        f.write(nouveau_contenu)

    nb_images = compteur - 1
    taille_avant = chemin_html.stat().st_size // 1024
    taille_apres = chemin_sortie_html.stat().st_size // 1024

    print(f"\n✅ Terminé !")
    print(f"   📄 HTML allégé : {nom_sortie}")
    print(f"   🖼️  Images extraites : {nb_images} fichier(s) dans images/")
    print(f"   📦 Taille avant : {taille_avant} Ko")
    print(f"   📦 Taille après  : {taille_apres} Ko")
    print(f"\n💡 Pour que les images s'affichent, garde le HTML et le dossier images/ au même endroit.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage : python extraire_images.py mon_fichier.html")
        sys.exit(1)
    extraire_images(sys.argv[1])
