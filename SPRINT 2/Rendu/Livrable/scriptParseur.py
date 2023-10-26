import os
import subprocess

print("Script started")

# Chemin vers le dossier contenant les PDF
SOURCE_DIR = "."
DEST_DIR = "Processed"

# Créer le dossier de destination s'il n'existe pas
if not os.path.exists(DEST_DIR):
    print(f"Creating {DEST_DIR}")
    os.makedirs(DEST_DIR)
else:
    print(f"{DEST_DIR} already exists")

def extract_info_from_text(file_text):
    title = "Unknown"
    abstract = "Unknown"

    # On tente d'extraire le titre
    lines = file_text.splitlines()
    if lines:
        title = lines[0]  # On prend la première ligne comme titre 

    # Tentative d'extraction de l'abstract
    try:
        start_abstract = lines.index("Abstract") + 1
        # Trouver l'index de "Introduction"
        for idx, line in enumerate(lines[start_abstract:]):
            if "Introduction" in line:
                end_abstract = start_abstract + idx
                break
        else:
            end_abstract = None

        abstract = " ".join(lines[start_abstract:end_abstract]).replace('\n', ' ').strip()
    except ValueError:
        # Si "Abstract" n'est pas trouvé, prend les lignes après le titre comme abstract (ajuster selon les besoins)
        abstract = " ".join(lines[1:5])  # Prend les 4 lignes après le titre

    return title, abstract

for filename in os.listdir(SOURCE_DIR):
    print(f"Checking file: {filename}")
    if filename.endswith(".pdf"):
        print(f"Processing file: {filename}")
        file_path = os.path.join(SOURCE_DIR, filename)

        # Créer un sous-dossier pour chaque PDF
        subdir_name = filename.replace(".pdf", "")
        subdir_path = os.path.join(DEST_DIR, subdir_name)
        if not os.path.exists(subdir_path):
            print(f"Creating directory: {subdir_path}")
            os.makedirs(subdir_path)
        else:
            print(f"Directory {subdir_path} already exists")

        # Copier le PDF vers le sous-dossier
        dest_pdf_path = os.path.join(subdir_path, filename)
        os.system(f"cp '{file_path}' '{dest_pdf_path}'")

        # Convertir le PDF en texte
        print(f"Converting PDF: {filename}")
        dest_txt_path = os.path.join(subdir_path, f"{subdir_name}_pdftotext.txt")
        subprocess.run(["pdftotext", file_path, dest_txt_path])

        # Lire le contenu du fichier texte
        with open(dest_txt_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Extraire les informations nécessaires
        print(f"Extracting info from: {filename}")
        title, abstract = extract_info_from_text(content)

        # Créer un fichier avec les éléments extraits
        info_path = os.path.join(subdir_path, f"{subdir_name}_info.txt")
        with open(info_path, 'w') as f:
            f.write(f"File: {filename.replace(' ', '_')}\n")
            f.write(f"Title: {title}\n")
            f.write(f"Abstract: {abstract}\n")

print("Script finished")
