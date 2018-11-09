**Nom du plugin** : Socle MOS
**Descriptif court** : Outil de génération et de croisement de modes d'occupation du sol
**Descriptif long** : 
Ce plugin propose 3 grandes fonctionnalités :
- Constitution d'un socle de mode d'occupation des sols à l'échelle parcellaire (t0)
- Mise à jour géométrique et attributaire (t+1) sur un socle existant
- Création d'un millésime attributaire sur une date antérieure (t-1)

**Étiquettes** : socle, mos, ocs, parcelle, processing, postgis
**Plus d'infos**
  **Page d'accueil** : https://www.sirs-fr.com/  
  **Suivi des anomalies** : http://projet.sirs-fr.com/project/nicolasrochard-adeupa/issues
  **Dépôt du code** : http://git.sirs-fr.com/projet/adeupa/tree/master/Outil-Socle-MOS

**Auteur** : Corentin Falcon (SIRS) sans lien ou si c'est obligatoire, lien vers ton email
**Version** : 0.4

**Changelog** :
version 0.4
* Automatisation de la méthode de génération de socle pour l'ADEUPA
* Conversion des processus ArcGIS vers PostGIS
* Ajout de nouvelles fonctions PostGIS
* Prise en compte des limites communales BDParcellaire
* Prise en compte des fichiers fonciers plutôt que des données brutes MAJIC
* Optimisation de la pertinence du codage automatique
* Optimisation du temps de traitements
* Ajout d'un outil de correction des géométries invalides