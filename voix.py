import mido
import pygame
import threading
import main_gauche2 as main_gauche
import main_droite2 as main_droite
import notes2 as notes
import numpy as np
from time import time
import gammes2 as gammes


class Voix : 
    def __init__(self, vecteur_init, vecteur_rythme, l_tab, scale, tempo = 120) -> None:
        self.oneTime = 60/tempo
        self.i_tab = 0 #position dans la progression d'accord
        self.boolnote= True #indique le besoin de générer une nouvelle note
        self.len_tab = len(l_tab)
        self.v= notes.f_gamme(vecteur_init, scale)
        self.vrtm = vecteur_rythme
        self.debut_bar = time() - 8*oneTime