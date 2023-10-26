import subprocess
import os

# Fonction pour extraire le premier gros paragraphe entre "Abstract" et "Introduction"
def extract_paragraph_between_abstract_and_introduction(pdf_path):
    try:
        result = subprocess.run(["pdftotext", pdf_path, "-"], capture_output=True, text=True, check=True)
        extracted_text = result.stdout
        # Trouver l'emplacement de "Abstract" et "Introduction"
        abstract_index = extracted_text.find("Abstract")
        intro_index = extracted_text.find("Introduction")
        if abstract_index != -1 and intro_index != -1:
            # Extraire le paragraphe entre "Abstract" et "Introduction"
            paragraph = extracted_text[abstract_index + len("Abstract"):intro_index].strip()
            return paragraph
        return None
    except subprocess.CalledProcessError as e:
        print("Erreur lors de l'extraction du texte :")
        print(e)
        return None

# Chemin vers le fichier PDF que vous souhaitez traiter
pdf_path = "/home/nas-wks01/users/uapv2000019/genielogiciel/Scrum_genie_logiciel/SPRINT 2/TP/Rachid Ouahsouni/ACL2004-HEADLINE.pdf" 

# Exécutez la fonction pour extraire le premier gros paragraphe entre "Abstract" et "Introduction"
paragraph = extract_paragraph_between_abstract_and_introduction(pdf_path)

# Créez le nom du fichier de sortie (remplacez l'extension .pdf par .txt)
output_filename = os.path.splitext(pdf_path)[0] + "_paragraph.txt"

# Enregistrez le paragraphe dans un fichier texte
if paragraph:
    with open(output_filename, "w", encoding="utf-8") as output_file:
        output_file.write(paragraph)
        print(f"Le premier gros paragraphe enregistré dans {output_filename}")
else:
    print("Paragraphe non trouvé dans le PDF.")
