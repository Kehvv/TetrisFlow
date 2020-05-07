#!/usr/bin/env python
# coding: utf-8

# In[19]:


import pygame
import random
pygame.font.init()


# In[20]:


#-------- CONSTANTS ----------#

s_width = 800
s_height = 700
p_width = 300  # meaning 300 // 10 = 30 width per block
p_height = 600  # meaning 600 // 20 = 30 height per block
block_size = 30
top_left_x = (s_width - p_width) // 2
top_left_y = s_height - p_height


# In[21]:


#---------- TETROMINO SHAPE FORMATS ----------#
Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [Z, S, O, J, L, I, T]
s_colours = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


# In[22]:


#-------- Tetromino class definition ----------#
class Tetromino(object):  
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.colour = s_colours[shapes.index(shape)]
        self.rotation = 0


# In[35]:


#--------- grid ----------#
def grid_create(locked_pos={}):  # 
    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)] #create list for every row in grid and draw black 

    for i in range(len(grid)):
        for j in range(len(grid[i])): # loop through grid
            if (j, i) in locked_pos: # if a block exists in this position
                c = locked_pos[(j,i)] #set as var c
                grid[i][j] = c #change grid position to c
    return grid

#-------- shape convert to positions based on formats ---------#
def shape_reformat(shape):# convert shape formats into drawn blocks
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)] #modulo of the rotation based on number of rotation positions in format - select correct shape from array

    for i, line in enumerate(format): #loop through format
        row = list(line) #convert to list format
        for j, column in enumerate(row): #loop through the row list 
            if column == '0': #where the line contains zero
                positions.append((shape.x + j, shape.y + i)) #add the shape x and y value to positions list

    for i, pos in enumerate(positions): #reposition the blocks to be offset into correct position
        positions[i] = (pos[0] - 2, pos[1] - 4) #

    return positions

#----------- check if new space is valid ---------#
def pos_valid(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]  #store all positions in the grid if nothing exists in the position
    accepted_pos = [j for sub in accepted_pos for j in sub] #reformat positons into flat list

    formatted = shape_reformat(shape) #pass in shape to be formatted

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1: #check if y value is greater than -1 to only show if it is visible on screen
                return False
    return True

#-----------check if game lost ---------#
def lose_condition_check(positions): #function to check if any blocks exist above the screen i.e. that the game is lost
    for pos in positions:
        x, y = pos
        if y < 1: #check if y value is 0 or less for any positions passed
            return True

    return False

def get_shape():
    return Tetromino(5, 0, random.choice(shapes)) #select one of the shapes at random and draw at position 5, 0 for the middle and top of grid

def draw_text_middle(surface, text, size, colour): #function to display end game text
    font = pygame.font.SysFont("Bauhaus 93", size, bold=True)
    label = font.render(text, 1, colour)
    
    #deciding where to display text by dividing screen dimensions to get centre
    surface.blit(label, (top_left_x + p_width /2 - (label.get_width()/2), top_left_y + p_height/2 - label.get_height()/2))


def draw_grid(surface, grid): #draw grey lines over the grid structure
    sx = top_left_x #start x
    sy = top_left_y # start y

    for i in range(len(grid)): #loop through rows in grid
        pygame.draw.line(surface, (128,128,128), (sx, sy + i*block_size), (sx+p_width, sy+ i*block_size)) #draw grey line, update x value each loop
        for j in range(len(grid[i])): #loop through columns
            pygame.draw.line(surface, (128, 128, 128), (sx + j*block_size, sy),(sx + j*block_size, sy + p_height)) #draw grey line, update y value each loop
        


def clear_rows(grid, locked):

    inc = 0
    for i in range(len(grid)-1, -1, -1): #loop through grid backwards as deletion needs to start from bottom to avoid overwrite
        row = grid[i] # set row equal to every row in grid
        if (0,0,0) not in row: #if colour black is not in row i.e. there are no empty blocks
            inc += 1 #increment +1 to save how many rows have been deleted
            ind = i #save the index of the row that has been removed
            for j in range(len(row)): #loop through j in the row
                try:
                    del locked[(j,i)] #try delete from the locked positions
                except:
                    continue

    if inc > 0: #if incremented i.e. if any rows have been deleted
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]: #sort locked positions list by y value
            x, y = key #get x,y of each position in locked position
            if y < ind: # if the y value of the locked position is greater than y i.e. if it is higher up the grid than the deleted row
                newKey = (x, y + inc) #increment the y value of the row above the deleted row by the number of deleted rows
                locked[newKey] = locked.pop(key) #save new key as old key

    return inc

