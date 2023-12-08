# -*- coding: utf-8 -*-
from os import path
import os
from glob import glob
import sys
from lxml import etree
import xml.etree.ElementTree as ET
import xml.dom.minidom as md

def find_ext(chemin_dossier, ext):
    return glob(path.join(chemin_dossier, "*.{}".format(ext)))

def pdf_to_txt(inpute_path) :
    cmd = "./pdfToText.sh "+inpute_path
    os.system(cmd)

def find_paragraph(file_path, titre):
    paragraph = ""
    linePrecedant = "aa"
    with open(file_path, "r") as file :
        for line in file :
            if((line.lower().find(titre) != -1) or (line.lower().replace(" ","").find(titre) != -1)):   
                       	
                if(len(line) <= len(titre)+1):
                        line = file.readline()
                        while line == "\n":
                            line = file.readline()
                while line:
                    if(titre == "introduction") :
                        if((line[0:1] == "2" and linePrecedant.strip()[-1:] == ".") or (line[0:3] == "II." and linePrecedant.strip()[-1:] == ".")):
                             break   

                    else :
                        if(line.lower().strip() == "1 introduction" or line.strip() == "I. INTRODUCTION" or line[0:9] == "Keywords:" or line.strip() == "1. Introduction"):
                             break

                    paragraph = paragraph + line.strip() + " "
                    linePrecedant = line
                    line = file.readline()

                if(paragraph != "\n"):
                    return paragraph

            elif((titre == "Conclusion" and line.find(titre) != -1) or line.find("Conclusions") != -1 or titre.upper() in line):

                if(len(line) <= len(titre)+1):
                    line = file.readline()
                    while line == "\n":
                        line = file.readline()

                while line:
                    if(("References" in line or "REFERENCES" in line)):
                        break   

                    paragraph = paragraph + line.strip() + " "
                    linePrecedant = line
                    line = file.readline()

                if(paragraph != "\n"):
                    return paragraph

    return "Not Found\n"

def find_reference(file_path, titre):
    paragraph = ""
    with open(file_path, "r") as file :
        for line in file :
            if((line.find(titre) != -1 or line.find("REFERENCES") != -1) and len(line.strip())<=13):            	
                if(len(line) <= len(titre)+1):
                        line = file.readline()
                        while line == "\n":
                            line = file.readline()
                while line:
                    if(titre == "References" or titre.upper() == "REFERENCES") :
                        if(line is None) :
                             break
                    paragraph = paragraph + line.strip() + " "
                    line = file.readline()
                if(paragraph != "\n"):
                    return paragraph
    return "Not Found\n"

def find_discussion(file_path, titre):
    paragraph = ""
    with open(file_path, "r") as file :
        for line in file :
            if(line.find(titre) != -1 or line.find("DISCUSSION") != -1):            	
                if(len(line) <= len(titre)+1):
                        line = file.readline()
                        while line == "\n":
                            line = file.readline()
                while line:
                    if(titre == "Discussion" or titre.upper() == "DISCUSSION") :
                        if(((line.find("References") != -1 or line.find("REFERENCES") != -1 )and len(line.strip())<=11) or (line.find("Conclusions") != -1 or line.find("CONCLUSIONS") != -1 or line.find("Conclusion") != -1 or line.find("CONCLUSION") != -1)):
                             break
                    paragraph = paragraph + line.strip() + " "
                    line = file.readline()
                if(paragraph != "\n"):
                    return paragraph
    return "Not Found\n"

