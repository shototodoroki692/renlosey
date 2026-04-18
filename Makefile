# confirm: demande la confirmation de l'utilisateur avec la saisie de "y", avant
# d'exécuter une commande.
.PHONY: confirm
confirm:
	@echo -n 'Êtes-vous sûr de vouloir exécuter cette commande ? [y/N] ' && read ans && [ $${ans:-N} = y ]

## install/%: installe dans notre environnement virtuel le package renseigné 
## après install/ avec pip.
.PHONY: install/%
install/%:
	venv/bin/pip install $*

## run/indexing: exécute notre script python pour l'indexation des nos documents.
.PHONY: run/indexing
run/indexing: confirm # run/db
	venv/bin/python3 indexing.py

## run/db: exécute notre fichier compose.yaml pour instancier un container
## docker à partir de notre image postgres. Notre base de données PostgreSQL est
## donc disponible via Docker.
.PHONY: run/db
run/db:
	docker compose up --build -d