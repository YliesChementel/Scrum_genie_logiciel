# Parseur d'Articles Scientifiques

## Introduction

Ce script a été développé pour traiter et analyser des articles scientifiques au format PDF. Il permet de convertir ces articles en texte brut ou en XML structuré, en extrayant des informations clés telles que le titre, les auteurs, l'abstract et les références. Le script est désormais plus interactif et flexible, offrant des fonctionnalités améliorées pour une meilleure expérience utilisateur.

## Nouvelles Fonctionnalités

- **Menu Interactif** : Un menu interactif est désormais intégré pour faciliter la sélection des fichiers PDF à analyser et le choix du format de sortie.
- **Listage des Répertoires** : Le script affiche maintenant les répertoires disponibles pour aider l'utilisateur à choisir le bon chemin de dossier contenant les fichiers PDF.
- **Prise en Charge des Formats TXT et XML** : Le script permet de générer des fichiers en format texte ou XML, contenant des informations structurées extraites des articles PDF.
- **Amélioration de la Présentation des Sorties** : Les sorties en fichier texte ont été améliorées pour une meilleure lisibilité, avec des titres de sections capitalisés et un formatage cohérent.

## Prérequis

1. Python 3.x doit être installé sur votre système.
2. Le script `pdftotext`, inclus dans la suite `poppler-utils`, est nécessaire pour la conversion des fichiers PDF en texte.

## Installation et Configuration

- Assurez-vous que Python 3.x et `pdftotext` sont installés sur votre machine.
- Placez le script `main.py` et `pdfToText.sh` dans le même répertoire que vos fichiers PDF.

## Comment Utiliser le Script

1. **Préparation** :

   - Stockez les fichiers PDF que vous souhaitez traiter dans un répertoire accessible par le script.

2. **Exécution** :

   - Ouvrez un terminal.
   - Naviguez jusqu'au répertoire contenant le script et les fichiers PDF.
   - Lancez le script en exécutant `python3 main.py`.
   - Suivez les instructions affichées dans le menu interactif pour choisir les fichiers PDF et le format de sortie.

3. **Résultats** :

   - Les fichiers traités seront organisés dans des dossiers `Analyse_txt` ou `Analyse_xml` selon le format choisi.

## Notes Importantes

- Le script créera de nouveaux dossiers pour les sorties et ne conservera pas les anciennes analyses.
- En cas d'absence d'une section identifiable (comme "Abstract"), le script appliquera des heuristiques pour extraire les informations pertinentes.

## Support et Contact

Pour toute question, commentaire ou besoin d'assistance, veuillez contacter "support@sprint5.com".
