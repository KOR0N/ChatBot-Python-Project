import os
import math

# Utiliser les fonctions avec les données existantes

enter_directory = "../speeche/speeches"
exit_directory = "../speeche/cleaned"

""""""""""""""""""""""""""""" Fonctions enfants """""""""""""""""""""""""""""""""""

def convertir_majuscule_en_minuscules(contenu):
    print(contenu)
    contenu_minuscule = ""
    # Convertir en minuscules 
    for caractere in contenu :
        # Vérifie si c'est une lettre majuscule
        if 65 <= ord(caractere) <= 90:
            contenu_minuscule += chr(ord(caractere)+32)
        else:
            contenu_minuscule += caractere
    return contenu_minuscule

def suppression_ponctuation(contenu):
    replace_to_nothing = "().,;!?:"
    replace_to_scape = "'-"
    new_contenu = ""

    for caractere in contenu :

        # Faire une sélection de tous les caractere devant être supprimé 
        if caractere == "\n" or caractere in replace_to_scape:
            new_contenu += " "

        # Faire une sélection de tous les caractere devant être remplacé par un espace 
        elif  caractere in replace_to_nothing or caractere == '"':
            new_contenu += ""

        # Les autres sont ajoutés au nouveau contenu
        else:
            new_contenu += caractere

    return new_contenu

def tf(content):
    tf_dic = {}
    for element in content:
        if element != "":
            if element not in tf_dic:
                tf_dic[element] = 1
            else:
                tf_dic[element] += 1
    return tf_dic

def list_of_files(directory, extension):
    files_names = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)
    return files_names


""""""""""""""""""""""""""""" Fonctions parents """""""""""""""""""""""""""""""""""


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


def cleaning_files(dossier):
    # Parcourir chaque fichier dans le dossier d'entré
    for fichier in os.listdir(dossier):
        fichier_entree = os.path.join(dossier, fichier)

        with open(fichier_entree, 'r') as file:
            contenu = file.read()
            contenu = convertir_majuscule_en_minuscules(contenu)
            contenu = suppression_ponctuation(contenu)
            
            # Écrire le contenu converti dans le nouveau fichier
            with open(fichier_entree, 'w') as file:
                file.write(contenu)


def idf_score(dossier):
    # Dictionnaire pour stocker le nombre de documents contenant chaque mot
    dico_frequence = {}
    total_documents = 0
    for fichier in os.listdir(dossier):
        fichier_entre = os.path.join(dossier, fichier)
        with open(fichier_entre,"r") as f:
            # Regrouper chaque mot dans une liste en supprimant les doublons
            content = set(f.read().split())
            for words in content:
                if words not in dico_frequence:
                    dico_frequence[words] = 0
                dico_frequence[words] += 1
        total_documents += 1

    # Calculer le score IDF pour chaque mot
    idf_scores = {}
    for word, frequency in dico_frequence.items():
        idf_scores[word] = math.log10(total_documents / frequency)
    return idf_scores


def association_tf_idf(tf_list,idf):
    matrice_tf_idf = []
    i = 0
    # Créer la matrice TF-IDF
    for words in idf:
        matrice_tf_idf.append([])
        for colonne in range(len(tf_list)):
            matrice_tf_idf[i].append(round(tf_list[colonne][words]*idf[words] if words in tf_list[colonne] else 0.0, 2))
        i+=1
    return matrice_tf_idf


def score_tfidf_plus_faible(matrice_tf_idf,idf):
    liste_mots_moins_important = []

    for words in range(len(matrice_tf_idf)):
        IDF = list(idf.keys())
        score_tfidf = 0
        for dossiers in range(len(matrice_tf_idf[words])):
            score_tfidf += matrice_tf_idf[words][dossiers]
        if score_tfidf == 0.0 :
            liste_mots_moins_important.append(IDF[words])

    return liste_mots_moins_important


def mots_max(matrice_tf_idf, idf):
    score_max = 0
    cle_score_max = ""
    liste_mots_max = []

    # Rechercher le score TF-IDF le plus élevé dans la matrice 
    for words in range(len(matrice_tf_idf)):
        IDF = list(idf.keys())
        score_tfidf = 0
        for dossier in range(len(matrice_tf_idf[words])):

            # Calculer le score
            score_tfidf += matrice_tf_idf[words][dossier]

        # Comparer le score avec le score maximum déjà enregistré
        if score_tfidf > score_max :
            score_max = score_tfidf
            cle_score_max = IDF[words]

    liste_mots_max.append(cle_score_max)

    # Faire un deuxième tour si il n'y a pas des mots ayant le même score
    for words in range(len(matrice_tf_idf)):
        IDF = list(idf.keys())
        score_tfidf = 0
        for dossier in range(len(matrice_tf_idf[words])):
            score_tfidf += matrice_tf_idf[words][dossier]

        # Si il a le même score et que ce n'est pas le même mot que précedemment, on l'ajoute
        if score_tfidf == score_max and cle_score_max != IDF[words]:
            liste_mots_max.append(cle_score_max)

    # Afficher le résultat
    print("Mot(s) avec le score TF-IDF le plus élevé :")
    for mot in liste_mots_max:
        print(mot)


