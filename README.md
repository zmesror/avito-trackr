# Avito-Trackr : Suivi de l'évolution des prix immobiliers au Maroc

Le projet Avito-Trackr est une application qui permet de collecter des données sur l'évolution des prix de l'immobilier au Maroc depuis le site avito.ma, de stocker les données dans une base de données MySQL, de calculer le prix moyen par mètre carré d'un appartement dans différentes villes, et de visualiser les données avec Matplotlib.

## Table des matières
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Configuration](#configuration)
- [Exécution des Spiders Scrapy](#exécution-des-spiders-scrapy)
- [Enregistrement des Données Collectées dans un Fichier](#enregistrement-des-données-collectées-dans-un-fichier)
- [Contribuer](#contribuer)
- [Licence](#licence)

## Installation

Avant d'utiliser Avito-Trackr, assurez-vous d'avoir Python (version 3.6 ou supérieure) installé sur votre système.

1. Clonez le dépôt GitHub :

    ```
    git clone https://github.com/your-user/avito-trackr.git
    ```

2. Installez les dépendances requises :

    ```
    pip install -r requirements.txt
    ```

3. Créez un fichier de configuration `config.json` et placez-le dans le répertoire `avito_trackr/avitoscraper`. Le format du fichier de configuration doit être le suivant :

    ```json
    {
        "api_key": "VOTRE_CLÉ_API"
    }
    ```

**Note :** La clé API est utilisée pour obtenir des user agents.

## Utilisation

### Configuration

Avant d'utiliser l'application, assurez-vous d'avoir configuré le fichier `config.json` avec votre clé API, que vous devez obtenir sur [ScrapeOps](https://scrapeops.io/).

### Collecte de Données

La collecte de données est gérée par Scrapy. Les données collectées seront automatiquement stockées dans la base de données MySQL spécifiée.


### Exécution des Spiders Scrapy

Pour exécuter les spiders Scrapy et spécifier la base de données pour le stockage des données, vous pouvez suivre ces étapes :

1. Ouvrez le fichier `pipelines.py` dans le répertoire `avito_trackr/avitoscraper`.

2. Dans le fichier `pipelines.py`, vous pouvez spécifier les paramètres de la base de données pour le stockage des données. Assurez-vous d'avoir configuré votre base de données MySQL avec les configurations nécessaires dans les paramètres.

3. Une fois que vous avez configuré les paramètres de la base de données, vous pouvez exécuter les spiders Scrapy avec la commande suivante :

```
scrapy crawl propertyspider
```

Cette commande lancer le spider propertyspider, qui commencera à collecter des données à partir du site avito.ma et à les stocker dans la base de données MySQL spécifiée dans SaveToMySQLPipeline.

### Enregistrement des Données Collectées dans un Fichier

Si vous souhaitez enregistrer les données collectées dans un fichier (par exemple, JSON ou CSV), vous pouvez utiliser la commande suivante :
```
scrapy crawl propertyspider -O file.json
```
ou
```
scrapy crawl propertyspider -O file.csv
```

Cette commande exécutera les spiders et enregistrera les données collectées dans le fichier spécifié, au format JSON ou CSV.

### Analyse des Données et Visualisation

L'analyse des données et la visualisation sont gérées par le fichier `price.py` dans le répertoire `data`. Il contient une classe `Price` qui permet de calculer diverses statistiques sur les données.

Pour effectuer une analyse ou générer des graphiques, vous pouvez utiliser le script principal `price.py` en passant des arguments pour spécifier ce que vous souhaitez faire.

Exemples d'utilisation :

- Pour calculer le prix moyen par mètre carré pour une ville spécifique :
    ```
    python price.py --city Casablanca
    ```

- Pour calculer le prix moyen par mètre carré pour toutes les villes :
    ```
    python price.py --calculate-all
    ```

- Pour générer des graphiques des moyennes par ville :
    ```
    python price.py --calculate-all --plot-cities
    ```

- Pour calculer le prix moyen par mètre carré sur une période donnée :
    ```
    python price.py --time 5
    ```

- Pour générer un graphique de l'évolution des prix au fil du temps :
    ```
    python price.py --time 5 --plot-time
    ```

N'hésitez pas à explorer les options disponibles dans `price.py` pour personnaliser votre analyse et vos graphiques.

**Note :** Il est important de noter que ce projet est principalement destiné à des fins d'apprentissage.

## Contribuer

Si vous souhaitez contribuer au projet Avito-Trackr, nous vous accueillons avec des suggestions, des rapports de bogues ou des demandes de fonctionnalités. Vous pouvez ouvrir une issue sur GitHub ou soumettre une pull request.
