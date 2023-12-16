import copy
import colored
import time


def lireTxt(chemin):
    file  = open(chemin,"r",encoding="utf8")
    BUT = eval(file.readline())
    rumba = eval(file.readline())
    TAILLE_TIGE = eval(file.readline())
    NB_TIGES = len(rumba)
    file.close()
    return (BUT, rumba, TAILLE_TIGE, NB_TIGES)

def push(tige_rumba, cube):
    tige_rumba.append(cube)
    return tige_rumba

def move(ru, a, b):
    r = copy.deepcopy(ru)
    if (len(r[b])<TAILLE_TIGE):
        cube = r[a].pop()
        r[b] = push(r[b], cube)
    else:
        print("Mouvement impossible : tige",b,"est déjà remplie.")
    return r

def afficher(rumba):
    print("\n")
    for i in range(TAILLE_TIGE-1, -1,-1):
        for j in range(len(rumba)):
            if (i>=len(rumba[j])):
                print(f'{colored.fg(15)}'"  │  ", end="")
            else:
                cube = rumba[j][i]
                print(f'{colored.fg((cube-1)//TAILLE_TIGE)} {cube:2d}', end="  ")
                
        print(f'{colored.fg(15)}'"")
    for i in range(len(rumba)):
        print("══╧══",end='')
    print()
    for i in range(len(rumba)):
        print(" ",i,end='  ')
    print()

def testEtatBut(etat):
    return etat["liste"] == BUT

def trouverDestinations(rumba, pi):
    destinations = []
    if len(rumba[pi])>0:
        for i in range(NB_TIGES):
            if (i!=pi and len(rumba[i])<TAILLE_TIGE):
                destinations.append(i)
    return destinations

def filsEtat(etat):
    fils = []
    r = copy.deepcopy(etat["liste"])
    indice_fils = 0
    for i in range(NB_TIGES):
        destinations = trouverDestinations(r,i)
        for j in range(len(destinations)):
            t = copy.deepcopy(etat["plan"])
            t.append( (i, destinations[j]) ) 
            fils.append({"liste":[], "profondeur":etat["profondeur"]+1,"plan": t })
            nouvelEtat = move(r, i, destinations[j])
            fils[indice_fils]["liste"] = nouvelEtat
            indice_fils += 1
    return fils

def ajouterTete(e, liste):
    liste.append(0)
    for i in range(len(liste)-1, 0, -1):
        liste[i] = liste[i-1]
    liste[0] = e
    return liste

def estDedans(e, vus):
    for i in range(len(vus)):
        if vus[i]["liste"] == e["liste"]:
            return True
    return False


# ALGORITHME IDA* 

def IDA_etoile(depart, h_choisie):
    enAttente = [{"liste":depart, "profondeur":0, "plan":[]}]
    prochain = enAttente[0]
    vus = []
    trouve = False
    compteur_crees = 0
    compteur_developpes = 0
    nb_developpes = []
    nb_crees = []
    iteration = 1
    seuil = f(prochain, h_choisie)
    seuils_prec = []
    print("\n\n\nRecherche en cours...\n\n\n")
    while len(enAttente)>0:
        prochain = enAttente.pop(0)
        if (not(estDedans(prochain, vus))):
            vus.append(prochain)
            if testEtatBut(prochain):
                trouve = True
                nb_developpes.append(compteur_developpes)
                nb_crees.append(compteur_crees)
                return (True, prochain, nb_developpes, nb_crees, f(prochain, h_choisie), iteration)
            else:
                fils = filsEtat(prochain)
                for e in fils:
                    if not(estDedans(e, vus)):
                        if f(e, h_choisie)<=seuil:
                            enAttente = ajouterTete(e, enAttente)
                        else:
                            seuils_prec.append(f(e, h_choisie))
                    compteur_crees += 1
                compteur_developpes += 1
        if len(enAttente)==0:
            nb_developpes.append(compteur_developpes)
            nb_crees.append(compteur_crees)
            compteur_crees = 0
            compteur_developpes = 0
            if len(seuils_prec) == 0:
                break
            iteration += 1
            seuil = min(seuils_prec)
            seuils_prec = []
            enAttente = [{"liste":depart, "profondeur":0, "plan":[]}]
            prochain = enAttente[0]
            vus = []

    return (trouve, depart, compteur_developpes, compteur_crees)

#******************* heuristiques ************************** 

def trouverPique(e, cube):
    for i in range(NB_TIGES):
        for j in range(len(e[i])):
            if e[i][j] == cube:
                return i
    return -1

# heuristique (amélioration)
def hAmeliore(e):
    distance = 0
    for i in range(NB_TIGES):
        for j in range(len(e["liste"][i])):
            if j<len(BUT[i]) and e["liste"][i][j] == BUT[i][j]:
                distance += 0
            else:
                distance += abs(i-trouverPique(BUT, e["liste"][i][j])) + abs((len(e["liste"][i])-1)-j)
    return distance

def hNbMalMis(e):
    distance = 0
    for i in range(NB_TIGES):
        for j in range(len(e["liste"][i])):
            if j>=len(BUT[i]) or e["liste"][i][j] != BUT[i][j]:
                distance += 1
    return distance

