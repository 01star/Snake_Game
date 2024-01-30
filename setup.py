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
        self.randomize()

    def randomize(self):
        # this function basically randomizes the location of the fruit itself ... 
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
        self.body = [Vector2(10,10), Vector2(9,10), Vector2(8,10)]
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

    def add_block(self):
        # this function just adds a block to the body of the snake
        # must only be called when a fruit is eaten

        # to implement it, we just make a copy of the last element in the body 
        # and append it to the very end of the list (body)
        snake_tail = self.body[-1]
        self.body.append(snake_tail)



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

        # we also want to check for collsiion between the snake and fruit, 
        # so we call the collition fucntion, we have defined in the class  
        self.check_collision()

        # check of the end of game states too 
        # so we simply call the check_end_state function
        self.check_end_state()

    def check_collision(self):
        # if the snake is at the position of the fruit, its a collision
        # now, we can get the position of the fruit from the position variable in its class
        # but snake does not have that, but we can check for the first element of the body -- the head
        # now, if they are the same, then we know that a collision happened between them ... 

        # the issue is, the body of the sanke is a list of vectors representing cells, and not pixels 
        # while the fruit does the opposite, it stores the position as pixels ... 
        # so to make them equal we would need to multiply the snake's head vector by cell_size 
        if (self.fruit.position == self.snake.body[0] * CELL_SIZE):
            # now we need to have two features in this function 
                # 1. we should delete this fruit and respawn a new one
                # 2. and we should increase the length of our snake by 1 cell ...
            
            # Feature 1 -- 
            # Approach 1 ...
                # so for the first feature, we just need to create a new object for the fruit element
                # doing so, it will replace the old object with the new object
                # and we have intiallized the fruit class to always have a randowm spawn location for the fruit
                # So, by simply creating a new object for fruit we achive both our goals for feature one 
                # self.fruit =  FRUIT()

            # Approach 2 ...
                # we randomize the location of the fruit itself
                # for this we can use the randomize function, which we can define in the fruit class itself 
                # this apporach is better than 
            self.fruit.randomize()


            # Feature 2
            # Approach 1 -- 
                # Now for second feature, we need to add an object to the end of the snake 
                # so we can just append the element to the end of the body
                # and the element to be iserted would be the same as the last element of the body
                # this all has been done in the add_block function of the snake class
            self.snake.add_block()

    
    def check_end_state(self):
        # End state can only happen in two states, 
            # check if the snake is outside the screen
            # if the snake was colliding with its own body 
        
        snake_head_post = self.snake.body[0] * CELL_SIZE
        # first condition, going out of the screen
        # we just have to make sure that the head of the snake is never outside the screen ...
        if (snake_head_post.x >= screen_width or snake_head_post.x < 0 or snake_head_post.y <0 or snake_head_post.y >= screen_height):
            # game over 
            self.game_over()
            print('game over')

        
        # the second condition is snake biting itself
        # to check for this, we can simply loop through the entire body of the snake
        # so if the position of head of the snake == any other body then game over
        for body_cell in self.snake.body[1:]:
            if (body_cell.x * CELL_SIZE == snake_head_post.x and body_cell.y * CELL_SIZE == snake_head_post.y):
                # game over
                self.game_over()
                print('game over biting the body')

    
    def game_over(self):
    # this function is called when the game is in the game over state
        pygame.quit()
        sys.exit()


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
            # check for the upkey press,and ensuring that it does not happen if the snake is going down 
            if (event.key == pygame.K_UP) and (main_game.snake.direction.y != 1):
                main_game.snake.direction = Vector2(0,-1)

            # check for the downkey press,and ensuring that it does not happen if the snake is going up 
            if (event.key == pygame.K_DOWN) and (main_game.snake.direction.y != -1):
                main_game.snake.direction = Vector2(0,1)

            # check for the leftkey press,and ensuring that it does not happen if the snake is going right 
            if (event.key == pygame.K_LEFT) and (main_game.snake.direction.x != 1):
                main_game.snake.direction = Vector2(-1,0)

            # check for the rightkey press,and ensuring that it does not happen if the snake is going left 
            if (event.key == pygame.K_RIGHT) and (main_game.snake.direction.x != -1):
                main_game.snake.direction = Vector2(1,0)

    screen.fill((175, 215, 70))         # this gives the background a shade of green
    main_game.draw_elements()           # creating the snake and fruits in the game ... 

    # update the screen for everyframe ... 
    pygame.display.update()
    # capping the frame rate at 60 fps
    clock.tick(60)