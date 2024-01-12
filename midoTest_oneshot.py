import mido
import pygame
import threading
import main_gauche2 as main_gauche
import main_droite2 as main_droite
import notes2 as notes
import numpy as np
from time import time


#test variables
vecteur_rythme = notes.norm(np.array([2, 4, 1, 3, 1, 0, 0, 0])) #le vecteur de proba des rythmes

vecteur_courant = notes.gauss(notes.init_v(), 50)

l_tab = [('A', 'Minor', ''), ('D', 'Minor', ''), ('G', 'Major', ''), ('G', 'Major', '')]

bpm = 120
oneTime = 60/bpm

# Function to play music
def play_music(output_port):
    
    i_tab = 0 #position dans la progression d'accord
    boolnote = True #indique le besoin de générer une nouvelle note
    len_tab = len(l_tab)
    v = vecteur_courant
    vrtm = vecteur_rythme
    debut_bar = time
    
    while playing:
            
        #on gère le changement d'accord
        if time() >= oneTime*8 + debut_bar: #début de mesure par la fin de la precedente
            root, quality, seventh = l_tab[i_tab]
            v = notes.f_newtab(v, root, quality, seventh)
            i_tab = (i_tab + 1)%len_tab
            debut_bar += oneTime*8
            print(root, quality, seventh)

        #on gère l'arrivée d'une nouvelle note
        if boolnote:
            tp = main_droite.gen(vrtm) + 1 #le nombre de temps de la note que l'on va jouer
            t_end = time() + tp*oneTime
            new_note = main_droite.gen(v)
            note_on = mido.Message('note_on', note = new_note, velocity = 64) #on enclenche la note
            output_port.send(note_on) #et on commence à la jouer
            boolnote = False #indique qu'une note est jouée
            v = notes.f_note(v, new_note) #la fonction qui modifie v à chaque note
        
        #on regarde si on peut jouer une nouvelle note
        elif time() > t_end:
            note_off = mido.Message('note_off', note = new_note)
            output_port.send(note_off)
            boolnote = True
                

    """while playing:
        # Replace this with your own logic to generate MIDI messages
        # For example, playing a C4 note with velocity 64 for 1 second
        note_on = mido.Message('note_on', note=60, velocity=64)
        output_port.send(note_on)
        time.sleep(1)
        note_off = mido.Message('note_off', note=60)
        output_port.send(note_off)
        time.sleep(1)"""

# Initialize pygame for handling user input
pygame.init()

# Set up MIDI output port (replace 'Your MIDI Port' with your actual MIDI output port name)
output_port_name = 'Microsoft GS Wavetable Synth 0'
output_port = mido.open_output(output_port_name)

# Variable to control music playback
playing = True

# Start the music playback in a separate thread
music_thread = threading.Thread(target=play_music, args=(output_port,))
music_thread.start()

# Set up the Pygame window
width, height = 400, 200
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Music Generator')

# Font for text
font = pygame.font.Font(None, 36)

loop = -1

# Main loop for handling user input
while True:
    loop+=1
    for event in pygame.event.get():
        #print("got event")
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Toggle between playing and pausing the music
                playing = not playing
                if playing:
                    print("Resumed music.")
                else:
                    print("Paused music.")
            elif event.key == pygame.K_ESCAPE:
                # Exit the program
                playing = False
                pygame.quit()
                exit()
    
    # Update the display
    screen.fill((255, 255, 255))

    # Display text
    text = font.render('Press SPACE to toggle playback', True, (0, 0, 0))
    screen.blit(text, (50, 50))

    pygame.display.flip()

    # Add a small delay to reduce CPU usage
    pygame.time.delay(10)
# Wait for the music thread to finish before exiting
music_thread.join()
pygame.quit()
