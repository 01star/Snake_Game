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


# creating a dictionary for storing the directions ... 
Directions = {'snake_up' : Vector2(0,-1), 'snake_down' : Vector2(0,1), 'snake_left' : Vector2(-1,0), 'snake_right' : Vector2(1,0) }

# creating the screen 
# we have the width and height in the cell file ... 
screen = pygame.display.set_mode((screen_height, screen_width))


# importing all the graphics from the graphics folder to make the game look pretty ... 
# first the fruit or apple 
apple = pygame.image.load('Graphics/Fruit/apple.png')

# now we can add the font to the game, 
game_font = pygame.font.Font('Text/PoetsenOne-Regular.ttf', 25)


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
        # pygame.draw.rect(screen, (255, 0, 0), fruit_rectangle)

        # instead of drawing the rectangle, i am going to draw the apple ... 
        screen.blit(apple, fruit_rectangle)



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

        # this is all loading the graphics for the snake itself ...
        # first loading the snake body 
        self.snake_bodyVertical = pygame.image.load('Graphics/snake/body/body_vertical.png').convert_alpha()
        self.snake_bodyHorizontal = pygame.image.load('Graphics/snake/body/body_horizontal.png').convert_alpha()

        # second loading the body curve parts ...
        self.snake_body_bottomLeft = pygame.image.load('Graphics/snake/body_turn_peice/body_bl.png').convert_alpha()
        self.snake_body_bottomRight = pygame.image.load('Graphics/snake/body_turn_peice/body_br.png').convert_alpha()
        self.snake_body_topLeft = pygame.image.load('Graphics/snake/body_turn_peice/body_tl.png').convert_alpha()
        self.snake_body_topRight = pygame.image.load('Graphics/snake/body_turn_peice/body_tr.png').convert_alpha()

        # third loading the orientation of the head ... 
        self.snake_headLeft = pygame.image.load('Graphics/snake/snake_head/head_left.png').convert_alpha()
        self.snake_headRight = pygame.image.load('Graphics/snake/snake_head/head_right.png').convert_alpha()
        self.snake_headUp = pygame.image.load('Graphics/snake/snake_head/head_up.png').convert_alpha()
        self.snake_headDown = pygame.image.load('Graphics/snake/snake_head/head_down.png').convert_alpha()

        # fourth loading all the tail orientations ... 
        self.snake_tailLeft = pygame.image.load('Graphics/snake/snake_tail/tail_left.png').convert_alpha()
        self.snake_tailRight = pygame.image.load('Graphics/snake/snake_tail/tail_right.png').convert_alpha()
        self.snake_tailUp = pygame.image.load('Graphics/snake/snake_tail/tail_up.png').convert_alpha()
        self.snake_tailDown = pygame.image.load('Graphics/snake/snake_tail/tail_down.png').convert_alpha()


    # draw the snake 
    def draw_snake(self):

        # for this we would need to draw for every cell/block that we have for the snake ... 
        # so we would loop through the entire list called body 
        for index,block in enumerate(self.body):
            # 1. create the rectangle with the position
            x_pos = int(block.x) * CELL_SIZE
            y_pos = int(block.y) * CELL_SIZE
            snake_rectangle = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)

            # This apporach is for no graphics 
            # # 2. draw the rectangle on the screen 
            # pygame.draw.rect(screen, (0, 0, 255), snake_rectangle)

            # find the direction of head .. 
            if index == 0:              # if its the head
                self.update_head_graphics()
                screen.blit(self.head, snake_rectangle)

            elif (index == len(self.body) - 1):
                self.update_tail_graphics()
                screen.blit(self.tail, snake_rectangle)
            else:
                previous_block = self.body[index - 1]
                next_block = self.body[index + 1]

                # finding the relatiave direction of the previous and next block w.r.t block
                prev_block_direction = previous_block - block
                next_block_direction = next_block - block

                # now if the x value of all the previous and next is same, we in a vertical line -- 
                if (previous_block.x == next_block.x):
                    screen.blit(self.snake_bodyVertical, snake_rectangle)

                # and if the y value of both the previous and next block is the same, we in a horizontal line -- 
                elif (previous_block.y == next_block.y):
                    screen.blit(self.snake_bodyHorizontal, snake_rectangle)

                # We have four corners left now, each which can be represented as two pair of conditions 
                
                # first corner would be the bottom_right corner --
                # now if the relative direction of the previous block is up and relavtive direction of next block is left
                # or the relative direction of next block is up and relative direction of previous block is left ...
                    # it the bottom right corner ...
                elif (prev_block_direction == Directions['snake_up'] and next_block_direction == Directions['snake_left']) or (prev_block_direction == Directions['snake_left'] and next_block_direction == Directions['snake_up']):
                    screen.blit(self.snake_body_bottomRight, snake_rectangle)

                # now using the same strategy for other corner
                # bottom left corner --
                elif (prev_block_direction == Directions['snake_up'] and next_block_direction == Directions['snake_right']) or (prev_block_direction == Directions['snake_right'] and next_block_direction == Directions['snake_up']):
                    screen.blit(self.snake_body_bottomLeft, snake_rectangle)

                # top right corner --
                elif (prev_block_direction == Directions['snake_down'] and next_block_direction == Directions['snake_left']) or (prev_block_direction == Directions['snake_left'] and next_block_direction == Directions['snake_down']):
                    screen.blit(self.snake_body_topRight, snake_rectangle)

                # top left corner -- 
                elif (prev_block_direction == Directions['snake_down'] and next_block_direction == Directions['snake_right']) or (prev_block_direction == Directions['snake_right'] and next_block_direction == Directions['snake_down']):
                    screen.blit(self.snake_body_topLeft, snake_rectangle)
             
            
    def update_head_graphics(self):
        # the direction of the head would always be the same as the direction of the input ...
        head_direction = self.direction

        if head_direction == Directions['snake_up']:
            self.head = self.snake_headUp
        elif head_direction == Directions['snake_down']:
            self.head = self.snake_headDown
        elif head_direction == Directions['snake_left']:
            self.head = self.snake_headLeft
        elif head_direction == Directions['snake_right']:
            self.head = self.snake_headRight
            
    def update_tail_graphics(self):
        # direction of the tail can be found from the change in vector values from the previous body node vector
        tail_direction = self.body[-1] - self.body[-2]

        if tail_direction == Directions['snake_up']:
            self.tail = self.snake_tailUp
        elif tail_direction == Directions['snake_down']:
            self.tail = self.snake_tailDown
        elif tail_direction == Directions['snake_left']:
            self.tail = self.snake_tailLeft
        elif tail_direction == Directions['snake_right']:
            self.tail = self.snake_tailRight
        


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
        self.draw_grass()
        self.fruit.draw_fruit()     
        self.snake.draw_snake()
        self.draw_score()


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

    
    def draw_grass(self):
        grass_color = (167, 209, 100)                # a shade of darker green 

        # so the aim is to make to background more like a check patter
        # alternating between light and dark green 
        # loop throught the mesh (2D array)
        for i in range(CELL_NUMBER):
            for j in range(CELL_NUMBER):
                x_posRect = i * CELL_SIZE
                y_posRect = j * CELL_SIZE
                grass_rect = pygame.Rect(x_posRect, y_posRect, CELL_SIZE, CELL_SIZE)

                # in every even row, at every even cell -- shade it a bit darker
                if (i % 2 == 0) and (j % 2 == 0):
                    pygame.draw.rect(screen, grass_color, grass_rect)
                
                # do the same for every odd row, at every odd cell 
                elif (i % 2 != 0) and (j % 2 != 0):
                    pygame.draw.rect(screen,grass_color, grass_rect)

                # this would create a checkers function on the background ... 
                    
    
    def draw_score(self):
        # get a way to get the score
        # for now lets just say the lenght of the snake is the score of the game ... 
        game_score = 'Score : ' + str(len(self.snake.body))          # type casted to be a string 

        # draw the score text ...
        score_surface = game_font.render(game_score, True, (56, 74, 12))

        # declaring the variables for the font position
        font_yPos = int(screen_height - 40)
        font_xPos = int(screen_width - 80)

        # drawing a rectangle for the score ... 
        score_rect = score_surface.get_rect(center = (font_xPos, font_yPos))
        screen.blit(score_surface, score_rect)



