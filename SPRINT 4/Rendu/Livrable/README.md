# Parseur d'articles scientifiques

## Introduction

Ce script a été mis à jour pour convertir des articles scientifiques au format PDF en texte brut ou en format XML structuré, en extrayant des informations clés. Pour chaque article PDF fourni, le script peut maintenant :

- Convertir le PDF en texte.
- Extraire le titre de l'article.
- Extraire le résumé (ou abstract) de l'article.
- Extraire d'autres informations telles que les auteurs et les références bibliographiques (selon la configuration du script).
- Extraire l'introduction de l'article .
- Extraire le corps de l'article .
- Extraire la conclusion de l'article .
- Extraire la discussion de l'article .
- Générer un fichier `.txt` ou un fichier `.xml` contenant ces informations, selon le choix de l'utilisateur.
- Organiser tous ces fichiers dans des sous-dossiers appropriés.

## Nouvelles Fonctionnalités

- **Support du Format XML** : En plus du format texte, le script peut désormais générer des sorties au format XML, structurées avec des balises spécifiques pour le titre, les auteurs, l'abstract, et les références bibliographiques.
- **Choix du Format de Sortie** : L'utilisateur peut choisir le format de sortie (texte ou XML) en utilisant des arguments de ligne de commande lors de l'exécution du script (`-t` pour texte, `-x` pour XML).
- **Sélection de PDF à Parser** : Une nouvelle fonctionnalité a été ajoutée pour permettre à l'utilisateur de sélectionner spécifiquement les PDF qu'il souhaite parser au début de l'exécution du script. Un menu interactif sera présenté, permettant à l'utilisateur de choisir les PDF à traiter.
## Prérequis

1. Python 3.x installé.
2. `pdftotext`, un outil de la suite `poppler-utils`, doit être installé pour la conversion des PDF en texte.

## Comment utiliser le script

1. **Préparation de l'environnement** :

   - Placez les PDF à traiter dans le même répertoire que le script.

2. **Exécution du script** :

   - Ouvrez un terminal ou une ligne de commande.
   - Naviguez jusqu'au répertoire contenant le script et les PDF.
   - Exécutez le script avec la commande :

     ```
     python3 Parseur.py -t
     ```

     ou

     ```
     python3 Parseur.py -x
     ```

     selon le format de sortie désiré.
     - Ecrire le nom du fichier sans l'extension .pdf . et après pour executer il faudra appuyer sur entrer (ligne vide) .

3. **Résultat**

   - Un nouveau dossier `Processed` contenant un sous-dossier pour chaque PDF choisit  avec les fichiers générés (fichier PDF , fichier pdftotxt ,fichier infos.txt ,fichier info.XML ) .

## Notes

- Le script n'écrase pas le dossier `Processed` s'il existe déjà, mais il ajoutera ou mettra à jour les fichiers pour les PDF traités.
- En l'absence d'une section "Abstract" identifiable, le script utilisera une heuristique pour extraire un résumé approximatif.

## Support

Pour toute question ou problème concernant ce script, veuillez contacter "td3@contact-ceri.fr".

