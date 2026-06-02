# Catalog Service

Premier micro-service du projet FlexShop permettant de gérer le catalogue de produits via une API REST Django REST Framework.

## Fonctionnalités

- CRUD complet sur les produits.
- Pagination automatique.
- Filtrage par catégorie.
- Recherche par nom et description.
- Tri par prix en centimes, date de création et stock.
- Documentation OpenAPI avec Swagger UI.
- Endpoint custom pour les produits en stock faible.
- Validation métier sur le prix et le stock.
- Prix stocké en centimes avec `price_cents`.

## Prérequis

- Python 3.12+
- Pip

## Installation et démarrage

1. Cloner le projet et se placer dans le répertoire :

```bash
cd catalog-service/catalog-service
```

2. Créer et activer l'environnement virtuel :

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Installer les dépendances :

```bash
pip install -r requirements.txt
```

4. Appliquer les migrations :

```bash
python manage.py migrate
```

5. Lancer le serveur de développement :

```bash
python manage.py runserver
```

## Endpoints principaux

- `GET /api/v1/products/` : lister les produits.
- `POST /api/v1/products/` : créer un produit.
- `GET /api/v1/products/{id}/` : récupérer un produit.
- `PATCH /api/v1/products/{id}/` : modifier partiellement un produit.
- `PUT /api/v1/products/{id}/` : remplacer un produit.
- `DELETE /api/v1/products/{id}/` : supprimer un produit.
- `GET /api/v1/products/low-stock/?threshold=5` : lister les produits avec un stock faible.

## Exemples de requêtes

```bash
curl http://localhost:8000/api/v1/products/
curl http://localhost:8000/api/v1/products/?category=electronics
curl http://localhost:8000/api/v1/products/?search=casque
curl http://localhost:8000/api/v1/products/?ordering=price_cents
curl http://localhost:8000/api/v1/products/?page=2
curl http://localhost:8000/api/v1/products/low-stock/?threshold=5
```

Créer un produit :

```bash
curl -X POST http://localhost:8000/api/v1/products/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Souris","description":"Souris sans fil","price":"29.99","stock":50,"category":"electronics"}'
```

## Documentation OpenAPI

- Swagger UI : [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)
- Schéma OpenAPI : [http://localhost:8000/api/schema/](http://localhost:8000/api/schema/)

## Tests unitaires

Pour lancer la suite de tests automatisés :

```bash
python manage.py test products
```

## Qualité du rendu

Avant de rendre le projet, vérifier que les fichiers suivants ne sont pas inclus dans le dépôt ou l'archive :

- `db.sqlite3`
- `venv/`
- `.venv/`
- `__pycache__/`
- `*.pyc`
