import pygame
import sys

pygame.init()

# cell info 
cell_size = 40

# creating a time object clock 
clock = pygame.time.Clock()

# creating the screen 
screen = pygame.display.set_mode((600,750))

while True:
    # event loop -- 
    # check for all possible event in pygame ...
    for event in pygame.event.get():
        # check for the quit event 
        if (event.type == pygame.QUIT):
            pygame.quit()               # exit the pygame
            sys.exit()                  # exit all the system processes related to this code 

    screen.fill((175, 215, 70))         # this gives the background a shade of green

    # update the screen for everyframe ... 
    pygame.display.update()
    # capping the frame rate at 60 fps
    clock.tick(60)