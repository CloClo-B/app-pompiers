from setuptools import setup, find_packages

# Configuration du paquet
setup(
    # Nom du projet
    name="fenalim",

    # Version du projet
    version="0.1.0",

    # Détecte les répertoires de code, spécifiquement du dossier app
    packages=find_packages(include=['app', 'app.*']),

    # Version minimale de Python nécéssaire
    python_requires='>=3.12',
)
