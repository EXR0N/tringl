# https://www.youtube.com/watch?v=i6xMBig-pP4
size = (600, 500)
state = 1 # 0 = off, 1 = on
framerate = 50

import pygame
import object

pygame.init()
win = pygame.display.set_mode(size) # init a window with a size
pygame.display.set_caption("Window Title!") # set the window title

posx = size[0]/2
posy = size[1]/2
width = 20
height = 20
speed = 5

while state: # main loop
    # get inputs
    for event in pygame.event.get(): # pygame.event.get() returns a list for everything that a user might do, such as key presses, mouse, etc
        #print(event)

        if event.type == pygame.QUIT:
            print('Exit')
            state = 0
            break

    k_down = pygame.key.get_pressed() # returns an array of all the keys, and at each index either a 1 or 0
    if k_down[pygame.K_LEFT]: # left arrow key
        posx -= speed
    if k_down[pygame.K_RIGHT]: # right arrow key
        posx += speed
    if k_down[pygame.K_UP]: # up arrow key
        posy -= speed
    if k_down[pygame.K_DOWN]: # down arrow key
        posy += speed

    # draw stuff
    pygame.draw.rect(win, (255, 0, 0), (posx, posy, width, height))

    #update display
    pygame.display.update() # update the display
    pygame.time.delay(int(1000/framerate)) # miliseconds, this is the frame rate here
    win.fill( (105, 105, 105) ) # draw the background over everything... we have this below everything so its ontop of everything in the next cycle

pygame.quit() # this ends the program if the while loop fails
