# Rapport de Fin de Projet

**Titre du Projet :** Programmation Orientée Objet en Python

**Auteur :** [Votre Nom]

**Filière :** IID1

**École :** École Nationale des Sciences Appliquées (ENSA) de Khouribga

**Année Universitaire :** 2025-2026

---

## Remerciements

[Vos remerciements ici]

---

## Résumé

[Votre résumé ici]

---

## Table des Matières

1.  Introduction
2.  Chapitre 1 : Concepts de la Programmation Orientée Objet
3.  Chapitre 2 : Fonctionnalités Orientées Objet de Python
5.  Chapitre 4 : Implémentation et Architecture du Projet
6.  Chapitre 5 : Tests
7.  Conclusion

---

## Introduction

[Introduction générale au projet, son contexte, ses objectifs, etc.]

---

## Chapitre 1 : Concepts de la Programmation Orientée Objet

*   **Classes et Objets :** [Explication]
*   **Encapsulation :** [Explication]
*   **Héritage :** [Explication]
*   **Polymorphisme :** [Explication]
*   **Abstraction :** [Explication]

---

## Chapitre 2 : Fonctionnalités Orientées Objet de Python

*   **Syntaxe des classes et des objets en Python :** [Explication et exemples]
*   **Méthodes spéciales (dunder methods) :** [Explication et exemples]
*   **Décorateurs :** [Explication et exemples]
*   **Gestion des exceptions :** [Explication et exemples]


---

## Chapitre 3 : Implémentation et Architecture du Projet
*   **Architecture du project (files structure and what each folder does)**
    1. Racine (/) & pages/ (Vue) :
        app.py sert de point d'entrée et de page d'accueil.
        Le dossier pages/ utilise le système de routage natif de Streamlit pour générer automatiquement la navigation latérale, isolant les interfaces par rôle (Admin, Professeur, Étudiant).
    2. src/models/ (Modèle) :
        Contient les classes Python pures qui définissent la structure de nos données. Ces fichiers garantissent que les données manipulées dans l'application respectent un format strict (encapsulation).
    3. src/services/ (Contrôleur/Service) :
        data_manager.py agit comme le chef d'orchestre. Il centralise toutes les opérations de lecture et d'écriture vers les fichiers JSON. L'interface graphique ne touche jamais directement aux fichiers JSON ; elle passe toujours par ce service.
    4. data/ (Persistance) :
        Stockage léger en format JSON, permettant une portabilité totale sans nécessiter de serveur SQL dédié pour cette phase du projet.

*   **Description détaillée des modules et des classes :**

    1. src/models/etudiant.py
        A. Classe Étudiant (src/models/etudiant.py)
        La classe Etudiant est l'entité centrale de l'application. Elle ne se contente pas de stocker les données administratives ; elle encapsule également la logique liée à la scolarité de l'élève.
        Fonctionnalités clés :
        Gestion d'identité et Authentification : La classe stocke les informations personnelles ainsi qu'un mot de passe (ajouté pour sécuriser l'accès au portail étudiant).
        Intégrité des données : La méthode ajouter_note() vérifie systématiquement si l'étudiant est inscrit au module avant d'accepter une note. Cela empêche les incohérences dans la base de données.
        Sérialisation (Mapping JSON) :
        to_dict() : Convertit l'objet en dictionnaire pour l'écriture dans etudiants.json.
        from_dict() : Reconstruit un objet Etudiant complet à partir des données brutes, assurant la persistance de l'état entre les sessions
    2. src/models/professeur.py
        La classe Professeur est structurée de manière similaire à la classe   Etudiant pour maintenir une cohérence dans le code, mais sa logique métier est focalisée sur l'enseignement plutôt que sur l'évaluation.
        Fonctionnalités clés :
        Gestion des Affectations : L'attribut modules_enseignes est une liste de chaînes de caractères (codes de modules). Plutôt que de stocker des objets Module entiers, nous stockons uniquement leurs identifiants uniques. Cela réduit la complexité de la sérialisation et évite les références circulaires lors de la sauvegarde en JSON.
        Méthode assigner_module : Cette méthode garantit l'unicité des assignations (un professeur ne peut pas être assigné deux fois au même module dans sa liste).
        Persistance : Comme pour l'étudiant, les méthodes to_dict et from_dict assurent la transformation des données pour le stockage.
    3. src/models/module.py (and Note if it's separate or included there)
        La classe Module représente une unité d'enseignement. Elle agit comme un carrefour relationnel entre le professeur et les étudiants.
        Fonctionnalités clés :
        Référencement par Identifiant (Loose Coupling) :
        Une décision d'architecture importante a été prise ici : la classe stocke id_professeur et une liste d'id_etudiant (des chaînes de caractères), plutôt que les objets Python eux-mêmes.
        Pourquoi ? Cela allège considérablement la structure des données et simplifie la sauvegarde en JSON. Cela évite les références circulaires infinies (Un étudiant contient un module qui contient l'étudiant, etc.).
        Gestion des Inscriptions : Les méthodes ajouter_etudiant et supprimer_etudiant permettent de gérer dynamiquement la liste de classe, assurant qu'un étudiant ne soit pas inscrit deux fois (gestion des doublons).
    4. Classe Note (src/models/note.py)
        La classe Note est une classe utilitaire qui structure l'évaluation. Elle est conçue pour être contenue dans la liste des notes d'un étudiant.
        Fonctionnalités clés :
        Validation des Données à l'Instanciation :
        Le constructeur __init__ inclut une validation stricte : if not (0 <= valeur <= 20).
        Cela garantit qu'il est techniquement impossible de créer un objet Note invalide dans le système. Si une interface ou un script tente d'insérer une note de 25/20, le programme lèvera une erreur ValueError immédiatement, protégeant l'intégrité des calculs de moyenne.
*   **explaining json files and what they serves fo**
        Cette section détaille la couche de persistance des données. Le choix s'est porté sur le format JSON (JavaScript Object Notation) pour sa légèreté, sa lisibilité par l'humain et sa compatibilité native avec Python.
        Ces fichiers agissent comme une base de données NoSQL simplifiée document-oriented.
        Rôle des fichiers :
        etudiants.json : Contient la liste complète des étudiants, incluant leurs informations personnelles, leur mot de passe haché (dans une version future) ou brut, ainsi que l'historique de leurs notes et inscriptions.
        professeurs.json : Stocke les profils des enseignants et la liste des modules qu'ils gèrent.
        modules.json : Répertorie tous les cours disponibles, servant de catalogue central pour l'application.
*   **explaining data managaer and its methods and what each one does**
*   **explaining app.py and how to use streamlit to build the interface**

---

## Chapitre 5 : Tests

*   **Stratégie de test :** [Description de l'approche de test]
*   **Tests unitaires :** [Exemples de tests unitaires]

---

## Conclusion

*   **Bilan du projet :** [Synthèse des réalisations]
*   **Apports personnels :** [Ce que vous avez appris]
*   **Perspectives d'amélioration :** [Idées pour le futur]


