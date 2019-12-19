
# Test de Falcon et de Pypy

Ce test a pour but de comparer deux technologies permettant de créer des applications web Python ainsi que deux interpréteurs Python différent. 

L'idée sous jacente est de trouver la combinaison fournissant les meilleures performances.

Les deux frameworks web considérés sont : 

* Flask
* Falcon

Selon sa documentation. Falcon devrait en toute logique être plus rapide que Flask. 

Les deux interpréteurs Python mis à l'épreuve sont : 

* CPython: Interpréteur de base de python
* Pypy : Un interpréteur Python mettant en place de la compilation [JIT](https://fr.wikipedia.org/wiki/Compilation_%C3%A0_la_vol%C3%A9e) permettant en toute logique une exécution plus rapide du code.

Ces deux technologies ainsi que les deux interpréteurs qui vont être testés représentent donc 4 combinaisons : 

1. Falcon sur Pypy
2. Falcon sur CPython
3. Flask sur Pypy
4. Flask sur CPython

## Use case utilisé dans le cadre de ce test
Le code suivante va être exécuté afin de générer 500.000 nombres qui seront retournés par une resource `/numbers` de chacune des application:

```
numbers = []
for _ in range(10):
    for _ in range(100):
        for _ in range(500):
            numbers.append(random.randint(0, 1000000))
```

Il est à noter que ce code est *intentionnellement* fort peu performant. 

## Canvas de test
Chacune des applications tourne dans un container Docker. Elles sont ainsi disponibles aux URLs suivantes : 

1. Falcon sur Pypy : [http://localhost:8000/numbers](http://localhost:8000/numbers)
2. Falcon sur CPython : [http://localhost:8001/numbers](http://localhost:8001/numbers)
3. Flask sur Pypy : [http://localhost:8002/numbers](http://localhost:8002/numbers)
4. Flask sur CPython : [http://localhost:8003/numbers](http://localhost:8003/numbers)

La méthode de test ici considérée va être d'envoyer 1500 requêtes à chaque application et d'étudier la distribution du temps nécessaire pour chaque combinaisons.

## Implémentation


```python
import requests
import datetime
import numpy as np

FALCON_PYPY = "http://localhost:8000/numbers"
FALCON_CPYTHON = "http://localhost:8001/numbers"
FLASK_PYPY = "http://localhost:8002/numbers"
FLASK_CPYTHON = "http://localhost:8003/numbers"
```


```python
def compute_request_timing(url):
    before = datetime.datetime.now()
    response = requests.get(url)
    after = datetime.datetime.now()
    assert response.ok
    return (after - before).total_seconds()

def perform_performance_test(url, nb_samples=1500):
    time = np.array([compute_request_timing(url) for _ in range(nb_samples)])
    return {
        "min": time.min(),
        "25%": np.percentile(time, 25),
        "mean": time.mean(),
        "median": np.median(time),
        "75%": np.percentile(time, 75),
        "max": time.max(),
        "total": time.sum()
    }
```

## Exécution

#### Test de Falcon + Pypy


```python
perform_performance_test(FALCON_PYPY, nb_samples=1500)
```




    {'min': 0.104927,
     '25%': 0.1220365,
     'mean': 0.127866198,
     'median': 0.12542950000000003,
     '75%': 0.129468,
     'max': 1.100328,
     'total': 191.799297}



#### Test de Falcon + CPython


```python
perform_performance_test(FALCON_CPYTHON, nb_samples=1500)
```




    {'min': 0.835484,
     '25%': 0.8495275,
     'mean': 0.8609402780000001,
     'median': 0.8543225000000001,
     '75%': 0.8612645000000001,
     'max': 1.148754,
     'total': 1291.410417}



#### Test de Flask + Pypy


```python
perform_performance_test(FLASK_PYPY, nb_samples=1500)
```




    {'min': 0.108334,
     '25%': 0.12477099999999999,
     'mean': 0.13695412666666668,
     'median': 0.132899,
     '75%': 0.14257925,
     'max': 1.17332,
     'total': 205.43119000000002}



#### Test de Flask + CPython


```python
perform_performance_test(FLASK_CPYTHON, nb_samples=1500)
```




    {'min': 0.837264,
     '25%': 0.85495275,
     'mean': 0.8687557246666668,
     'median': 0.8608255,
     '75%': 0.869811,
     'max': 1.871099,
     'total': 1303.1335870000003}



## Analyse des résultats
On remarque que le plus gros gain de performance est obtenu lorsque l'on passe de CPython à Pypy. 

En effet, que ce soit pour Falcon (683%) ou Flask (658%), ont remarque une augmentation de plus de 650% de l'application (elle est 6,5 fois plus rapide). 

Ensuite, on remarque que Falcon est 110% plus rapide que Flask (les requêtes prennent 10% moins de temps à être exécutées). 

Au vu de cette analyse, il semble raisonnable de dire que le plus gros "quick win" est de changer d'interpréteur pour passer de CPython à Pypy. 
Cette remarque est mise en exergue par la constatation que cette modification est également la plus simple à mettre en place. 

Effectivement, ce changement ne demande qu'une modification de l'image Docker de base ainsi que des commandes d'installation des dépendances de la dite application. 

Le passage de Falcon à Flask demande lui un temps plus important car une modification/réécriture du core source est nécessaire afin de se conformer aux classes et synthaxes de cette librarie. 


```python

```
