<a>
    <img src="https://dev.tranquil.it/samba/fr/doc/_images/Samba.png" title="Aimeos" align="right" height="60" />
</a>

# Samba-DC-GUI 

[![Samba-DC-GUI](http://www.linux-migration.fr/Cap0.png)](http://https://www.samba.org//)

## Table des matières

- [Installation](#installation)
    - [Copie des fichiers](#copie-des-fichiers)
    - [Lancement](#lancement)
- [Utilisation](#utilisation)
    - [Ajout des utilisateurs](#adduser)
    - [Exporter un fichier CSV](#exportusers)
- [Template HTML](#template)
    - [base.html](#template-base)
    - [index.html](#template-index)
    - [create.html](#template-create)
    - [delete.html](#template-delete)
    - [liste.html](#template-liste)
    - [table.html](#template-table)
- [Licence](#licence)
- [Liens](#liens)

## Installation

Vous devez disposer des programmes suivants:

- Python3
- Flask (`pip install Flask`).
- D'un système Linux avec un contrôler de domaine Samba4 fonctionnel.

### Copie des fichiers:

`git clone https://github.com/rchaudanson/Samba-DC-GUI.git`

`cd Samba-DC-GUI`




### Lancement:

**Note:**  Vous devez déclarer les variables d’environnement suivantes:

`export FLASK_APP=app`

`export FLASK_DEBUG=1`
<br><br>

Puis lancer l'application:

`flask run`
<br><br>



## Utilisation

### Afficher l'interface web:

Démarrez votre navigateur internet et accédez à l'adresse suivante:

`http://127.0.0.1:5000`

![ ](http://www.linux-migration.fr/Cap2.png)

### Ajout des utilisateurs

* Cliquez sur **Créer des utilisateurs** puis sur **Créer un utilisateur**.
* Indiquez les information concernant l'utilisateur et validez.

![ ](http://www.linux-migration.fr/Cap5.png)



### Exporter un fichier CSV

Vous pouvez importer plusieurs utilisateurs depuis un fichier CSV.<br>
Pour cela:

* Cliquez sur **Créer des utilisateurs** puis sur **Importer CSV**.
* Le fichier CSV doit être formater de la façon suivante:

```
jlogan,motdepasse,julien,logan,jlogan@isis.local,569
dsam,motdepasse,sam,dadal,dsam@isis.local,522
vmartine,motdepasse,martine,vevert,vmartine@isis.local,524
wjulie,motdepasse,julie,winter,wjulie@isis.local,787
```

* Soit:
`LOGIN,MOTDEPASSE,PRENON,NOM,MAIL,TEL`

![ ](http://www.linux-migration.fr/Cap4.png)



## Template HTML

L'interface est axées autour de 6 templates HTML situés dans le dossier "template" à la racine du projet:  

* base.html
* index.html
* create.html
* delete.html
* liste.html
* table.html


**Note:** 

* Le template "tables" est un tableau HTML généré à chaque consultation de la liste des utilisateurs. 
* Le template "delete" est n'est actuellement pas utilisé.




## Licence

????????????????????????

## Liens

* [Samba](https://www.samba.org/)
* [Flack](https://flask.palletsprojects.com/)
* [Python](https://www.python.org/)
