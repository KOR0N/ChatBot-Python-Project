# Membre de l’équipe :
- Le Galliard Alexandre 
- Dauvel Alexandre
- Mathis Gosselin

Lien vers le dépot Git :
https://github.com/KOR0N/Projet-Python

# Fonctionnalités principales de notre application :
1) Afficher la liste des mots les moins importants dans le corpus de documents.  
2) Afficher le(s) mot(s) ayant le score TD-IDF le plus élevé.
3) Indiquer le(s) mot(s) le(s) plus répété(s) par le président donné.
4) Indiquer le(s) nom(s) du (des) président(s) qui a (ont) parlé d'un mot donné et celui qui l’a répété le plus de fois.
5) Indiquer le premier président à parler d'un thème donné.
6) Afficher, hormis les mots dits « non importants », quel(s) est(sont) le(s) mot(s) que tous les présidents ont évoqués.



!!! Attention : si vous utiliser pycharm, ajoutez "./" devant pour les chemins d'accès ("./speeches" et pas "speeches") !!!

# Instructions d’exécution du code :
- Call of the function
- Fonction whoes extract the name of presidents
- Attribuer pour chaque nom de président le prénom associé
- Parcourir chaque fichier dans le dossier d'entré
- Convertir en minuscules
- Vérifie si c'est une lettre majuscule
- Créer le chemin du nouveau fichier dans le dossier de sortie
- Écrire le contenu converti dans le nouveau fichier
- Parcourir chaque fichier dans le dossier d'entré
- Faire une sélection de tous les caractere devant être supprimé
- Faire une sélection de tous les caractere devant être remplacé par un espace
- Les autres sont ajoutés au nouveau contenu
- Écrire le contenu converti dans le nouveau fichier
- convertir_majuscule_en_minuscules("speeches","cleaned")
- suppression_ponctuation("cleaned")
- Lire le contenu du fichier
- Créer le dictionnaire pour le nombre d'occurence de chaque mots 
- Séparer les mots de la chaîne de caractere en une liste 
- Parcourir les mots de la liste string 
- Ajouter le mot au dictionnaire si il n'existe pas 
- Incrementer 1 pour chaque mot 
- print(tf_score("Voici un exemple de chaîne de caractere, elle sert à tester si la fonction marche bien par exemple le mot exemple apparait 3 fois :)")
- Dictionnaire pour stocker le nombre de documents contenant chaque mot
- Parcourir tous les fichiers dans le répertoire du corpus
- Lire le contenu du fichier
- Mettre à jour la fréquence des mots dans les documents
- Calculer le score IDF pour chaque mot
- Exemple d'utilisation de la fonction
- Trouver l'indice du score TF-IDF le plus élevé
- Afficher le résultat
- Trouver l'indice du score TF-IDF le plus élevé
- Récupérer le mot correspondant à l'indice trouvé
- Afficher le résultat
- Utiliser la fonction avec les données existantes
- mots_moins_importants(matrice_tf_idf, tf_list, dossier)
- mot_moin_important(matrice_tf_idf, tf_list, dossier)
- print(presidents_name_display(name_association(recup_nom(list_of_files("speeches","txt")))))

# Précision sur l'organisation :

Mathhis Go : impossibilité d'installer et d'utuliser le logiciel Pycharm, il a donc été difficile de travailler en groupe à distencce cependatant nosu avoins trouver le moyen de travailler sur le même pc.
Alexandre LGD : On a travaillé sur l'ordinateur d'Alexandre Dauvel, car mon PyCharm ne voulait pas installer la version de Python adaptée.

