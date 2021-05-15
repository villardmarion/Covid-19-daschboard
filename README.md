# Covid-19-dashboard
This is a simplified Covid19 dashboard developed as part of a school project.
This dashboard was 100% developed using python v. 3.7
## Libraries
### Dash
Dash is a productive Python framework for building web analytic applications.

Written on top of Flask, Plotly.js, and React.js, Dash is ideal for building data visualization apps with highly custom user interfaces in pure Python. 
It's particularly suited for anyone who works with data in Python.

Through a couple of simple patterns, Dash abstracts away all of the technologies and protocols that are required to build an interactive web-based application. 
Dash is simple enough that you can bind a user interface around your Python code in an afternoon.

Dash apps are rendered in the web browser. You can deploy your apps to servers and then share them through URLs. 
Since Dash apps are viewed in the web browser, Dash is inherently cross-platform and mobile ready.
Dash version: 
*Documentation* : https://dash.plotly.com/introduction 
### Plotly
## Data
### World data
Pour les informations globales sur le monde entier, la base de données de l’OMS (que l’on peut télécharger via le lien : https://covid19.who.int/WHO-COVID-19-global-data.csv) a été utilisée notamment pour calculer les indicateurs mondiaux tels que le nombre de cas ou de décès. Cette base de données contient l’ensemble des informations pour tous les pays et est mise à jour tous les jours ce qui permet d’avoir des indicateurs mis à jour en temps réel.
Pour les informations au sujet de la vaccination, une autre base de données de l’OMS a été utilisée (que l’on peut télécharger via le lien : https://covid19.who.int/who-data/vaccination-data.csv). Cette base de données est mise à jour régulièrement selon les pays qui transmettent les informations le plus souvent possible.

### French data
Pour les informations ciblées sur la France, plusieurs bases de données ont été utilisées :
Pour les données hospitalière, la base de données utilisée est l’une de celle disponible en open sourc esur le site du gouvernement (que l’on peut télécharger via le lien : https://www.data.gouv.fr/fr/datasets/r/6fadff46-9efd-4c53-942a-54aca783c30c). Cette base de données contient des informations sur la date, les départements, les hospitalisations, réanimations, décès ou retour à domicile des patients. Elle a été utilisée dans le dashboard pour calculer notamment les indicateurs des pages vue globale de la situation en France, les réanimations et les décès.
Pour les données générales et notamment pour obtenir le nombre total de décès une autre base de données trouvées en open source sur le site du gouvernement a été utilisée (que l’on peut télécharger via le lien : https://www.data.gouv.fr/fr/datasets/r/63352e38-d353-4b54-bfd1-f1b3ee1cabd7). Cette base de données contient les informations concernant les départements, les sexes, les hospitalisations, réanimations, décès ou retour à domicile. Elle a été utilisée pour calculer notamment les indicateurs liés au ratio des sexes quant au nombre de décès ou de réanimations.
Pour la situation vaccinale et toujours provenant de la même source une autre base de données a été utilisée (que l’on peut télécharger via le lien : https://www.data.gouv.fr/fr/datasets/r/b8d4eb4c-d0ae-4af6-bb23-0e39f70262bd). Cette base contient les informations des différents vaccins concernant le nombre de vaccinations par la première dose et la seconde dose. Cette base de données a été choisie car elle est de petite dimension mais contient toutes les informations voulues pour les indicateurs présentés dans cette partie du dashboard.

## Dashboard
### Monde
### France
#### France Réanimation
#### France Décès
#### France Vaccination

# Modélisation SIR:
Source de ce jeu de données : https://coronavirus.politologue.com - Les données proposées dans ce fichier sont une compilation des données proposées par le CSSE (The Johns Hopkins University) https://gisanddata.maps.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6
Les données de ce fichier sont celles qui sont produites pour générer les graphiques sur https: //coronavirus.politologue.com
Vous pouvez utiliser ces données sans problème et une référence à https://coronavirus.politologue.com sera appréciable


