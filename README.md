# Echo_Tele_Expertise
Echo Télé-Expertise, est un portail Web, destiné aux professionnels de santé demandeurs d'expertise et radiologues interprétateurs.

Il permet l'échange et le partage de données d'imagerie médicale échographique entre sites distants. Sur ce territoire, il organise le transfert d'examens d'imagerie échographique, les comptes rendus, la télé-expertise ainsi que le télédiagnostic entre les professionnels de santé.
(Meryem Rkach) 

# Technologies utiliser:
- Backend: Django 3
- Base de Données: PostgreSQL (Relationnelle)

# Installation:
## dépendances:
- python 3+
- pip (or easy_install)
Pour assurer l'isolation de l'app d'abord on prépare l'environnement virtuel:
- install pipenv:   pip install pipenv
Dans le dossier où vous deposerer le dossier de l'app utiliser la commande suivante pour creer pipfile et demarer le shell en virtuel env
- run: pipenv shell
Dans le nouveau shell (ces dependencies vont etre installer seulement dans le virtuel env):
- pipenv install django
- pipenv install psycopg2
- pipenv install psycopg2-binary
Pour utiliser ImageField dans Django:
- pipenv install Pillow
Pour generer le pdf:
- pipenv install xhtml2pdf
Pour le cryptage:
- pipenv install pycryptodome

## Db Super User:
- 'USER': 'postgres',
- 'PASSWORD': 'ITGod2020@'

# Apps:
## core:
Cette app contient le code que j'ai utiliser pour étendre le modele de l'utilisateur

Pour étendre et changer l'ancien comportement du modele de l'utilisateur j'ai choisie la methode suivante:
- Creating a Custom User Model Extending AbstractBaseUser.

## Couleurs de la template:
couleur principale: #142850
couleur secondaire: #27496D
troisième couleur: #00909E
couleur du fond: #e6e4e4

## The myconveryions:
contain a template filter used to transform int -> str,
instead of convert in the views fonction, my choice was to let it in the template.