# implementation of card game - Memory
# Author: SV
# Mailto: sreeram.vasudevan@gmail.com

import simplegui
import random
import math

# helper function to initialize globals
def new_game():
    global numbers, exposed, card_limit, turns
    global first_card, second_card, state
        
    # generating a list of 16 numbers in range [0,8)
    numbers = [ num for num in range(8) ] * 2
    random.shuffle(numbers)
    
    # setting the exposed state of all cards to False
    exposed = [ False for num in numbers ]
    
    # setting the boundary for card
    card_limit = [ 25 + 800 / 16 *i for i in range(16) ]
    
    turns, first_card, second_card, state  = 0, 0, 0, 0   
    
     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, exposed, first_card, second_card, turns
    
    for count,value in enumerate(numbers):
        # 48 is the maximum width of green colour line
        if math.fabs(pos[0] - card_limit[count]) < 48 / 2:
            if state == 0:
                state, first_card = 1, count
                exposed[count] = True
                
            elif state == 1:
                if exposed[count] == False:
                    exposed[count] = True
                    state, second_card = 2, count
                    turns = turns + 1
                    
            else:
                if exposed[count] == False:
                    exposed[count] = True
                    state = 1
                    if numbers[first_card] != numbers[second_card]:
                        exposed[first_card] = False
                        exposed[second_card] = False
                    first_card = count
    
                            
# cards are logically 50x100 pixels in size    
def draw(canvas):
    label.set_text('Turns = ' + str(turns))
    for count,value in enumerate(exposed):
        if value == True:
            canvas.draw_text(str(numbers[count]), (card_limit[count] - 20, 70), 40, 'White', 'serif')
        else:
            canvas.draw_line((card_limit[count], 0), (card_limit[count], 100), 48, 'Green')

            
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric
