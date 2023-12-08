#!/bin/bash

# Vérifiez si le dossier TEXT existe, sinon créez-le
if [ ! -d "TEXT" ]; then
    mkdir TEXT
fi

# Videz le contenu du dossier TEXT
rm -f TEXT/*

# Vérifiez si le chemin du dossier PDF est fourni
if [ -z "$1" ]; then
    echo "Aucun dossier spécifié pour les fichiers PDF."
    exit 1
fi

# Convertissez chaque fichier PDF en texte et déplacez-le dans le dossier TEXT
find "$1" -name "*.pdf" -exec sh -c 'pdftotext -raw -enc ASCII7 "{}" "TEXT/$(basename "{}" .pdf).txt"' \;
