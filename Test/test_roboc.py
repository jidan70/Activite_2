" -*- coding:Utf-8 -*-

import unittest, pickle, sys
sys.path[:0] = ['../']

class FonctionnaliteRobocTest(unittest.TestCase):

    """ Classe testant les fonctionnalité de Roboc, de la composition de la carte
        du labyrinthe au bon fonctionnment réseau, c'est à dire de la communication
        entre le serveur et les joueurs clients"""
    def setUp(self):
        with open("labt.txt", "rb") as fichier:
            unpickler = pickle.Unpickler(fichier)
            carte = unpickler.load()
        self.carte = carte

    #test si les principaux objets fixe font bien parti de la carte importé
    def test_constitLab(self):
        lst_obj_lab = [" ", "o", "U"]
        for elt in lst_obj_lab:
            self.assertTrue(elt in self.carte)
            
    #test la si la taille de la carte est conforme à la taille supporté
    def test_tailleLab(self):
        taille_supporte = 209
        self.assertIs(len(self.carte),taille_supporte)

if __name__ == '__main__':
    unittest.main()
