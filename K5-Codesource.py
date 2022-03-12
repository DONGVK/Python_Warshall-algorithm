"""
@Author @105115 DONG
"""
import math

def del_linebreak(lines):
    i=0
    while(i < len(lines)):
        if( lines[i].find('\n') != -1):
            lines[i] = lines[i].replace('\n', '')#Suppression du retour chariot
        i+=1
    return lines

def adjacency_matrix(graph):
    ng = graph.copy()
    tab=[]
    for i in ng[2:]:
        tmp = i.split(' ')#création d'un tableau à partir de la ligne du fichier
        tab += [tmp]
    nt = [[0]*int(ng[0]) for _ in range(int(ng[0]))]#création d'un tableau de [m colonnes] ... n lignes
    for i in tab:
        nt[int(i[0])][int(i[1])]=  1 if (int(i[2]) != 0) else 0
    return nt

def default_matrix(graph):
    ng = graph.copy()
    tab=[]
    for i in ng[2:]:
        tmp = i.split(' ')#création d'un tableau à partir de la ligne du fichier
        tab += [tmp]
    nt = [[math.inf]*int(ng[0]) for _ in range(int(ng[0]))]#création d'un tableau de [m colonnes] ... n lignes
    for i in tab:
        nt[int(i[0])][int(i[1])]=int(i[2])
    for i in range(len(nt)):
        if(nt[i][i] == math.inf):#si dans la diagonale il y a une valeur infini, on le remplace par 0
            nt[i][i] = 0
    return nt

def print_matrix(m):
    number = "    "
    for i in range(len(m)):
        number += "{0:^4}".format(str(i)) + "| " if i < len(m) - 1 else "{0:^4}".format(str(i))# {0:¨4} permet de centrer la chaine limité à 4 caractères
    print(number)#print la légende au desus
    print('---'+'------'*(len(m)))#print les traits
    for i in range(len(m)):
        print(i , '|' , '| '.join("{0:^4}".format(str(e)) for e in m[i]) )
        print('---'+'------'*(len(m)))


def print_matrixad(m):
    number = []#tableau pour la légende
    for i in range(len(m)):
        number.append(i)#ajout des nombre dans le tableau
    print('   ', ' |  '.join(map(str, number)) )#print les valeurs de dessus, join permet de créer une chaine de caractère séparer de | et map et faire un array de string
    print('---'+'-----'*(len(m)))#print les traits
    for i in range(len(m)):
        print(number[i] , '|' , ' |  '.join(map(str, m[i])) )
        print('-----'*len(m)+'---')

def floyd_warshall(m):
    new_array = m.copy()
    pred = [[0]*len(m) for _ in range(len(m))]
    for z in range(len(m)):#remplissage de la matrice P tel que pred[i][j]=i
        for y in range(len(m)):
            pred[z][y]=z

    print("\nInitialisation:")
    print("L :\n")
    print_matrix(new_array)
    print("P :\n")
    print_matrix(pred)

    for k in range(len(m)):#sommet
        txt = "Iteration n°"+str(k+1)
        print("\n"+txt)
        for i in range(len(m)):#sommet de départ
            for j in range(len(m)):#sommet de destination au sommet de départ
                if( (new_array[i][k] + new_array[k][j]) < new_array[i][j]):
                    pred[i][j] = pred[k][j]
                    new_array[i][j] = min(new_array[i][j], new_array[i][k] + new_array[k][j])
                if( i == j and new_array[i][j] < 0):
                    print("L :\n")
                    print_matrix(new_array)
                    print(" ")
                    print("P :\n")
                    print_matrix(pred)
                    print("Détection de circuit absorbant")
                    return [], []

        print("L :\n")
        print_matrix(new_array)
        print(" ")
        print("P :\n")
        print_matrix(pred)

    print("\nRésultat final : \n ")
    print("L :\n")
    print_matrix(new_array)
    print(" ")
    print("P :\n")
    print_matrix(pred)

    return new_array, pred

def path_short(i, j, pred, mfw):#Fonction qui donne les plus court chemins entre deux sommets donnés
    i,j = int(i), int(j)#convertire les str en int
    if(mfw[i][j] == math.inf):
        return "Désolé, il n'y a pas de chemin possible"
    tab = []#tableau de valeur pour le chemin
    tab.append(j)#on ajoute le sommet de fin
    tab.append(pred[i][j])
    while(tab[len(tab)-1] != i):
        tab.append(pred[i][tab[len(tab)-1]])#on ajoute le predeceseur de i pour le chemin
    print("Le chemin de" , i , "à", j, "est de longueur :", mfw[i][j])
    print("Le chemin le plus court est : ")
    return tab[::-1]




#-------------------------- MAIN(Ne pas oublier de changer le chemin d'accès aux fichiers .txt (Ligne 130)--------------------------------
print("Created by DONG Jean - PONNOU Wilfried - NGUYEN Duc Hoang")
ask = input("Voulez-vous commencer ? Oui | Non \n")
while ((ask.lower() != "oui") and (ask.lower() != "non")):
    ask = input("Voulez-vous commencer ? Oui | Non \n")

start = True if (ask.lower() == "oui") else False
while(start):
    choose_f = input("Entrez le nom du fichier:\n")#Lecture du fichier .txt du graphe correspondant à l'input entrée par l'utilisateur
    file = open("K5-"+choose_f+".txt", "r")#Ne pas oublier de mettre ici le chemin du dossier contenant les fichiers .txt
    lines = file.readlines()
    file.close()
    lines = del_linebreak(lines)

    matrixad = adjacency_matrix(lines)
    matrix = default_matrix(lines)

    print("Matrice d'adjacence\n")
    print_matrixad(matrixad)
    print("Matrice de valeurs\n")
    print_matrix(matrix)

    print("\nExécution de l'algorithme de Floyd-Warshall\n")
    ma,pred = floyd_warshall(matrix)
    if(ma != [] and pred != []):
        chemin = input("Chemin ? Oui | Non\n")
        while((chemin.lower() != "oui") and (chemin.lower() != "non")):#Boucle de demande/affichage de chemins
            chemin = input("Chemin ? O/Oui | N/Non")
        while(chemin.lower() == "oui"):
            i = int(input("Départ ?\n"))
            j = int(input("Arrivée ?\n"))
            while(i > len(matrix) - 1):
                i = int(input("Départ ? (Veuillez sélectionner un sommet valide)\n"))
            while(j > len(matrix) - 1):
                j = int(input("Arrivée ?(Veuillez sélectionner un sommet valide)\n"))
            print(path_short(i, j, pred, ma))
            chemin = input("Chemin ? Oui | Non\n")
            while((chemin.lower() != "oui") and (chemin.lower() != "non")):
                chemin = input("Chemin ? Oui | Non\n")


    ask = input("Un autre graphe à tester ? Oui | Non \n")
    while ((ask.lower() != "oui") and (ask.lower() != "non")):#Boucle d'affichage de graphes
        ask = input("Un autre graphe à tester ? Oui | Non \n")
    start = True if (ask.lower() == "oui") else False
print("Merci d'avoir testé le programme, à bientôt.")
