# Echo_Tele_Expertise
Echo Télé-Expertise, est un portail Web, destiné aux professionnels de santé demandeurs d'expertise et radiologues interprétateurs.

Il permet l'échange et le partage de données d'imagerie médicale échographique entre sites distants. Sur ce territoire, il organise le transfert d'examens d'imagerie échographique, les comptes rendus, la télé-expertise ainsi que le télédiagnostic entre les professionnels de santé.

Des imprime ecran de l'app:

![Screen Shot 1](https://github.com/XD-OB/Echo_Tele_Expertise/blob/master/extras/ete_home.JPG)

![Screen Shot 2](https://github.com/XD-OB/Echo_Tele_Expertise/blob/master/extras/ete_screen2.JPG)

![Screen Shot 3](https://github.com/XD-OB/Echo_Tele_Expertise/blob/master/extras/ete_screen3.JPG)

# Structure de la base de données
Elle est detailler dans le pdf et le XLSX dans le dossier Extras

# Technologies utiliser:
- Backend: Django3 (Python3+)
- FrontEnd: HTML, CSS, Bootstrap4, Javascript, JQuery
- Base de Données: PostgreSQL (Relationnelle)

# Simple Methode pour lancer l'app:
## Pour la premiere fois
### Lancer l'app principale:
- Installer Python3+
- Installer pip
- Installer PostgresSQL
- (Si vous ete sous le systeme d'exploitation Windows: vous devriez Telecharger Python et PostgresSQL puis les installer)
- it clone the project from the git or i will send it to you.
- Dans echoTeleExpertise creer un dossier media
- Dans media creer 2 dossiers: avatars  documents
- dans avatars coller le fichier dans extras: empty_profile.jpg
- Dans le terminal ou le CMD dans le dossier de l'app:
- pip install pipenv
- pipenv shell
- pipenv install -r requirements.txt
- Dans pgadmin creer la base de donnée 'etedb'
- Dans settings.py modifier username & password
- cd echoTeleExpertise
- python manage.py makemigrations
- python manage.py migrate
- python manage.py createsuperuser
- python manage.py runserver
==> Dans cette étape le site est lancer dans: 127.0.0.1:8000 (Mentionner dans le msg)
## Lancer l'app de dwv:
Dans le Dossier de l'app ouvrir un autre terminal (laisser le dernier terminal running :) ).
- Download & Install NodeJs
- Download & Install Yarn
- cd ete-dwv
- yarn install
- yarn start
==> Tous est bien :)



## Dans le quotidien (toujours XD)
### Lancer l'app principale
Dans le dossier de l'app telecharger la premiere fois
- pipenv shell
- cd echoTeleExpertise
- python manage.py runserver
==> L'app principale est lancer dans 127.0.0.1:8000 (Mentionner dans le msg)
### Lancer l'app de dwv:
Dans le dossier de l'app telecharger la premiere fois
- cd ete-dwv
- yarn start
==> C'est terminer!


# Installation:
## dépendances:
- installer python 3+
- installer pip
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

# DICOM Web Viewer:
Le visionneur dicom utiliser:
- https://github.com/ivmartel/dwv-jqui/releases/tag/v0.4.0
- yarn install
- yarn start

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

## The myconvertions:
contain a template filter used to transform int -> str,
instead of convert in the views fonction, my choice was to let it in the template.
