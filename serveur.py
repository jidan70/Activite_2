# -*- coding:Utf-8 -*-

"""Module du serveur gérant la connexion des Joueurs clients , à lancer en premier"""

import os, socket, re, time, select
from labyrinthe import *
from carte import *


HOTE = ""
PORT = 15500


#Création du socket serveur
serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    serveur.bind((HOTE,PORT))        
except:
    print("Le serveur ne peut utiliser l'adresse, rééssayez... \n \
si le problème persiste changez le port")

print("Le serveur est en service")

#Demande au serveur de choisir la carte
a=action_depart()

try:
    a=a.replace("x", " ")
except:
    pass

les_joueurs = {}
symb_joueur = {}
i = 1
#On va permettre au serveur d'attendre 15secondes pour chaque
#Nouvelle connexion avant de lancer la partie
serveur.settimeout(15)

while i <= 5:
    serveur.listen(5)
    #Si l'attente dépasse 15 seconde la boucle est arrété et le jeu commence
    try:
        connexion, adresse = serveur.accept()
    except socket.timeout:
        break
    les_joueurs[i] = connexion
    print("joueur",i," est entré dans la partie")
    connexion.send("choisissez votre symbole".encode("Utf8"))
    symb = connexion.recv(10).decode("Utf8")
    symb_joueur[i] = symb
    #On ajoute le symbole du joueur sur la carte
    a = ajouter_symbole_sur_carte(symb, a)
    new_message = "joueur" + str(i) + " est entré \n La partie commence dans 15 secondes\
 si aucun nouveau joueur entre dans la partie(inutile d'appuyer sur C )"
    for key in les_joueurs:
        les_joueurs[key].send(a.encode("Utf8"))
        les_joueurs[key].send(new_message.encode("Utf8"))
    connexion.send("attente des joueurs".encode("Utf8"))
    i += 1

for key in les_joueurs:
    les_joueurs[key].send("La partie commence".encode("Utf8"))
liste_joueur = []
for key in les_joueurs:
    liste_joueur.append(les_joueurs[key])

print("chargement serveur")
time.sleep(2)

nb_joueur = len(les_joueurs)
i = 1

#Le jeu commence ici
#i représente le tour du joueur i et varie sans dépasser le nombre de joueur
#La variable i s'incrémentera de 1 à chaque tour puis sera réinitialisé
#À 1 lorsqu'il atteindra le nombre de joueur nb_joueur
#Dans cette boucle la variable a represent la carte et son évolution
while i <= nb_joueur:
    les_joueurs[i].send("Votre tour".encode("Utf8"))
    msg_gen = "Tour du joueur" + str(i)
    #On précise à chaque joueur le joueur qui est en train de joueur 
    for joueur in liste_joueur:
        if joueur != les_joueurs[i]:
            joueur.send(msg_gen.encode("Utf8"))
    #Le serveur recoit la commande du joueur
    commande = les_joueurs[i].recv(15).decode("Utf8")
    #On capture a à son état au début de la boucle c.a.d du tour
    b = a
    #c1 représente la commande direction
    c1 = commande[0]
    #On va vérifié si le joueur a demandé de murer ou percer
    #c2 représente l'action murer ou percer du joueur
    try:
        c2 = commande[1]
    except:
        pass
    else:
        a = dep_mur(a, c1, c2, symb_joueur[i])
        #Si l'action est impossible la fonction dep_mur renvoit a inchangé
        #On relance le tour en cas d'action impossible
        if b == a:
            continue
        #Sinon l'action est considéré et on passe au tour suivant
        i += 1
        message = "joueur " + str(i) + " a joué \n" + a
        for key in les_joueurs:
            les_joueurs[key].send(message.encode("Utf8"))
        del c2
        time.sleep(1)
        if i > nb_joueur:
            i = 1
        continue

    #Dans le cas ou le joueur a choisi de se déplacer
    #On appelle la fonction deplacer
    a = deplacer(a, c1, 1, symb_joueur[i])

    #Si déplacement incorrect on relance le tour
    if b == a:
        les_joueurs[i].send("déplacement incorrect ,rejouez".encode("Utf8"))
        time.sleep(1)
        continue

    #Lorsque le joueur i a gagné
    if a == "vous gagnez":
        les_joueurs[i].send(a.encode("Utf8"))
        message = "joueur " + str(i) + " a gagné"
        for joueur in liste_joueur:
            if joueur != les_joueurs[i]:
                joueur.send(message.encode("Utf8"))
                joueur.close()
        time.sleep(1)
        break
        
    message = "joueur " + str(i) + " a joué \n" + a
    for key in les_joueurs:
        les_joueurs[key].send(message.encode("Utf8"))
    time.sleep(1.5)
    i += 1
    #On réinitialise i si i est supérieur au nombre de joueur
    if i > nb_joueur:
        i = 1

try:
    os.sys("pause")
except:
    print("le jeu est términé")
    
