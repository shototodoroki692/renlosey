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

## run: exécute notre script python pour l'indexation des nos documents.
.PHONY: run/indexing
run/indexing: confirm
	venv/bin/python3 indexing.py