def h(e, h_utilisee):
    if h_utilisee==1:
        return hNbMalMis(e)
    else:
        return hAmeliore(e)

def f(e, h_choisie):
    return e["profondeur"] + h(e, h_choisie)



# Programme principal
all_bool = False
print("Bonjour, bienvenue dans la Rumba des chiffres !")
print("Nous vous proposons un algorithme (IDA*) permettant de résoudre n'importe quelle partie de Rumba des chiffres (tant que celle-ci est réalisable).")

fichier = open("solution.txt", "w")
fichier.truncate()

nom_fichier = input("Avec quel fichier voulez vous jouer ? (par défaut: rumba.txt / 'all' pour tous les faire) :")
if nom_fichier == "":
    fichiers = ["rumba.txt"]
elif nom_fichier == "all":
    all_bool = True
    fichiers = ["rumba_1_1.txt", "rumba_1_2.txt", "rumba_2_3.txt", "rumba_2_4.txt", "rumba_2_5.txt", "rumba_2_6.txt"]
else:
    fichiers = [nom_fichier]

h_choisie = eval(input("Souhaitez-vous utiliser l'heuristique 'nombreMalMis'[1] ou l'heuristique améliorée (non-minorante) [2] :"))    

for i in range(len(fichiers)):
    (BUT, rumba, TAILLE_TIGE, NB_TIGES) = lireTxt(fichiers[i])

    while (len(BUT)!=len(rumba)):
        input("Attention, la disposition que vous proposez n'est pas autorisée, veuillez modifier le fichier ",fichiers[i]," (la première ligne correspond à l'état but, la deuxième à l'état initial et la troisième au nombre de blocs maximum par tige), enregistrer, puis appuyer sur entree")
        (BUT, rumba, TAILLE_TIGE, NB_TIGES) = lireTxt(fichiers[i])

    print("\nSouhaitez-vous bien atteindre ce but :")
    afficher(BUT)
    print("À partir de cette disposition :")
    afficher(rumba)
    if (not(all_bool)):
        rep = input("oui [o]/ non [n] : ")
        while rep != 'o' and rep != 'n':
            rep = input("Pardon, je n'ai pas compris votre réponse, oui [o]/ non [n] : ")
        while (rep=='n'):
            input("Modifiez le fichier rumba.txt (la première ligne correspond à l'état but, la deuxième à l'état initial et la troisième au nombre de blocs maximum par tige),\nenregistrez, puis appuyez sur entrée")
            (BUT, rumba, TAILLE_TIGE, NB_TIGES) = lireTxt(fichiers[i])
            while (len(BUT)!=len(rumba)):
                input("Attention, la disposition que vous proposez n'est pas autorisée, veuillez modifier le fichier",fichiers[i],", enregistrer, puis appuyer sur entree")
                (BUT, rumba, TAILLE_TIGE, NB_TIGES) = lireTxt(fichiers[i])
            print("souhaitez vous bien atteindre ce but :")
            afficher(BUT)
            print("À partir de cette disposition :")
            afficher(rumba)
            rep = input("oui [o]/ non [n] : ")
            while rep != 'o' and rep != 'n':
                rep = input("pardon, je n'ai pas compris votre réponse, oui [o]/ non [n] : ")
    print("parfait, nous pouvons commencer :")      

    # lancement de l'algorithme
    start = time.time()
    resultat = IDA_etoile(rumba, h_choisie)
    end = time.time()

    # résultats

    if resultat[0]:
        print("\n\n\nLe but a été atteint :")
        afficher(resultat[1]["liste"])
        print("\nProfondeur du noeud :", resultat[1]["profondeur"], "\nPlan solution :",resultat[1]["plan"],"\nnb de noeuds créés par iteration:", resultat[3],"\nnb de noeuds développés par iteration:", resultat[2], "\nnb d'iterations :", resultat[5], "\ntemps d'execution :", round(end-start, 4), "sec")
        fichier.write(fichiers[i])
        fichier.write("\nEtat initial :\t\t\t\t")
        fichier.write(str(rumba))
        fichier.write("\nEtat but :\t\t\t\t")
        fichier.write(str(BUT))
        fichier.write("\nProfondeur du noeud :\t\t\t")
        fichier.write(str(resultat[1]["profondeur"]))
        fichier.write("\nPlan solution :\t\t\t\t")
        fichier.write(str(resultat[1]["plan"]))
        fichier.write("\nnb de noeuds créés par itération :\t")
        fichier.write(str(resultat[3]))
        fichier.write("\nnb de noeuds développés par itération :\t")
        fichier.write(str(resultat[2]))
        fichier.write("\nnb d'iterations :\t\t\t")
        fichier.write(str(resultat[5]))
        fichier.write("\ntemps d'execution :\t\t\t")
        fichier.write(str(round(end-start, 4)))
        fichier.write(" sec\n\n\n")
        print("(Les résultats ont été inscrit dans le fichier 'solution.txt')")
    else :
        print("Le but n'est pas atteignable...")

fichier.close()