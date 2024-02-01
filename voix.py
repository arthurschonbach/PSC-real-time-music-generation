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
    """
    c'est une classe virtuelle
    elle sert de classe mère pour toutes les autres voix
    """
    def __init__(self, vecteur_init, vecteur_rythme, l_tab, scale, output_port, tempo = 120) -> None:
        self.oneTime = 60/tempo
        self.vrtm = vecteur_rythme
        self.l_tab = l_tab
        self.vecteur_init = vecteur_init
        self.output_port = output_port

        # à décider dans les classes
        self.velocity = 64
        self.channel
        self.program

        self.i_tab = 0 #position dans la progression d'accord
        self.boolnote= True #indique le besoin de générer une nouvelle note
        self.note_on
        self.t_end
        self.root
        self.quality
        self.seventh
        self.len_tab = len(l_tab)
        self.v= notes.f_gamme(self.vecteur_init, scale)
        self.debut_bar = time() - 8*self.oneTime
    
    def nextTime(self, t = time()):
        if time() >= self.oneTime*8 + self.debut_bar: #début de mesure par la fin de la precedente
           self.changeMesure()
        
        if self.boolnote: #une nouvelle note
            self.t_end = self.durationNote(t)
            self.new_note = self.newNote()
            note_on = mido.Message("note_on", note = self.new_note, channel = self.channel, velocity = self.velocity)
            self.output_port.send(note_on)
            self.boolnote = False
            self.v = notes.f_note(self.v, self.new_note)
        
        elif time() > self.t_end : #
            note_off = mido.Message("note_off", note = self.new_note, channel = self.channel, velocity = self.velocity)
            self.output_port.send(note_off)
            self.boolnote = True


    def changeMesure(self):
        self.root, self.quality, self.seventh = self.l_tab[i_tab]
        i_tab = (i_tab + 1)%self.len_tab
        debut_bar += self.oneTime*8
        print(self.root, self.quality, self.seventh)
    
    def newNote(self):
        return main_droite.gen(self.v)

    def durationNote(self, t):
        return t

    def choixInstrument(self):
        instru = mido.Message("program_change", program = self.program)
        self.output_port.send(instru)

class VoixGauche(Voix) : 
    def __init__(self, vecteur_init, vecteur_rythme, l_tab, scale, output_port, tempo=120) -> None:
        super().__init__(vecteur_init, vecteur_rythme, l_tab, scale, output_port, tempo)
        
        self.channel = 0
        self.program = 0 #piano

        self.rtm = main_gauche.nouvelle_structure_rythmique(self.vrtm)
        self.i_rtm = 0
        self.len_rtm = len(self.rtm)

        self.choixInstrument()
    
    def changeMesure(self):
        super().changeMesure()
        self.v = self.vecteur_init
        self.v = notes.f_gamme(self.v, gammes.accord(self.root, self.quality, self.seventh))
    
    def newNote(self):
        return super().newNote
    
    def durationNote(self, t):
        tp_l = self.rtm[self.i_rtm]  #le nombre de temps de la note que l'on va jouer
        i_rtm_l = (i_rtm_l + 1)%self.len_rtm
        return time() + tp_l*self.oneTime

class VoixDroite(Voix):
    def __init__(self, vecteur_init, vecteur_rythme, l_tab, scale, output_port, tempo=120) -> None:
        super().__init__(vecteur_init, vecteur_rythme, l_tab, scale, output_port, tempo)

        self.channel = 1
        self.program = 0 #piano

        self.choixInstrument()
    
    def changeMesure(self):
        self.v = notes.f_newtab(self.v, self.root, self.quality, self.seventh)
    
    def newNote(self):
        return super().newNote()
    
    def durationNote(self, t):
        tp = main_droite.gen(self.vrtm)
        t_end = t + tp*self.oneTime
        return t_end