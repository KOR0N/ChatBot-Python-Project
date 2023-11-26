from functions import *

dossier = "cleaned"
tf_list = tf_score(dossier)
idf = idf_score(dossier)
matrice_tf_idf = association_tf_idf(tf_list,idf,dossier)

if __name__ == "__main__":
    question = int(input("Voici différentes fonctions disponibles :\n   1) Afficher la liste des mots les moins importants dans le corpus de documents.\n   2) Afficher le(s) mot(s) ayant le score TD-IDF le plus élevé.\n   3) Indiquer le(s) mot(s) le(s) plus répété(s) par un président.\n   4) Indiquer le(s) nom(s) du (des) président(s) qui a (ont) parlé d'un mot à choisir et celui qui l’a répété le plus de fois.\n   5) Indiquer le premier président à parler d'un thème/sujet choisi.\n   6) Hormis les mots dits « non importants », quel(s) est(sont) le(s) mot(s) que tous les présidents ont évoqués.\n   7) QUITTER\nVeuillez choisir une de ces options (1/2/3/4/5/6/7) :"))
    while question < 1 or question > 7 :
        question = int(input("ERREUR. Veuillez choisir une option à nouveau : "))
    match question:
        case 1:
            print(score_tfidf_plus_faible(matrice_tf_idf, tf_list, dossier))
        case 2:
            mots_max(matrice_tf_idf, tf_list, dossier)
        case 3:
            choice = input("\nPour cette fonctionnalité vous devez rechercher un nom de président. Voulez vous voir la liste des présidents archivés ? (o/n) : ")
            if choice == "o" :
                presidents_name_display(recup_nom(files_names))
            elif choice != "o" and choice != "n":
                while  choice != "o" and choice != "n" :
                    choice = input("ERREUR. Pour cette fonctionnalité vous devez rechercher un nom de président. Voulez vous voir la liste des présidents archivés ? (o/n) : ")
            
            president_name = input("\nVeuillez entrer un nom de président : ")
            while president_name not in recup_nom(files_names):
                president_name = input("Nom non valide. Veuillez entrer un nom de président : ")
            mots_plus_répétés_par_président(president_name,tf_list)
        case 4:
            mot = input("\nVeuillez entrer un mot à rechercher : ")
            mots_dit_par_présidents(mot,tf_list)
        case 5:
            theme = input("\nVeuillez entrer un theme à rechercher : ")
            premier_president_dire_theme(theme,tf_list)
        case 6:
            print(mots_dit_par_tous_les_presidents(matrice_tf_idf,tf_list))

