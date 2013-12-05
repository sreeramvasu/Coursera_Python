# Guess the number game 
# Author: SV
# MailTo: sreeram.vasudevan@gmail.com

import simplegui
import random
import math

# initialize global variables used in your code
num_range = 100
random_num_chosen = 0
number_of_guesses = 0


# helper function to start and restart the game
def new_game():
    # starts and restarts a new game  
    global random_num_chosen 
    global number_of_guesses
    
    random_num_chosen = random.randrange(num_range)
    number_of_guesses = int(math.ceil(math.log(num_range + 1) 
                                  / math.log(2)))
    
    print "\nNew game. Range is from 0 to", num_range
    print "Number of remaining guesses is", number_of_guesses 
    

# define event handlers for control panel
def range100():
    # button that changes range to range [0,100) and restarts
    global num_range
        
    num_range = 100
    new_game()       
  

def range1000():
    # button that changes range to range [0,1000) and restarts
    global num_range
        
    num_range = 1000
    new_game() 
    
    
def input_guess(guess):
    # main game logic goes here	
    global number_of_guesses
    global num_range
    
    # casting the input guess to integer type
    guess = int(guess)
    
    print "\nGuess was", guess    
    
    number_of_guesses -= 1
    print "Number of remaining guesses is", number_of_guesses
    
    # game ends due to running out of guesses
    if number_of_guesses == 0 and guess != random_num_chosen:
        print "You ran out of guesses. The number was", random_num_chosen
        num_range = 100
        new_game()
        return   
    
    # game ends due to correct answer obtained
    if guess == random_num_chosen:
        print "Correct!"
        num_range = 100
        new_game()
        return  
    
    if guess > random_num_chosen:
        print "Lower!"
    else:
        print "Higher!"   
        
        
# create frame
game_frame = simplegui.create_frame("Guess the number",200,200)

# register event handlers for control elements
game_frame.add_button("Range is [0,100)", range100, 200)
game_frame.add_button("Range is [0,1000)", range1000, 200)
game_frame.add_input("Enter a guess", input_guess, 200)

# call new_game and start frame
new_game()
game_frame.start()

# always remember to check your completed program against the grading rubric
