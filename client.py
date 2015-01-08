# -*- coding:Utf-8 -*-

"""Module du client, à lancer pour se connecteur au serveur de
Roboc une fois que celui-ci est lancé"""

import os, socket, re
from threading import Thread
from labyrinthe import *
from carte import *

HOTE = "localhost"
PORT = 15500

class Recept(Thread):
    """classe héritant de Thread et qui permet à la reception des réponses
    du serveur cette classe gére aussi l'envoi des commandes au serveur """

    def __init__(self, connexion):
        Thread.__init__(self)
        self.connex = connexion
    def run(self):
        #le client va recevoir des réponses de manière constante
        while True:
            msg_jeu = self.connex.recv(1500).decode("Utf8")

            #Quand c'est le tour du joueur celui-ci recevra les commandes à faire
            if msg_jeu == "Votre tour" or msg_jeu == "déplacement incorrect , rejouez":
                print(msg_jeu)
                commande = ""
                #Tant que la commande entrée ne correspond pas aux commandes attendu
                #Le client devra ressaisir les commandes
                while not re.search(r"^[NSOEesno]{1}[MPmp]?$", commande) or commande == "":
                    commande = input("Entrez la commande ( <N>ord | <S>ud | <E>st | <O>uest )\
 \n fonctionnel : | <M>urer | <P>ercer \n EXEMPLE(murer est : em")
                self.connex.send(commande.encode("Utf8"))

            #Lorsque le serveur demande le symbole pour joueur
            if msg_jeu == "choisissez votre symbole":
                symb = choix_symbole()
                self.connex.send(symb.encode("Utf8"))

            if msg_jeu == "vous gagnez":
                print(msg_jeu)
                self.connex.close()
                break
                

            #sinon tout autre message est affiché tout simplement
            else:
                print(msg_jeu)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("accés au serveur Roboc")

client.connect((HOTE,PORT))
print("Connexion avec succés")

#On aurait pu  utiliser tout simplement une fonction reprenant le run du thread défini plus haut
th_r = Recept(client)
th_r.start()


os.system("pause")       