def find_corps(file_path):
    paragraph = ""
    linePrecedant = ""
    check = find_paragraph(file_path,"introduction")
    with open(file_path, "r") as file :
        for line in file :
            if(check == "Not Found\n"):
            	if(line[0:1] == "1" or line[0:3] == "I."):
                     while line:
                         if(line.find("Discussion") != -1 or line.find("DISCUSSION") != -1 or line.find("Conclusions") != -1 or line.find("CONCLUSIONS") != -1 or line.find("Conclusion") != -1 or line.find("CONCLUSION") != -1 or ((line.find("References") != -1 or line.find("REFERENCES") != -1) and len(line.strip())<=13)) :
                               break
                         paragraph = paragraph + line.strip() + " "
                         line = file.readline() 
                     return paragraph     
			    
            	linePrecedant = line
			    
            else:
            	if((line[0:1] == "2" and linePrecedant.strip()[-1:] == ".") or (line[0:3] == "II." and linePrecedant.strip()[-1:] == ".")):
                     while line:
                         if(line.find("Discussion") != -1 or line.find("DISCUSSION") != -1 or line.find("Conclusions") != -1 or line.find("CONCLUSIONS") != -1 or line.find("Conclusion") != -1 or line.find("CONCLUSION") != -1 or ((line.find("References") != -1 or line.find("REFERENCES") != -1) and len(line.strip())<=13)) :
                               break
                         paragraph = paragraph + line.strip() + " "
                         line = file.readline() 
                     return paragraph     
			    
            	linePrecedant = line
		    	
		    
            
    return "Not Found\n"

def create_directory(dossier):
    directory_name = dossier
    path = directory_name
    if(os.path.isdir(path)):
        os.system("rm -r " + path)                  #supprimer le dossier s'il exit    
    os.system("mkdir " + path)                      #re creer le dossier
    return path    

def parser_file_to_xml(target_path, output_path) :

    article = etree.Element("article")
    file_name = os.path.basename(target_path).replace(".txt", ".pdf")
    title = ""
    writer =""
    abstract = ""

    preamble = etree.SubElement(article, "preamble")
    preamble.text = file_name

    file = open(target_path, "r")
    for i in range(2) :
        title = title + file.readline().strip('\n').strip() + " "

    for line in file :
       if(line.lower().find("abstract") != -1):
          break;
       writer = writer + line.strip('\n').strip()

    file.close()

    titre = etree.SubElement(article, "titre")
    titre.text = title

    auteur = etree.SubElement(article, "auteur")
    auteur.text = writer

    abstract = etree.SubElement(article, "abstract")
    abstract.text = find_paragraph(target_path, "abstract")

    introduction = etree.SubElement(article,"introduction")
    introduction.text = find_paragraph(target_path,"introduction")

    corps = etree.SubElement(article,"corps")
    corps.text = find_corps(target_path)

    discu = etree.SubElement(article, "Discussion")
    discu.text = find_discussion(target_path, "Discussion")

    conclusion = etree.SubElement(article, "conclusion")
    conclusion.text = find_paragraph(target_path, "Conclusion")

    biblio = etree.SubElement(article, "biblio")
    biblio.text = find_reference(target_path, "References")

    xmlstr = ET.tostring(article).decode('utf8')
    newxml = md.parseString(xmlstr)
    with open(output_path, "a") as output:
        output.write(newxml.toprettyxml(indent='\t',newl='\n'))

def format_title(title):
    return title.capitalize()

def parser_file_to_txt(filepath, output_path):
    writer = ""
    file_name = os.path.basename(filepath).replace(".txt", ".pdf")
    title = ""

    f = open(filepath, "r")
    for i in range(2):
        title += f.readline().strip('\n').strip() + " "
    for line in f:
        if(line.lower().find("abstract") != -1):
            break
        writer += line.strip('\n').strip()
    f.close()

    f = open(output_path, "a")
    f.write("\n\n" + format_title("Nom du fichier : ") + file_name + "\n")
    f.write("\n\n" + format_title("Titre du fichier : ") + title.rstrip() + "\n")
    f.write("\n\n" + format_title("Auteurs : ") + writer.rstrip() + "\n")

    abstract = find_paragraph(filepath, "abstract")
    f.write("\n\n" + format_title("Abstract : ") + abstract)

    introduction = find_paragraph(filepath, "introduction")
    f.write("\n\n" + format_title("Introduction : ") + introduction)

    corps = find_corps(filepath)
    f.write("\n\n" + format_title("Corps : ") + corps)

    discussion = find_discussion(filepath, "Discussion")
    f.write("\n\n" + format_title("Discussion : ") + discussion)

    conclusion = find_paragraph(filepath, "Conclusion")
    f.write("\n\n" + format_title("Conclusion : ") + conclusion)

    reference = find_reference(filepath, "References")
    f.write("\n\n" + format_title("References : ") + reference)

    f.close()