#--------next shape ---------#
def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('Bauhaus 93', 30)
    label = font.render('Next Shape', 1, (255,255,255)) #label for next shape box
    
    #---------- label position ----------#
    sx = top_left_x + p_width + 50 ##setting position of label
    sy = top_left_y + p_height/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)] #to get sublist

    for i, line in enumerate(format):
        row = list(line) #store row 
        for j, column in enumerate(row): #loop through shape row
            if column == '0': #if the cell contains a block
                pygame.draw.rect(surface, shape.colour, (sx + j*block_size, sy + i*block_size, block_size, block_size), 0) #draw the rectangle shape

    surface.blit(label, (sx , sy - 40)) #draw label
    
#------------- SCORE ----------#
def update_score(nscore): #update the text doc
    score = max_score() #save the current score as max score

    with open('scores.txt', 'w') as f:
        if int(score) > nscore: #if new score is less than stored score
            f.write(str(score)) #save old score
        else:
            f.write(str(nscore)) #overwrite old score with new score


def max_score(): #function to read the score from txt file
    with open('scores.txt', 'r') as f: #reads scores file 
        lines = f.readlines() #store the line value
        score = lines[0].strip() #set as score and strip any blankspace
    return score

#-------------- load emotion from recognition module -----------#
def current_emotion(): #function to read the current emotion from the emotion recognition
    emotion = ''
    
    with open('emotion.txt', 'r') as f: #reads emotion file 
        emotionString = 'unknown'
        lines = f.readlines() #store the line value
        try:
            emotion = lines[0].strip()
        except IndexError:
            pass
       #check emotion
        if emotion == '0':
            emotionString ='Angry'
        elif emotion == '1':
            emotionString ='Disgust'
        elif emotion == '2':
            emotionString ='Fear'
        elif emotion == '3':
            emotionString ='Happy'
        elif emotion == '4':
            emotionString ='Sad'
        elif emotion == '5':
            emotionString ='Surprise'
        elif emotion == '6':
            emotionString ='Neutral'
        else:
            emotionString = emotion
            
    return emotionString


def draw_window(surface, grid, difficulty, emotion, score=0, last_score = 0):
    surface.fill((0, 0, 0))
    
    text_colour = (255, 255, 255)
    # change colour based on positive or negative emotion
    if (emotion == 'Happy'):
        text_colour = (221,160,221)
    elif (emotion == 'Neutral'):
        text_colour = (152,251,152)
    else:
        text_colour = (220,20,60)
    
    # TetrisFlow Label #
    pygame.font.init()
    font = pygame.font.SysFont('Bauhaus 93', 60)
    label = font.render('TetrisFlow', 1, text_colour)

    surface.blit(label, (top_left_x + p_width / 2 - (label.get_width() / 2), 30))
    
    # Emotion Label #
    font = pygame.font.SysFont('Bauhaus 93', 20)
    label = font.render('Current emotion: ' + emotion, 1, text_colour)
    sx = top_left_x + 300
    sy = top_left_y - 100

    surface.blit(label, (sx + 20, sy + 160))
    
    # fall speed label #
    font = pygame.font.SysFont('Bauhaus 93', 20)
    label = font.render('Current Speed: ' + str(round(difficulty, 2)), 1, text_colour)
    sx = top_left_x - 220
    sy = top_left_y + 100

    surface.blit(label, (sx + 20, sy + 160))

    # current score label #
    font = pygame.font.SysFont('Bauhaus 93', 30)
    label = font.render('Score: ' + str(score), 1, (255,255,255))

    sx = top_left_x + p_width + 50
    sy = top_left_y + p_height/2 - 100

    surface.blit(label, (sx + 20, sy + 160))
    
    # highest score label #
    font = pygame.font.SysFont('Bauhaus 93', 20)
    label = font.render('High Score: ' + last_score, 1, (255,255,255))

    sx = top_left_x - 200
    sy = top_left_y + 200

    surface.blit(label, (sx + 20, sy + 160))

    for i in range(len(grid)):
        for j in range(len(grid[i])): #loop through grid
            #draw on surface, colour is grid i j, position where to draw
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, text_colour, (top_left_x, top_left_y, p_width, p_height), 5) #draw dynamic coloured box to display play area

    draw_grid(surface, grid)
        


