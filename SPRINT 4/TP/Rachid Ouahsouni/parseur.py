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
    corps = "Inconnu"
    conclusion = "Inconnu"
    discussion = "Inconnu"
    biblio = "Inconnu"

    # On tente d'extraire le titre
    lines = file_text.splitlines()
    if lines:
        title = lines[0].strip()  # On prend la première ligne comme titre 

    # Tentative d'extraction des auteurs (ajuster selon la structure du document)
    if len(lines) > 1:
        authors = lines[1].strip()

    # Tentative d'extraction de l'abstract
    abstract_start_keywords = ["Abstract", "Résumé"]  # Mots clés pouvant indiquer le début de l'abstract

    for keyword in abstract_start_keywords:
        try:
            start_abstract = lines.index(keyword) + 1
            end_abstract = None
            for idx, line in enumerate(lines[start_abstract:], start=start_abstract):
                if any(keyword in line for keyword in ["Introduction", "Keywords"]):
                    end_abstract = idx
                    break
            if end_abstract:
                abstract = " ".join(lines[start_abstract:end_abstract]).replace('\n', ' ').strip()
                break
        except ValueError:
            # Si le mot clé n'est pas trouvé, on passe au suivant
            continue

    # Tentative d'extraction de l'introduction, du corps, de la conclusion, de la discussion et de la bibliographie
    sections_start_keywords = {
        "Introduction": "introduction",
        "Corps": "corps",
        "Conclusion": "conclusion",
        "Discussion": "discussion",
        "Bibliographie": "biblio"
    }

    current_section = None
    for line in lines:
        for keyword, section in sections_start_keywords.items():
            if keyword in line:
                current_section = section
                break
        if current_section:
            globals()[current_section] = line.replace(keyword, '').strip()
            if line.endswith("."):
                current_section = None

    return title, authors, abstract, introduction, corps, conclusion, discussion, biblio

def create_xml_output(title, authors, abstract, introduction, corps, conclusion, discussion, biblio, subdir_path, subdir_name):
    # Créer la structure XML
    root = ET.Element("article")
    ET.SubElement(root, "preamble").text = subdir_name
    ET.SubElement(root, "title").text = title
    ET.SubElement(root, "author").text = authors
    ET.SubElement(root, "abstract").text = abstract
    ET.SubElement(root, "introduction").text = introduction
    ET.SubElement(root, "corps").text = corps
    ET.SubElement(root, "conclusion").text = conclusion
    ET.SubElement(root, "discussion").text = discussion
    ET.SubElement(root, "biblio").text = biblio

    # Écrire le fichier XML
    tree = ET.ElementTree(root)
    xml_path = os.path.join(subdir_path, f"{subdir_name}.xml")
    tree.write(xml_path)

# Sélection des fichiers PDF à traiter
selected_files = []
print("Sélectionnez les fichiers PDF à traiter (appuyez sur Entrée pour terminer la sélection):")
while True:
    filename = input("Nom du fichier (sans l'extension .pdf) : ")
    if not filename:
        break
    selected_files.append(f"{filename}.pdf")

# Boucle de traitement pour chaque fichier PDF sélectionné
for filename in selected_files:
    print(f"Vérification du fichier : {filename}")
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
    title, authors, abstract, introduction, corps, conclusion, discussion, biblio = extract_info_from_text(content)

    # Créer un fichier en fonction de l'option sélectionnée
    if args.xml:
        # Générer un fichier XML
        create_xml_output(title, authors, abstract, introduction, corps, conclusion, discussion, biblio, subdir_path, subdir_name)
    elif args.text:
        # Générer un fichier texte
        info_path = os.path.join(subdir_path, f"{subdir_name}_info.txt")
        with open(info_path, 'w') as f:
            f.write(f"Fichier : {filename.replace(' ', '_')}\n")
            f.write(f"Titre : {title}\n")
            f.write(f"Auteurs : {authors}\n")
            f.write(f"Résumé : {abstract}\n")
            f.write(f"Introduction : {introduction}\n")
            f.write(f"Corps : {corps}\n")
            f.write(f"Conclusion : {conclusion}\n")
            f.write(f"Discussion : {discussion}\n")
            f.write(f"Bibliographie : {biblio}\n")

print("Script terminé")