def mots_plus_répétés_par_président(president_name,tf_list,files_names):

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


def mots_dit_par_présidents(mot,tf_list,files_names):

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
        for cle, valeur in mot_dit_nombre_de_fois.items():
            if valeur_max == valeur and cle not in president_max:
                president_max += ", " + cle
        print(f"Donc le(s) président(s) ayant dit le plus de fois le mot '{mot}' est (sont) le(s) président(s) {president_max}.")

    # Si aucun président à prononcé ce mot
    else:
        print("Aucun des présidents ont prononcés ce mot selon les dossiers.")


def premier_president_dire_theme(theme,tf_list,files_names):

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


def mots_dit_par_tous_les_presidents(idf,tf_list,non_important):
    """"""
    mot_present = []
    for word in idf:
        present = True
        for doc in tf_list :
            if word not in doc:
                present = False
        if present == True and word not in non_important:
            mot_present.append(word)
    # Verifier si au moins un mot a ete dit par
    if len(mot_present) > 0:
        print(f"Le(s) mot(s) dit(s) par tous les présidents est (sont) : {mot_present}")
    else:
        print("Les présidents n'ont dis aucun mots important en commun.")

""""""""""""""""""""""""""""""""" Partie 2 """""""""""""""""""""""""""""""""""""""

def tokenisation(contenu):
    """ Permet de convertir un contenu en parametre en liste de mots mnuscules et sans les ponctuations """
    contenu = convertir_majuscule_en_minuscules(contenu)
    contenu = suppression_ponctuation(contenu)
    contenu = contenu.split(" ")
    return contenu

def presence_mot(contenu,idf):
    """ AFficher les mots présents et absents dans le dictionnaire IDF """
    dic = {}
    for mots in contenu:
        if mots != "":
            dic[mots] = False

            if mots in idf:
                dic[mots] = True
    return dic

def inverse_matrice(matrice):
    """ Inverser la matrice donné en parametre """
    m = []
    ligne = matrice[0]
    for j in range(len(ligne)):
        m.append([])
    i = 0

    # Ajouter les valeurs des lignes dans les colonnes du même rang
    for ligne in matrice:
        for j in range(len(ligne)):
            m[j].append(matrice[i][j])
        i += 1
    return m

def calculate_tfidf(tf_list,idf,dossier):
    """Calculer et retourner la matrice TF-IDF en fonction du TF de la question et de l'IDF de tous les mots dans le corpus"""
    matrice_tf_idf = []
    i = 0
    # Créer la matrice TF-IDF
    for i in range(len(dossier)):
        matrice_tf_idf.append([])
        for words in idf:
            # Ajouter la valeur TF-IDF du mot de la question dans la matrice si ce mot est présent selon le document sinon 0
            matrice_tf_idf[i].append(round(tf_list[words]*idf[words] if words in tf_list else 0.0, 2))
        i+=1
    return matrice_tf_idf

def scalaire(A,B):
    """Fonction qui prend en valeur A et B deux vecteur permet de calculer et retourner A . B = somme de 1 à m avec i=1 pour Ai * Bi"""

    # Vérifier si les deux vecteurs ont la même dimension
    if len(A) != len(B):
        return("Erreur ! A et B sont de dimension différentes. Merci de réessayer en entrant des vecteurs de même dimension")

    # Calculer la somme des produits des éléments correspondants des deux vecteurs 
    somme_produits = 0
    for i in range(len(A)): # On peut prendre A puisqu'ils sont de même dimension 
        somme_produits += A[i] * B[i]

    return somme_produits # On se retrouve donc bien avec tout ce qu'on voulait notre expression du produit scalaire

def norme(A):
    """Fonction qui prend en paramètre un vecteur A et calcule et retourne la racine carrée de la somme des carrés de ses composantes"""
    # Calculer la somme des carrés des éléments du vecteur
    somme_carres = 0
    for element in A:
        somme_carres += element**2

    # Retourner la racine carrée de la somme des carrés
    return math.sqrt(somme_carres)

def similarite(A,B):
    """Prend en parametre deux matrice pour calculer leurs vetceurs et retourner le fichier avec la plus grande similarite"""
    final = []
    # Calculer de la similarite pour chaque fichiers
    for i in range(len(A)):
        scal=scalaire(A[i],B[i])
        norme_a=norme(A[i])
        norme_b=norme(B[i])
        if norme_a==0 or norme_b==0:
            final.append(0)
        else:
            final.append((scal)/(norme_a*norme_b))
    
    # Calculer le fichier avec la plus grande similarite
    if max(final) == 0:
        return("Aucun document correspond à cette question")
    for i in range(len(final)):
        if final[i] == max(final):
            return i
        