# creating object of the main class ...  
main_game = MAIN()

# for now to see if the movement function works, we can create a new event ...
# this event is that it would movce the snake at priodic time ...
SCREEN_UPDATE = pygame.USEREVENT                    # this is a event that is made by me
pygame.time.set_timer(SCREEN_UPDATE, 150)


# THIS IS THE GAME LOOP 
while True:

    screen.fill((175, 215, 70))         # this gives the background a shade of green
    main_game.draw_elements()           # creating the snake and fruits in the game ... 

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
                main_game.snake.direction = Directions['snake_up']

            # check for the downkey press,and ensuring that it does not happen if the snake is going up 
            if (event.key == pygame.K_DOWN) and (main_game.snake.direction.y != -1):
                main_game.snake.direction = Directions['snake_down']

            # check for the leftkey press,and ensuring that it does not happen if the snake is going right 
            if (event.key == pygame.K_LEFT) and (main_game.snake.direction.x != 1):
                main_game.snake.direction = Directions['snake_left']

            # check for the rightkey press,and ensuring that it does not happen if the snake is going left 
            if (event.key == pygame.K_RIGHT) and (main_game.snake.direction.x != -1):
                main_game.snake.direction = Directions['snake_right']

    # update the screen for everyframe ... 
    pygame.display.update()
    # capping the frame rate at 60 fps
    clock.tick(60)