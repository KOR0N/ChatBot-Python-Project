#########################################################################################################
##################################### CHATBOT PROJET PYTHON #############################################
#########################################################################################################
# Alexandre LE GALLIARD
# Alexandre DAUVEL

# Ce fichier comporte le menu du ChatBot en utilisant les fonctions du fichier functions.py

#-------------------------------------------------------------------------------------------------------#


from functions import *

dossier = "./speeche/cleaned"
dossier_non_traite = "./speeche/speeches"

files_names = list_of_files(dossier_non_traite, "txt")

tf_list = []
for filename in os.listdir(dossier):
    fichier_entre = os.path.join(dossier, filename)
    with open(fichier_entre, "r") as file:
        content = file.read()
        content = content.split() 
        tf_list.append(tf(content))

idf = idf_score(dossier)
matrice_tf_idf = association_tf_idf(tf_list,idf)
non_important = score_tfidf_plus_faible(matrice_tf_idf, idf)

if __name__ == "__main__":
    question = int(input("Parmi ces fonctionnalités :\n    1) Accéder aux fonctionnalités proposées par notre application.\n    2) Accéder au ChatBot.\nVeuillez en choisir une option (1/2) : "))
    while question != 1 and question != 2 :
        question = int(input("Parmi ces fonctionnalités :\n    1) Accéder aux fonctionnalités proposées par notre application.\n    2) Accéder au ChatBot.\nVeuillez en choisir une option (1/2) : "))

    if question == 1 :
        question = int(input("\nVoici différentes fonctions disponibles :\n   1) Afficher la liste des mots les moins importants dans le corpus de documents.\n   2) Afficher le(s) mot(s) ayant le score TD-IDF le plus élevé.\n   3) Indiquer le(s) mot(s) le(s) plus répété(s) par un président.\n   4) Indiquer le(s) nom(s) du (des) président(s) qui a (ont) parlé d'un mot à choisir et celui qui l’a répété le plus de fois.\n   5) Indiquer le premier président à parler d'un thème/sujet choisi.\n   6) Hormis les mots dits « non importants », quel(s) est(sont) le(s) mot(s) que tous les présidents ont évoqués.\n   7) QUITTER\nVeuillez choisir une de ces options (1/2/3/4/5/6/7) : "))
        while question < 1 or question > 7 :
            question = int(input("ERREUR. Veuillez choisir une option à nouveau : "))
        match question:
            case 1:
                print(non_important)
            case 2:
                mots_max(matrice_tf_idf, idf)
            case 3:
                choice = input("\nPour cette fonctionnalité vous devez rechercher un nom de président. Voulez vous voir la liste des présidents archivés ? (o/n) : ")
                if choice != "o" and choice != "n":
                    while  choice != "o" and choice != "n" :
                        choice = input("ERREUR. Pour cette fonctionnalité vous devez rechercher un nom de président. Voulez vous voir la liste des présidents archivés ? (o/n) : ")
                
                if choice == "o" :
                    presidents_name_display(recup_nom(files_names))
                
                president_name = input("\nVeuillez entrer un nom de président : ")
                while president_name not in recup_nom(files_names):
                    president_name = input("Nom non valide. Veuillez entrer un nom de président : ")
                mots_plus_répétés_par_président(president_name,tf_list,files_names)
            case 4:
                mot = input("\nVeuillez entrer un mot à rechercher : ")
                mots_dit_par_présidents(mot,tf_list,files_names)
            case 5:
                theme = input("\nVeuillez entrer un theme à rechercher : ")
                premier_president_dire_theme(theme,tf_list,files_names)
            case 6:
                mots_dit_par_tous_les_presidents(idf,tf_list,non_important)

    else:
        question = tokenisation(input("\nBienvenue sur notre ChatBot\nVeuillez entrez une question : "))
        matrice_tf_idf = inverse_matrice(matrice_tf_idf)
        print(generation_reponse(question,idf,matrice_tf_idf,dossier_non_traite))