def main(window_main):  # *
    last_score = max_score()
    locked_positions = {}
    grid = grid_create(locked_positions)

    change_tetromino = False
    run = True
    current_tetromino = get_shape()
    next_tetromino = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    difficulty = 0.3
    level_time = 0
    score = 0

    while run:
        grid = grid_create(locked_positions)
        fall_time += clock.get_rawtime() #stores since loop ran
        level_time += clock.get_rawtime() 
        clock.tick()
        emotion = current_emotion()
     
        
#     #--------- INCREASES DIFFICULTY OVER TIME ---------#
#         if level_time/1000 > 5:
#             level_time = 0
#             if difficulty > 0.1: #ensures the fall speed does not get reduced any further than this - 0.1 is max difficulty
#                 difficulty  -= 0.005 # increment to decrease speed
#     #---------  ---------#
        
    #--------- ADJUSTS DIFFICULTY BASED ON EMOTION ---------#
        if (emotion == 'Happy'):
            if difficulty > 0.1: #ensures the fall speed does not get reduced any further than this - 0.1 is max difficulty
                difficulty  -= 0.0005 # decrement to increase speed and difficulty
        elif (emotion == 'Neutral'):
            difficulty = difficulty #no change to speed when neutral
        else:
            if difficulty < 1.0: #ensures the fall speed does not get increassed any further than this - 1.0 is lowest difficulty
                difficulty  += 0.0005
    #---------  ---------#
                
        if fall_time/1000 > difficulty:  #checks how much time has passed compared to defined fall speed
            fall_time = 0 #reset fall time
            current_tetromino.y += 1 #increment the y value of the piece
            if not(pos_valid(current_tetromino, grid)) and current_tetromino.y > 0: #check if y value is correct i.e greater than 0
                current_tetromino.y -= 1 #revert y increment
                change_tetromino = True #stop movement on this piece

        for event in pygame.event.get():
            if event.type == pygame.QUIT: #if event is quit
                run = False #stop running game
                pygame.display.quit() #quit game

            if event.type == pygame.KEYDOWN: #if event is a key press
                if event.key == pygame.K_LEFT: # if the key pressed is the left key
                    current_tetromino.x -= 1 #reduce x value of current piece by 1
                    if not(pos_valid(current_tetromino, grid)): #if the new space is not valid
                        current_tetromino.x += 1 #revert change to x value
                if event.key == pygame.K_RIGHT: # if the key pressed is the right key
                    current_tetromino.x += 1 #increase x value of current piece by 1
                    if not(pos_valid(current_tetromino, grid)): #if the new space is not valid
                        current_tetromino.x -= 1 #revert change to x value
                if event.key == pygame.K_DOWN: # if the key pressed is the down key
                    current_tetromino.y += 1 #increase y value of current piece by 1
                    if not(pos_valid(current_tetromino, grid)): #if the new space is not valid
                        current_tetromino.y -= 1  #revert change to y value
                if event.key == pygame.K_UP:  # if the key pressed is the up key
                    current_tetromino.rotation += 1 #increase rotation value of current piece by 1
                    if not(pos_valid(current_tetromino, grid)): #if the new space is not valid
                        current_tetromino.rotation -= 1  #revert change to rotation value

        shape_pos = shape_reformat(current_tetromino) #store current piece

        for i in range(len(shape_pos)): #loop through shape
            x, y = shape_pos[i]
            if y > -1: #check if y is 0 or greater i.e. on the grid and not above the screen
                grid[y][x] = current_tetromino.colour #store colours from shape 

        if change_tetromino:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_tetromino.colour #store the location and colour of a shape that is now locked
            current_tetromino = next_tetromino # move to next piece
            next_tetromino = get_shape() #save next piece from random shapes
            change_tetromino = False 
            score += clear_rows(grid, locked_positions) * 10 #increments the score by the number of rows cleared * 10

        draw_window(window_main, grid, difficulty, emotion, score, last_score) #pass in the surface, score and high score from txt file
        draw_next_shape(next_tetromino, window_main) #draw next shape and label
        pygame.display.update()

        if lose_condition_check(locked_positions): #checking lose condition i.e. blocks are above y value
            draw_text_middle(window_main, "YOU LOST!", 80, (255,255,255)) #output lose game text
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            update_score(score) #update the saved high score
        


def main_menu(window_main):  # start in main menu
    run = True
    while run:
        window_main.fill((0,0,0)) #fill screen black
        draw_text_middle(window_main, 'Press Any Key To Play', 60, (255,255,255)) #display text
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #if game is closed
                run = False
            if event.type == pygame.KEYDOWN: #if any key is pressed
                main(window_main) #call main function onto window

    pygame.display.quit()


window_main = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('TetrisFlow')
main_menu(window_main)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




