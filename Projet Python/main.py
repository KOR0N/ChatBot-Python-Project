import os
import math


def list_of_files(directory, extension):
    files_names = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)
    return files_names

# Call of the function
directory = "speeches"
files_names = list_of_files(directory, "txt")

# Fonction whoes extract the name of presidents
def recup_nom(files_names):
    presidents_name = []
    for filename in files_names:
        filename = filename.replace('Nomination_','')
        filename = filename.replace('.txt','')
        for caractere in filename:
            if (caractere < 'a' or caractere > 'z') and (caractere < 'A' or caractere > 'Z') and caractere!=" ":
                filename = filename.replace(caractere,'')
        presidents_name.append(filename)
    return presidents_name

def name_association(presidents_name):
    for names in range(len(presidents_name)):
        # Attribuer pour chaque nom de président le prénom associé
        match presidents_name[names]:
            case "Chirac":
                presidents_name[names] = "Jacque " + presidents_name[names]
            case "Hollande":
                presidents_name[names] = "François " + presidents_name[names]
            case "Macron":
                presidents_name[names] = "Emmanuel " + presidents_name[names]
            case "Mitterrand":
                presidents_name[names] = "François " + presidents_name[names]
            case "Sarkozy":
                presidents_name[names] = "Nicolas " + presidents_name[names]
            case "Giscard dEstaing":
                presidents_name[names] = "Valéri " + presidents_name[names]
    return presidents_name

def presidents_name_display(presidents_name):
    print("Les présidents sont :")
    for i in set(presidents_name):
        print(i)

def convertir_majuscule_en_minuscules(dossier_entree,dossier_sortie):
    # Parcourir chaque fichier dans le dossier d'entré
    for fichier in os.listdir(dossier_entree):
        fichier_entree = os.path.join(dossier_entree, fichier)

        with open(fichier_entree, 'r') as file:
            contenu = file.read()
            contenu_minuscule = ""

            # Convertir en minuscules 
            for caractere in contenu :
                # Vérifie si c'est une lettre majuscule
                if 65 <= ord(caractere) <= 90:
                    contenu_minuscule += chr(ord(caractere)+32)
                else:
                    contenu_minuscule += caractere

            # Créer le chemin du nouveau fichier dans le dossier de sortie
            fichier_sortie = os.path.join(dossier_sortie, fichier)

            # Écrire le contenu converti dans le nouveau fichier
            with open(fichier_sortie, 'w') as file:
                file.write(contenu_minuscule)


def suppression_ponctuation(dossier):
    # Parcourir chaque fichier dans le dossier d'entré
    for fichier in os.listdir(dossier):
        fichier_entree = os.path.join(dossier, fichier)

        with open(fichier_entree, 'r') as file:
            contenu = file.read()
            new_contenu = ""

            for caractere in contenu :

                # Faire une sélection de tous les caractere devant être supprimé 
                if caractere == "." or caractere == "," or caractere == ";" or caractere == "!" or caractere == "?" or caractere == ":" :
                    new_contenu += ""

                # Faire une sélection de tous les caractere devant être remplacé par un espace 
                elif caractere == "\n" or caractere == "'" or caractere == "-":
                    new_contenu += " "

                # Les autres sont ajoutés au nouveau contenu
                else:
                    new_contenu += caractere

            # Écrire le contenu converti dans le nouveau fichier
            with open(fichier_entree, 'w') as file:
                file.write(new_contenu)

# convertir_majuscule_en_minuscules("speeches","cleaned")
# suppression_ponctuation("cleaned")

def tf_score(dossier): 
    tf = []

    for filename in os.listdir(dossier):
        fichier_entre = os.path.join(dossier, filename)
        with open(fichier_entre, "r") as file:

            # Lire le contenu du fichier
            content = file.read()

            # Créer le dictionnaire pour le nombre d'occurence de chaque mots 
            dico_occurrence = {} 

            # Séparer les mots de la chaîne de caractere en une liste 
            content = content.split() 

            # Parcourir les mots de la liste string 
            for word in content : 

                # Ajouter le mot au dictionnaire si il n'existe pas 
                if word not in dico_occurrence: 
                    dico_occurrence[word] = 0 

                # Incrementer 1 pour chaque mot 
                dico_occurrence[word] += 1 

            tf.append(dico_occurrence)

    return tf 

# print(tf_score("Voici un exemple de chaîne de caractere, elle sert à tester si la fonction marche bien par exemple le mot exemple apparait 3 fois :)"))


def idf_score(dossier):

    # Dictionnaire pour stocker le nombre de documents contenant chaque mot
    dico_frequence = {}
    total_documents = 0

    # Parcourir tous les fichiers dans le répertoire du corpus
    for fichier in os.listdir(dossier):
        fichier_entre = os.path.join(dossier, fichier)
        with open(fichier_entre, "r") as file:

            # Lire le contenu du fichier
            content = file.read()

            # Mettre à jour la fréquence des mots dans les documents
            words_in_document = set(content.split())
            for word in words_in_document:
                dico_frequence[word] = dico_frequence.get(word, 0) + 1
            total_documents += 1

    # Calculer le score IDF pour chaque mot
    idf_scores = {}
    for word, frequency in dico_frequence.items():
        idf_scores[word] = math.log10(total_documents / (frequency))  # Ajout de 1 pour éviter la division par zéro
    return idf_scores

# Exemple d'utilisation de la fonction

def association_tf_idf(tf_list,idf,dossier):
    matrix_tf_idf = []

    for ligne in range(len(dossier)):
        matrix_tf_idf.append([])
        for colonne in tf_list[ligne]:
            matrix_tf_idf[ligne].append(tf_list[ligne][colonne]*idf[colonne])
    return matrix_tf_idf

def mots_moins_importants(matrice_tf_idf, tf_list, dossier):
    for i in range(len(dossier)):
        tfidf_scores_document = matrice_tf_idf[i]
        liste_mots_moins_important = []

        # Trouver l'indice du score TF-IDF le plus élevé
        for tf_idf_indice in range(len(tfidf_scores_document)):
            if tfidf_scores_document[tf_idf_indice] == 0:
                liste_mots_moins_important.append(tf_list[tf_idf_indice].keys())
                # Afficher le résultat
                print("Document",i+1,": Le(s) mot(s) avec le score TF-IDF le moins élevé sont :",liste_mots_moins_important)

def mots_max(matrice_tf_idf, tf_list, dossier):
    for i in range(len(dossier)):
        tfidf_scores_document = matrice_tf_idf[i]

        # Trouver l'indice du score TF-IDF le plus élevé
        max_tfidf_index = tfidf_scores_document.index(max(tfidf_scores_document))
        print(max_tfidf_index)

        # Récupérer le mot correspondant à l'indice trouvé
        mots_document = list(tf_list[i].keys())
        mot_max_tfidf = mots_document[max_tfidf_index]

        # Afficher le résultat
        print("Document",i+1,": Le mot avec le score TF-IDF le plus élevé est :",mot_max_tfidf," avec un score de ",tfidf_scores_document[max_tfidf_index])

# Utiliser la fonction avec les données existantes
dossier = "cleaned"
tf_list = tf_score(dossier)
idf = idf_score(dossier)
matrice_tf_idf = association_tf_idf(tf_list,idf,dossier)
print(matrice_tf_idf)

# mots_moins_importants(matrice_tf_idf, tf_list, dossier)
# mot_moin_important(matrice_tf_idf, tf_list, dossier)
# print(presidents_name_display(name_association(recup_nom(list_of_files("speeches","txt")))))