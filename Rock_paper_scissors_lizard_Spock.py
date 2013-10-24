# Rock-paper-scissors-lizard-Spock 
# Author: SV
# MailTo: sreeram.vasudevan@gmail.com


# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

# 5 is reserved for invalid name/number

# helper functions

import random
import math

def number_to_name(number):
    # fill in your code below
    
    # convert number to a name using if/elif/else
    # don't forget to return the result!
    
    if number == 0:
        return 'rock'
    elif number == 1:
        return 'Spock'
    elif number == 2:
        return 'paper'
    elif number == 3:
        return 'lizard'
    elif number == 4:
        return 'scissors'
    else:
        return 'Invalid number'

    
def name_to_number(name):
    # fill in your code below

    # convert name to number using if/elif/else
    # don't forget to return the result!
    
    if name == 'rock':
        return 0
    elif name == 'Spock':
        return 1
    elif name == 'paper':
        return 2
    elif name == 'lizard':
        return 3
    elif name == 'scissors':
        return 4
    else:
        return 5

def rpsls(name): 
    # fill in your code below

    # convert name to player_number using name_to_number
    player_number = name_to_number(name)
    
    # error handling for invalid number
    if player_number >= 5:
        print number_to_name(player_number)
        return

    # compute random guess for comp_number using random.randrange()
    comp_number = random.randrange(0,5)
    
    if comp_number >= 5:
        print number_to_name(comp_number)
        return

    # compute difference of player_number and comp_number modulo five
    diff_obtained = (player_number - comp_number)%5

    # use if/elif/else to determine winner
    if diff_obtained == 0:
        winner = 'Player and computer tie!'
    elif diff_obtained > 0 and diff_obtained < 3:
        winner = 'Player wins!'
    else:
        winner = 'Computer wins!'

    # convert comp_number to name using number_to_name
    comp_name = number_to_name(comp_number)
    
    # print results
    print "\n"
    print "Player chooses " + name
    print "Computer chooses " + comp_name
    print winner
    
    
# testing the code
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")




