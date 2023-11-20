import os
import subprocess
import argparse
import xml.etree.ElementTree as ET

# Configuration de l'analyse des arguments de ligne de commande
parser = argparse.ArgumentParser(description='Parseur de PDF en texte/XML')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-t', '--text', action='store_true', help='Générer une sortie texte')
group.add_argument('-x', '--xml', action='store_true', help='Générer une sortie XML')
args = parser.parse_args()

print("Démarrage du script")

# Chemin vers le dossier contenant les PDF
SOURCE_DIR = "."
DEST_DIR = "Processed"

# Créer le dossier de destination s'il n'existe pas
if not os.path.exists(DEST_DIR):
    print(f"Création de {DEST_DIR}")
    os.makedirs(DEST_DIR)
else:
    print(f"Le répertoire {DEST_DIR} existe déjà")

def extract_info_from_text(file_text):
    title = "Inconnu"
    authors = "Inconnu"
    abstract = "Inconnu"

    # On tente d'extraire le titre
    lines = file_text.splitlines()
    if lines:
        title = lines[0]  # On prend la première ligne comme titre 

    # Tentative d'extraction des auteurs (ajuster selon la structure du document)
    if len(lines) > 1:
        authors = lines[1]

    # Tentative d'extraction de l'abstract
    try:
        start_abstract = lines.index("Abstract") + 1
        end_abstract = None
        for idx, line in enumerate(lines[start_abstract:], start=start_abstract):
            if "Introduction" in line or "Keywords" in line:
                end_abstract = idx
                break
        if end_abstract:
            abstract = " ".join(lines[start_abstract:end_abstract]).replace('\n', ' ').strip()
    except ValueError:
        # Fallback si "Abstract" n'est pas trouvé
        abstract = " ".join(lines[2:6]).strip()  # Quatre lignes après les auteurs

    return title, authors, abstract

def create_xml_output(title, authors, abstract, subdir_path, subdir_name):
    # Créer la structure XML
    root = ET.Element("article")
    ET.SubElement(root, "preamble").text = subdir_name
    ET.SubElement(root, "title").text = title
    ET.SubElement(root, "author").text = authors
    ET.SubElement(root, "abstract").text = abstract

    # Écrire le fichier XML
    tree = ET.ElementTree(root)
    xml_path = os.path.join(subdir_path, f"{subdir_name}.xml")
    tree.write(xml_path)

# Boucle de traitement pour chaque fichier PDF
for filename in os.listdir(SOURCE_DIR):
    print(f"Vérification du fichier : {filename}")
    if filename.endswith(".pdf"):
        print(f"Traitement du fichier : {filename}")
        file_path = os.path.join(SOURCE_DIR, filename)

        # Créer un sous-dossier pour chaque PDF
        subdir_name = filename.replace(".pdf", "")
        subdir_path = os.path.join(DEST_DIR, subdir_name)
        if not os.path.exists(subdir_path):
            print(f"Création du répertoire : {subdir_path}")
            os.makedirs(subdir_path)
        else:
            print(f"Le répertoire {subdir_path} existe déjà")

        # Copier le PDF vers le sous-dossier
        dest_pdf_path = os.path.join(subdir_path, filename)
        os.system(f"cp '{file_path}' '{dest_pdf_path}'")

        # Convertir le PDF en texte
        print(f"Conversion du PDF : {filename}")
        dest_txt_path = os.path.join(subdir_path, f"{subdir_name}_pdftotext.txt")
        subprocess.run(["pdftotext", file_path, dest_txt_path])

        # Lire le contenu du fichier texte
        with open(dest_txt_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Extraire les informations nécessaires
        print(f"Extraction des informations de : {filename}")
        title, authors, abstract = extract_info_from_text(content)

        # Créer un fichier en fonction de l'option sélectionnée
        if args.xml:
            # Générer un fichier XML
            create_xml_output(title, authors, abstract, subdir_path, subdir_name)
        elif args.text:
            # Générer un fichier texte
            info_path = os.path.join(subdir_path, f"{subdir_name}_info.txt")
            with open(info_path, 'w') as f:
                f.write(f"Fichier : {filename.replace(' ', '_')}\n")
                f.write(f"Titre : {title}\n")
                f.write(f"Auteurs : {authors}\n")
                f.write(f"Résumé : {abstract}\n")

print("Script terminé")
