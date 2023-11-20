# Parseur d'articles scientifiques en format texte

## Introduction

Ce script a pour but de convertir des articles au format PDF en texte brut et d'en extraire des informations clés. Plus précisément, pour chaque article PDF fourni, le script va :

- Convertir le PDF en texte.
- Extraire le titre de l'article.
- Extraire le résumé (ou abstract) de l'article.
- Générer un fichier `.txt` contenant le nom du fichier d'origine, le titre extrait et l'abstract.
- Organiser tous ces fichiers dans des sous-dossiers appropriés.

## Prérequis

1. Python 3.x installé
2. `pdftotext` doit être installé sur votre machine. Il s'agit d'un outil de la suite `poppler-utils` permettant de convertir des PDF en texte.

## Comment utiliser le script

1. **Préparation de l'environnement** :

   - Assurez-vous que les PDF à traiter soient dans le même répertoire que le script.

2. **Exécution du script** :

   - Ouvrez un terminal ou une ligne de commande.
   - Naviguez jusqu'au répertoire contenant le script et les PDF.
   - Exécutez le script avec la commande :
     ```
     python3 scriptParseur.py
     ```

3. **Résultat** :

   - Après l'exécution du script, un nouveau dossier nommé `Processed` sera créé (s'il n'existait pas déjà).
   - À l'intérieur de ce dossier, un sous-dossier pour chaque PDF sera créé, contenant :
     - Le PDF original.
     - Une version texte du PDF.
     - Un fichier d'informations contenant le titre et l'abstract extraits.

## Notes

- Si le dossier `Processed` existe déjà, le script ne le supprime pas, mais il ajoutera ou écrasera les fichiers existants pour les PDF traités.
- Si le script ne trouve pas la section "Abstract" dans le fichier, il prendra les quatre premières lignes après le titre comme abstract.

## Support

Pour toute question ou problème concernant ce script, veuillez contacter "td3@contact-ceri.fr".
