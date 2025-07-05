# My Awesome Project

Behold My Awesome Project!

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

License: MIT

## Settings

Moved to [settings](https://cookiecutter-django.readthedocs.io/en/latest/1-getting-started/settings.html).

## Basic Commands

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy library_prj

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/2-local-development/developing-locally.html#using-webpack-or-gulp).

## Deployment

The following details how to deploy this application.


# TODO – Fonctionnalités de l'application de gestion de librairie

- [x] Gestion des livres
  - [x] Ajouter, modifier, supprimer des livres
  - [x] Rechercher et filtrer les livres (titre, auteur, genre, ISBN, etc.)
  - [x] Gérer les stocks (quantité, seuil d'alerte)
  - [x] Gérer les catégories/genres
- [x] Gestion des auteurs et éditeurs
  - [x] Ajouter, modifier, supprimer des auteurs
  - [x] Ajouter, modifier, supprimer des éditeurs
  - [x] Lier livres, auteurs et éditeurs
- [x] Gestion des utilisateurs/clients
  - [x] Inscription, connexion, gestion du profil
  - [x] Historique des emprunts/achats
  - [x] Gestion des réservations
- [x] Gestion des emprunts et retours (si bibliothèque)
  - [x] Enregistrer les emprunts et retours
  - [x] Gérer les dates d'échéance et pénalités de retard
  - [ ] Notifications de rappel
- [x] Gestion des ventes (si librairie commerciale)
  - [x] Enregistrer les ventes
  - [x] Gestion du panier d'achat
  - [x] Facturation et reçus
- [x] Gestion des réservations
  - [x] Réservation de livres en ligne
  - [x] Notification lors de la disponibilité
- [x] Statistiques et rapports
  - [x] Statistiques sur les ventes/emprunts
  - [x] Livres les plus populaires
  - [x] Rapports de stock
- [x] Gestion des utilisateurs (administration)
  - [x] Gestion des rôles (admin, employé, client)
  - [x] Gestion des permissions
- [x] Interface multilingue
  - [x] Support du français, anglais, etc.
- [x] Autres fonctionnalités
  - [x] Gestion des avis et notes sur les livres
  - [ ] Système de recommandations
  - [ ] Exportation des données (CSV, PDF)
  - [ ] Intégration avec des systèmes de paiement (si vente en ligne)

---

Ce document servira de référence pour le développement du projet.

# Référence – Applications Django à créer

Voici la liste des applications à créer pour couvrir toutes les fonctionnalités :

- **books** : gestion des livres, catégories, genres, stock
- **authors** : gestion des auteurs
- **publishers** : gestion des éditeurs
- **users** : gestion des utilisateurs, profils, rôles
- **loans** : gestion des emprunts, retours, pénalités, rappels
- **sales** : gestion des ventes, panier, facturation
- **reservations** : gestion des réservations de livres
- **reports** : génération de statistiques et rapports
- **reviews** : gestion des avis, notes, recommandations

---
