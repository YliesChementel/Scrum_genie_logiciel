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
    introduction = "Inconnu"
    conclusion = "Inconnu"
    body = "Inconnu"

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

    # Tentative d'extraction de l'introduction
    try:
        start_introduction = lines.index("1. Introduction") + 1
    except ValueError:
        try:
            start_introduction = lines.index("Introduction") + 1
        except ValueError:
            try:
                start_introduction = lines.index("1 Introduction") + 1
            except ValueError:
                try:
                    start_introduction = lines.index("I. I NTRODUCTION") + 1
                except ValueError:
                    try:
                        start_introduction = lines.index("INTRODUCTION") + 1
                    except ValueError:
                        start_introduction = None

    if start_introduction is not None:
        end_introduction = None
        for idx, line in enumerate(lines[start_introduction:], start=start_introduction):
            if "Methods" in line or "Background" in line or "Conclusion" in line or line.strip().startswith("2 ") or "A noisy-channel model for sentence" in line or "Previous Work" in line or  "Related Work" in line or line.strip().startswith("2."):
                end_introduction = idx
                break
        if end_introduction:
            introduction = " ".join(lines[start_introduction:end_introduction]).replace('\n', ' ').strip()

    # Tentative d'extraction du corps
    if start_introduction is not None and end_introduction is not None:
        body_start = end_introduction
        body_end = None
        for idx, line in enumerate(lines[body_start:], start=body_start):
            if "Conclusion" in line or "Acknowledgements" in line or "References" in line:
                body_end = idx
                break
        if body_end:
            body = " ".join(lines[body_start:body_end]).replace('\n', ' ').strip()

    # Tentative d'extraction de la conclusion
    try:
        start_conclusion = lines.index("Conclusions and Future Work") + 1
    except ValueError:
        try:
            start_conclusion = lines.index("Conclusion") + 1
        except ValueError:
            try:
                start_conclusion = lines.index("Conclusions") + 1
            except ValueError:
                try:
                    start_conclusion = lines.index("4 Conclusion") + 1
                except ValueError:
                    try:
                        start_conclusion = lines.index("Conclusions") + 1
                    except ValueError:
                        try:
                            start_conclusion = lines.index("CONCLUSIONS") + 1
                        except ValueError:
                            start_conclusion = None

    if start_conclusion is not None:
        end_conclusion = None
        for idx, line in enumerate(lines[start_conclusion:], start=start_conclusion):
            if "Acknowledgements" in line or "References" in line:
                end_conclusion = idx
                break
        if end_conclusion:
            conclusion = " ".join(lines[start_conclusion:end_conclusion]).replace('\n', ' ').strip()

    return title, authors, abstract, introduction, body, conclusion

def create_xml_output(title, authors, abstract, introduction, conclusion, body, subdir_path, subdir_name):
    # Créer la structure XML
    root = ET.Element("article")
    ET.SubElement(root, "preamble").text = subdir_name
    ET.SubElement(root, "title").text = title
    ET.SubElement(root, "author").text = authors
    ET.SubElement(root, "abstract").text = abstract
    ET.SubElement(root, "introduction").text = introduction
    ET.SubElement(root, "body").text = body  # Nouveau élément
    ET.SubElement(root, "conclusion").text = conclusion

    # Écrire le fichier XML
    tree = ET.ElementTree(root)
    xml_path = os.path.join(subdir_path, f"{subdir_name}.xml")
    tree.write(xml_path)

# Boucle de traitement pour chaque fichier PDF
titles = set()  # Utilisé pour suivre les titres uniques
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
        title, authors, abstract, introduction, body, conclusion = extract_info_from_text(content)

        # Vérifier si le titre est déjà utilisé
        if title not in titles:
            titles.add(title)  # Ajouter le titre à l'ensemble des titres

            # Créer un fichier en fonction de l'option sélectionnée
            if args.xml:
                # Générer un fichier XML
                create_xml_output(title, authors, abstract, introduction, conclusion, body, subdir_path, subdir_name)
            elif args.text:
                # Générer un fichier texte
                info_path = os.path.join(subdir_path, f"{subdir_name}_info.txt")
                with open(info_path, 'w') as f:
                    f.write(f"Fichier : {filename.replace(' ', '_')}\n")
                    f.write(f"Titre : {title}\n")
                    f.write(f"Auteurs : {authors}\n")
                    f.write(f"Résumé : {abstract}\n")
                    f.write(f"Introduction : {introduction}\n")
                    f.write(f"Corps : {body}\n")
                    f.write(f"Conclusion : {conclusion}\n")

print("Script terminé")
