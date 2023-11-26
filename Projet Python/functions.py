import os
import math


def list_of_files(directory, extension):
    files_names = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)
    return files_names


def recup_nom(files_names):
    presidents_name = []

    # Parcourir la liste des nominations des discours des présidents
    for filename in files_names:

        # Enlever les caracteres indesirables et répétés
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
            words_in_document = content.split()
            for words in words_in_document:
                if words in dico_frequence:
                    dico_frequence[words] += 1
                else:
                    dico_frequence[words] = 1
            total_documents+=1


    # Calculer le score IDF pour chaque mot
    idf_scores = {}
    for word, frequency in dico_frequence.items():
        idf_scores[word] = math.log((total_documents / frequency)+1)
    return idf_scores

# Exemple d'utilisation de la fonction

def association_tf_idf(tf_list,idf,dossier):
    matrice_tf_idf = []
    i = 0

    # Créer la matrice TF-IDF
    for words in idf:
        matrice_tf_idf.append([])
        for colonne in range(len(tf_list)):

            # Ajouter la valeur TF-IDF du mot dans la matrice si ce mot est présent selon le document
            if words in tf_list[colonne]:
                matrice_tf_idf[i].append(tf_list[colonne][words]*idf[words])
            # Ajouter la valeur 0 si ce n'est pas le cas
            else:
                matrice_tf_idf[i].append(0.0)
        i+=1
    return matrice_tf_idf

def score_tfidf_plus_faible(matrice_tf_idf, tf_list, dossier):
    for i in range(len(dossier)):
        tfidf_scores_document = matrice_tf_idf[i]
        liste_mots_moins_important = []

        # Trouver l'indice du score TF-IDF le plus élevé
        for tf_idf_indice in range(len(tfidf_scores_document)):
            if tfidf_scores_document[tf_idf_indice] == 0:
                liste_mots_moins_important.append(tf_list[tf_idf_indice].keys())
                # Afficher le résultat
    return liste_mots_moins_important
            

def mots_max(matrice_tf_idf, tf_list, dossier):
    for i in range(len(dossier)):
        tfidf_scores_document = matrice_tf_idf[i]

        # Trouver l'indice du score TF-IDF le plus élevé
        max_tfidf_index = tfidf_scores_document.index(max(tfidf_scores_document))

        # Récupérer le mot correspondant à l'indice trouvé
        mots_document = list(tf_list[i].keys())
        mot_max_tfidf = mots_document[max_tfidf_index]

        # Afficher le résultat
        print(f"Document {i+1} : Le mot avec le score TF-IDF le plus élevé est '{mot_max_tfidf}' avec un score de {tfidf_scores_document[max_tfidf_index]}")


def mots_plus_répétés_par_président(president_name,tf_list):

    #Récuperer les noms des présidents
    noms = recup_nom(files_names)
    list_mot_max = []

    #Trouver les mots les plus répétés par présidents
    for presidents_names in range(len(noms)) :
        if noms[presidents_names] == president_name :
            valeur_mots_max = 0
            mots_max = ""
            for words in tf_list[presidents_names]:
                if tf_list[presidents_names][words] > valeur_mots_max:
                    mots_max = words
                    valeur_mots_max = tf_list[presidents_names][words]
            list_mot_max.append(mots_max)
            for words in tf_list[presidents_names]:
                if tf_list[presidents_names][words] == valeur_mots_max and words != mots_max:
                    list_mot_max.append(mots_max)

    print("Le(s) mot(s) le(s) plus répété(s) par",president_name, "est (sont) :",list_mot_max)


def mots_dit_par_présidents(mot,tf_list):

    # Récuperer les noms des présidents
    noms = recup_nom(files_names)

    mot_dit_nombre_de_fois = {}

    # Ajouter 1 à chaque fois qu'un président à prononcer le mot recherché
    for speeches in range(len(tf_list)):
        for words in tf_list[speeches]:
            if words == mot :
                if noms[speeches] in mot_dit_nombre_de_fois:
                    mot_dit_nombre_de_fois[noms[speeches]] += 1
                else:
                    mot_dit_nombre_de_fois[noms[speeches]] = 1

    # Si au moins un président à prononcer ce mot
    if len(mot_dit_nombre_de_fois) > 0 :
        president_max = ""
        valeur_max = 0
        print(f"Les présidents ayant dit le mot '{mot}' sont :")

        # Trouver le président ayant dit le plus de fois le mot + Afficher chaque président ayant dit ce mot avec son nombre de fois
        for cle, valeur in mot_dit_nombre_de_fois.items():
            print(f"    - {cle}, l'ayant dit {valeur} fois.")
            if  valeur_max < valeur:
                valeur_max = valeur
                president_max = cle
        print(f"Donc le président ayant dit le plus de fois le mot '{mot}' est le président {president_max}")

    # Si aucun président à prononcé ce mot
    else:
        print("Aucun des présidents ont prononcés ce mot selon les dossiers.")


def premier_president_dire_theme(theme,tf_list):

    # Récuperer les noms des présidents
    noms = recup_nom(files_names)

    premier_president = ""

    # Chercher le nom du premier président ayant abordé le thème
    for speeches in range(len(tf_list)):
        for words in tf_list[speeches]:
            if words == theme:
                premier_president = noms[speeches]
                break

    # Afficher le nom du premier président ayant abordé le thème si il y en a un
    if premier_president:
        print(f"Le premier président à parler de {theme} est le président {premier_president}.")

    # Afficher qu'aucun président n'en a parlé si cecn'est pas le cas
    else:
        print("Aucun n'a évoqué ce sujet.")


""""""""""""""" Fonction non fonctionelle """""""""""""""""""""
def mots_dit_par_tous_les_presidents(matrice_tf_idf,tf_list):
    mot_present = []
    mot_est_dit_par_tous = True
    for words in range(len(matrice_tf_idf)):
        for speeches in range(len(matrice_tf_idf[words])):
            if matrice_tf_idf[words][speeches] != 0:
                mot_est_dit_par_tous = False
        if mot_est_dit_par_tous == True:
            mot_present.append(tf_list[speeches].keys())
            # for cle,valeur in idf.items():
            #     if valeur == matrice_tf_idf[words][speeches]:
            #         mot_present.append(cle)
        mot_est_dit_par_tous = True

    if len(mot_present) > 0:
        print(f"Le(s) mot(s) dit(s) par tous les présidents est (sont) : {mot_present}")
    else:
        print("Les présidents n'ont dis aucun mots important en commun.")

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# Utiliser les fonctions avec les données existantes
directory = "speeches"
files_names = list_of_files(directory, "txt")