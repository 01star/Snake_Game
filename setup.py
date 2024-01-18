import pygame
import sys

pygame.init()

# creating a time object clock 
clock = pygame.time.Clock()

# creating the screen 
screen = pygame.display.set_mode((600,750))

# creating screens now ... 
test_surface = pygame.Surface((100,200))
test_surface.fill((0,0,255))

while True:
    # event loop -- 
    # check for all possible event in pygame ...
    for event in pygame.event.get():
        # check for the quit event 
        if (event.type == pygame.QUIT):
            pygame.quit()               # exit the pygame
            sys.exit()                  # exit all the system processes related to this code 

    screen.fill((175, 215, 70))
    screen.blit(test_surface, (0,0))

    # update the screen for everyframe ... 
    pygame.display.update()
    # capping the frame rate at 60 fps
    clock.tick(60)