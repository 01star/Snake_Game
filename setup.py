import pygame
import sys

pygame.init()

# cell info 
# thr cell is a square, where the cell_size is the length of the side of the square
cell_size = 40
cell_number = 20

# and since the screen is made up of those cells, we can  have the height and weidth of the screen as
# height = width = cell_size * cell_numbers
screen_height = cell_size * cell_number
screen_width = cell_size * cell_number

# creating a time object clock 
clock = pygame.time.Clock()

# creating the screen 
# we have already calculated the screen height and width
# we will use those to create a screen for the game
screen = pygame.display.set_mode((screen_height, screen_width))

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