def lister_repertoires(chemin_dossier):
    try:
        repertoires = [dossier for dossier in os.listdir(chemin_dossier) if os.path.isdir(os.path.join(chemin_dossier, dossier))]
        if not repertoires:
            print("Aucun sous-dossier trouvé.")
        else:
            print("Sous-dossiers disponibles :")
            for idx, dossier in enumerate(repertoires):
                print(f"{idx+1}. {dossier}")
    except FileNotFoundError:
        print("Chemin du dossier non trouvé.")

def select_pdf_files(folder_path):
    pdf_files = find_ext(folder_path, "pdf")
    selected_files = []
    print("Sélectionnez les fichiers PDF à parser (entrez le numéro séparé par des espaces) :")
    for idx, file in enumerate(pdf_files):
        print(f"{idx+1}. {os.path.basename(file)}")
    selections = input("Entrez les numéros des fichiers sélectionnés : ").split()
    for selection in selections:
        try:
            selected_files.append(pdf_files[int(selection) - 1])
        except (IndexError, ValueError):
            print(f"Choix invalide: {selection}")
    return selected_files

def main():
    print("Bienvenue dans le parser de fichier PDF.")
    print("---------------------------------------------------------------------------------")

    choix_format = input("Choisissez le format de sortie (-t pour texte, -x pour XML) : ")
    if choix_format not in ["-t", "-x"]:
        print("Format invalide. Veuillez choisir -t ou -x.")
        return 0

    print("---------------------------------------------------------------------------------")
    print("Liste des répertoires dans le dossier courant :")
    lister_repertoires(".")
    print("---------------------------------------------------------------------------------")

    chemin_dossier_PDF = input("Entrez le chemin du dossier contenant les fichiers PDF : ")
    print("Liste des répertoires dans le dossier spécifié :")
    lister_repertoires(chemin_dossier_PDF)
    print("---------------------------------------------------------------------------------")

    selected_files = select_pdf_files(chemin_dossier_PDF)

    nom_dossier_output = "Analyse_txt" if choix_format == "-t" else "Analyse_xml"
    dossier_output = create_directory(nom_dossier_output)

    pdf_to_txt(chemin_dossier_PDF)

    print("---------------------------------------------------------------------------------")
    print("Analyse en cours...")
    print("---------------------------------------------------------------------------------")

    # Pour chaque fichier PDF sélectionné, on crée un fichier TXT correspondant
    for file in selected_files:

        File_txt_path = "TEXT/" + os.path.basename(file).replace(".pdf", ".txt")

        print ("Création du fichier " + File_txt_path + "...")
        output_path = dossier_output + "/" + os.path.basename(file).replace(".pdf", ".txt" if choix_format == "-t" else ".xml")

        # On parse le fichier TXT créé
        if choix_format == "-t":
            parser_file_to_txt(File_txt_path, output_path) # On parse le fichier TXT créé
            print("Persage du fichier " + File_txt_path + " terminé.")
        else:
            parser_file_to_xml(File_txt_path, output_path)
            print("Persage du fichier " + File_txt_path + " terminé.")
            
        print("\n")

    print("---------------------------------------------------------------------------------")
    print("Analyse terminée.")
    print("---------------------------------------------------------------------------------")

if __name__ == "__main__":
    main()