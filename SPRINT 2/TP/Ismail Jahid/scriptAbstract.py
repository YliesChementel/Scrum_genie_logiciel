import subprocess
import sys

def extraire_resume(chemin_du_pdf):
    try:
        # Appeler pdftotext depuis le script Python
        pdf_text = subprocess.check_output(['pdftotext', chemin_du_pdf, '-'], stderr=subprocess.STDOUT, text=True)

        # Trouver l'index du mot 'Abstract' (peut nécessiter des ajustements en fonction du PDF)
        abstract_index = pdf_text.find('Abstract')
        
        # Si 'Abstract' n'est pas trouvé, retourner une chaîne vide
        if abstract_index == -1:
            return ""
        
        # Extraire le texte après 'Abstract' jusqu'à la prochaine occurrence de 'Introduction'
        introduction_index = pdf_text.find('Introduction', abstract_index)
        if introduction_index != -1:
            return pdf_text[abstract_index + len('Abstract'):introduction_index].strip()

        # Si 'Introduction' n'est pas trouvé, extraire jusqu'à la fin du texte
        return pdf_text[abstract_index + len('Abstract'):].strip()

    except subprocess.CalledProcessError as e:
        # En cas d'erreur lors de l'extraction du texte, imprimer l'erreur
        print("Erreur lors de l'extraction du texte du PDF:", e.output)
        return None

if __name__ == "__main__":
    # Vérifier s'il y a exactement un argument (le chemin du fichier PDF) passé lors de l'exécution du script
    if len(sys.argv) != 2:
        print("Usage: python scriptTitre.py <chemin/vers/votre/fichier.pdf>")
    else:
        chemin_du_pdf = sys.argv[1]
        resume = extraire_resume(chemin_du_pdf)
        
        # Afficher le résumé
        if resume:
            print(resume)
        else:
            print("Extraction du résumé du PDF a échoué.")

