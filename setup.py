import pygame
import sys, random

from pygame.math import Vector2


# SETTING UP PYGAME ...
pygame.init() 
clock = pygame.time.Clock()


# CELL INFO ...  
# the cell is a square, where the CELL_SIZE is the length of the side of the square
CELL_SIZE = 40
CELL_NUMBER = 20


# SCREEN INFO ...
# and since the screen is made up of those cells, we can  have the height and weidth of the screen as
# height = width = CELL_SIZE * CELL_NUMBERs
screen_height = CELL_SIZE * CELL_NUMBER
screen_width = CELL_SIZE * CELL_NUMBER

# creating the screen 
# we have the width and height in the cell file ... 
screen = pygame.display.set_mode((screen_height, screen_width))


# CREATING THE FRUIT ... 
class FRUIT:
    # fruit needs to be placed at a position, so we need x and y co-oridnates for it ...
    # we would also need a rectangle to place the fruit on the screen ...
    def __init__(self):
        # the position of the fruit spawn should be random ...
        self.x = random.randint(0, CELL_NUMBER - 1)
        self.y = random.randint(0, CELL_NUMBER - 1)

        # vectors are more convinient data-structures to use cause of vector operations 
        # so we will make a position vector (x, y)
        self.position = Vector2(self.x, self.y) * CELL_SIZE

    def draw_fruit(self):
        # tasks this functions needs to do ...
            # ** create a rectangle
            # ** then draw the rectangle

        # ** creating a rectangle 
        # rectangle takes 4 arguments :
            # the x, y co-ordinates where you want to place the fruit 
            # and the size of the rectangle that you want ... 

        # for the x,y -- it would be the same as the x,y of the fruit
        # and for the size, it would be the same as the CELL_SIZE
            # we had to do a typecasting since vectors give values in float ... 
            # but rectangle function wants integers 
        fruit_rectangle = pygame.Rect(int(self.position.x), int(self.position.y), CELL_SIZE, CELL_SIZE)

        # ** drawing the rectangle 
        # draw takes three arguments :
            # the screen you want to display on, which is the 'screen' for us 
            # the color you want the rectangle to have, which is Red for us
            # the rectangle you want to draw, for us is fruit_rectangle
        pygame.draw.rect(screen, (255, 0, 0), fruit_rectangle)



# CREATING THE SNAKE
class SNAKE:
    # creating the snake and placing it in the center of the screen 
    # note snake is not just a single square but a collection of one, so it would be made up of multiple 
    # since it is a collection of block, and as the game progresses the number of cells would increase 
    # it would be ideal to use linked list as a data structure to store the blocks ... 
    def __init__(self):
        self.body = [Vector2(11,10), Vector2(10,10), Vector2(9,10)]
        # this is the default direction. which is move the snake forward. 
        self.direction = Vector2(1,0)       # for now, it just moves to the right ...

    # draw the snake 
    def draw_snake(self):
        # for this we would need to draw for every cell/block that we have for the snake ... 
        # so we would loop through the entire list called body 
        for block in self.body:
            # 1. create the rectangle with the position
            x_pos = int(block.x) * CELL_SIZE
            y_pos = int(block.y) * CELL_SIZE
            snake_rectangle = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)

            # 2. draw the rectangle on the screen 
            pygame.draw.rect(screen, (0, 0, 255), snake_rectangle)

    def move_snake(self):
        body_copy = self.body[:-1]                                  # copies the entire body except the tail ...
        body_copy.insert(0, self.body[0] + self.direction)          # now we can add a head to the body in the direction 
        self.body = body_copy[:]                                    # copies the entire new moved body to the original     



# This class would contain all the logic of the code ... 
class MAIN:
    # this is the main class for the game
    # We are using this class to hopefully make the game loop more simple and easier to understand 
    # Aim to define as much things about the game as possible in this class
    def __init__(self):
        # since we only have two objects in our game 
        # namely snake and fruits, we will only have those two as objects in our class
        self.snake = SNAKE()            # creating the snake obj
        self.fruit = FRUIT()            # creating the fruit obj

    # after creating the objects of our game elements, it is also important to draw those elements on the screen
    # this is simple, since we already have defined draw functions for each of those elements
    # we simply need to call those functions to draw them 
    # as a last step we would have to call this function in the game loop ... 
    def draw_elements(self):
        # the order of drawing the elements is imp 
        # the one drawn before would be on a layer before 
        # the objects are like stack, one drawn later is drawn above the others 
        self.fruit.draw_fruit()     
        self.snake.draw_snake()


    # this is the function that is suppose to be run for every update of the screen, 
    # which would be true even when there is no input from the user ... 
    def update(self):
        # so in the game, if the user does not provide any inputs
        # the snake would keep on moving in the direction where the head is ...
        # the direction of the head is set by snake.direction (but in case of no input we just make the snake move)
        self.snake.move_snake()


# creating object of the main class ...  
main_game = MAIN()

# for now to see if the movement function works, we can create a new event ...
# this event is that it would movce the snake at priodic time ...
SCREEN_UPDATE = pygame.USEREVENT                    # this is a event that is made by me
pygame.time.set_timer(SCREEN_UPDATE, 150)


# THIS IS THE GAME LOOP 
while True:
    # event loop -- 
    # check for all possible event in pygame ...
    for event in pygame.event.get():
        # check for the quit event 
        if (event.type == pygame.QUIT):
            pygame.quit()               # exit the pygame
            sys.exit()                  # exit all the system processes related to this code 

        if(event.type == SCREEN_UPDATE):
            main_game.update()

        if (event.type == pygame.KEYDOWN):
            if event.key == pygame.K_UP :
                main_game.snake.direction = Vector2(0,-1)

            if event.key == pygame.K_DOWN :
                main_game.snake.direction = Vector2(0,1)

            if event.key == pygame.K_LEFT :
                main_game.snake.direction = Vector2(-1,0)

            if event.key == pygame.K_RIGHT :
                main_game.snake.direction = Vector2(1,0)

    screen.fill((175, 215, 70))         # this gives the background a shade of green
    main_game.draw_elements()           # creating the snake and fruits in the game ... 

    # update the screen for everyframe ... 
    pygame.display.update()
    # capping the frame rate at 60 fps
    clock.tick(60)