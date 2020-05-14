# Installation

Pour commencer, il vous faut installer les dépendances listées dans **requirements.txt**:

```bash
pip install -r requirements.txt
```

Ensuite, il faut télécharger PhantomJS et placer l'exécutable a la racine de ce projet. PhantomJS est téléchargable au lien suivant: https://phantomjs.org/download.html


# Récupérer le fil d'actualité d'une oeuvre

Pour récupérer le fil d'actualité d'une oeuvre, il suffit de récupérer l'url de la fiche de l'oeuvre que vous désirez et de lancer la commande suivante dans le terminal.


```bash
python scrap_feed.py [URL]
```

Il est également possible de définir une date limite si vous ne souhaitez pas redéscendre tout en bas du fil d'actualité d'une oeuvre. Pour cela il suffit d'ajouter un mois limite et une année limite, la récupération s'arretera alors des qu'une action datée du mois et de l'année en question sera récupérée.

```bash
python scrap_feed.py [URL] [mois_limite] [annee_limite]
```

Si je veux par exemple récupérer le fil d'actualité de Blade Runner jusqu'en mars 2018, la commande sera:

```bash
python scrap_feed.py https://www.senscritique.com/film/Blade_Runner/494050 2 2018
```