"""Module contenant toute les fonction permettant de gérer les cartes(création,
   affichage, placer les joueurs, choix des symbole) et les commandes"""

import os
import sys

import pickle
import re, random
from carte import *

l_s = ["X", "G", "g", "E", "K"]

def action_depart():
    """Fonction permmetant de chosir entre une nouvelle partie et une partie
    existante"""
    global a
    partie_existante=input("tapez J pour joueur")
    if partie_existante == "J" or partie_existante == "j" :
        choix_carte()
    else:
            action_depart()
    return a


def choix_carte():
    """Permet le choix entre les cartes du jeu pour une nouvelle partie """
    global a
    choix=0
    fichier_existe=False

    while fichier_existe is False:
        choix=input("choisir carte : 1-facile 2-moyen ")
        if choix == '1':
            choix = crt1
            fichier_existe = True            
        if choix == '2':
            choix = crt2
            fichier_existe = True
    with open(choix,"rb") as fichlab:
        depickler1=pickle.Unpickler(fichlab)
        a= depickler1.load()


def choix_symbole():
    liste_symbole = ["X", "G", "g", "E", "K"]
    symbole_choisi = ""
    re_symb = r"^[XKGgE]{1}$"
    while not re.search(re_symb, symbole_choisi) or symbole_choisi == "":
        symbole_choisi = input("choisissez votre symbole pour jouer {}".format(liste_symbole))
    return symbole_choisi

def ajouter_symbole_sur_carte(symb,a):
    """Ajoute le symbole du joueur sur la carte"""
    place = random.randint(0,len(a))
    while a[place] != " ":
        place = random.randint(0,len(a))
    a = a[0:place] + symb + a[place+1:]
    return a

def dep_mur(carte, c1, c2, symb):
    """Fonction permettant la prise en charge des commande murer et percer"""
    global l_s
    #défintion des objets non considéré par l'action murer ou percer
    m_block = [".", "o"] + l_s
    p_block = [ "o", " "] + l_s
    b = list(carte)
    #c1 représnte la direction de l'action
    c1 = c1.lower()
    c2 = c2.lower()
    mur = "."
    #si l'action consiste à murer
    if c2 == "m":
        if c1 == "e" and b[b.index(symb) + 1] not in m_block:
            b[b.index(symb) + 1] = mur
        if c1 == "o" and b[b.index(symb) - 1] not in m_block:
            b[b.index(symb) - 1] = mur
        if c1 == "s" and b[b.index(symb) + 16] not in m_block:
            b[b.index(symb) + 16] = mur
        if c1 == "n" and b[b.index(symb) - 16] not in m_block:
            b[b.index(symb) - 16] = mur
    #si l'action consiste a percer
    if c2 == "p":
        if c1 == "e" and b[b.index(symb) + 1] not in p_block:
            b[b.index(symb) + 1] = " "
        if c1 == "o" and b[b.index(symb) - 1] not in p_block:
            b[b.index(symb) - 1] = " "
        if c1 == "s" and b[b.index(symb) + 16] not in p_block:
            b[b.index(symb) + 16] = " "
        if c1 == "n" and b[b.index(symb) - 16] not in p_block:
            b[b.index(symb) - 16] = " "

    a = "".join(b)
    return a
    
def deplacer(a,msgClient,n,symb):
    """Fontion permettant le déplacement du joueur
    n représente le nombre de deplacement qui sera égal à 1 dans le serveur
    a reprente la carte , symb le symbole du joueur et msgClient la commande de déplacement"""
    global l_s
    obstacle = ["o", "."]
    print("carte",a)
    b= list(a) #variable local représentant le deplacement du joueur
    msgClient= msgClient.lower()
    deplacement = msgClient
    
    if n>0 and n < len(a):        
        if deplacement == "s".lower() :
            if b[b.index(symb) + 16 * n] not in obstacle and b[b.index(symb) + 16 * n] not in l_s:
                b[b.index(symb) + 16 * n] = symb #déplacement du joueur
                b[b.index(symb)] = " "
            else:
                print("deplacement impossible")

        if deplacement == "n".lower():
            if b[b.index(symb) - 16 * n] not in obstacle and b[b.index(symb) - 16 * n] not in l_s:
                b[b.index(symb) - 16 * n] = symb
                b[b.index(symb,b.index(symb)+1)] = " "
            else:
                print("deplacement impossible")

        if deplacement == "o".lower() :
            if b[b.index(symb) - n ] not in obstacle and b[b.index(symb) - n ] not in l_s:
                b[b.index(symb) - n ] = symb
                b[b.index(symb,b.index(symb)+1)] = " "
            else:
                print("deplacement impossible")

        if deplacement == "e".lower() :
            if b[b.index(symb) + n ] not in obstacle and b[b.index(symb) + n ] not in l_s:
                b[b.index(symb) + n ] = symb
                b[b.index(symb)] = " "
            else:
                print("deplacement impossible")
            
    if b.index(symb) == a.index("U"):
        print("Vous êtes sorti du labyrinthe")
        return "vous gagnez"
    a="".join(b)
    return a

