# Mini-project #6 - Blackjack
# Author: SV
# Mailto: sreeram.vasudevan@gmail.com

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# Position variables
HEAD_POSITION = (100,60)
SCORE_POSITION = (450, 60)
OUTCOME_POSITION = (100, 120)
PLAYER_POSITION = (60, 420)
DEALER_POSITION = (60, 220)

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos, is_flipped = True):
        ''' Based on the card being flipped or not, either the card or its back is displayed '''
        
        if is_flipped == False:
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        else:
            canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [pos[0] + CARD_BACK_CENTER[0], pos[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.hand = []
        self.hide_second = False

    def __str__(self):
        # return a string representation of a hand
        return_hand_str = 'Hand contains'
        
        for card in self.hand:
            return_hand_str += ' ' + str(card)
        
        return return_hand_str

    def add_card(self, card):
        # add a card object to a hand
        self.hand.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        value = 0
        aces = 0
        for card in self.hand:
            value += VALUES[card.get_rank()]
            if card.get_rank() == 'A':
                aces += 1
        
        if aces == 0:
            return value
        else:
            if value + 10 > 21:
                return value
            else:
                return value + 10
            
      
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        count = 0
        for card in self.hand:
            if count == 1 and self.hide_second == True:
                card.draw(canvas, [pos[0] + count * (CARD_SIZE[0] + 20), pos[1]], True)
            else:
                card.draw(canvas, [pos[0] + count * (CARD_SIZE[0] + 20), pos[1]], False)
            count += 1
 
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck = [Card(suit, rank) for suit in SUITS for rank in RANKS]
        random.shuffle(self.deck)

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)

    def deal_card(self):
        # deal a card object from the deck
        return self.deck.pop()
    
    def __str__(self):
        # return a string representing the deck
        return_deck_str = 'Deck contains'
        
        for card in self.deck:
            return_deck_str += ' ' + str(card)
        
        return return_deck_str
    

#define event handlers for buttons
def deal():
    global outcome, in_play, score
    global deck, player_hand, dealer_hand
    
    # creating a deck and initializing players hand
    deck = Deck()
    player_hand, dealer_hand = Hand(), Hand()

    # if Deal is pressed in the middle of a game, player loses a point
    if in_play == True:
        score -= 1
    # game starts
    in_play = True
    
    # get the initial cards from the deck for the player as well as dealer
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    
    outcome = 'Game in progress. Hit or stand?'
    
    # hiding the second card of the dealer
    dealer_hand.hide_second = True
    
def hit():
    
    # if the hand is in play, hit the player
    # if busted, assign a message to outcome, update in_play and score
    global score, outcome, in_play
    
    if not player_hand.get_value() > 21 and in_play:
        player_hand.add_card(deck.deal_card())
        
        if player_hand.get_value() > 21:
            # player got busted as total exceeded 21
            outcome = 'You went bust and you lose! Deal again?'
            dealer_hand.hide_second = False
            in_play = False
            score -= 1
      
def stand():
       
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    # assign a message to outcome, update in_play and score
    global in_play, score, outcome
    
    if in_play:
        if not player_hand.get_value() > 21:
            dealer_hand.hide_second = False
            
            while dealer_hand.get_value() < 17:
                dealer_hand.add_card(deck.deal_card())
                
            if dealer_hand.get_value() > 21:
                outcome = 'Dealer went bust. You win! New Deal?'
                score += 1
            else:
                # If its a tie, then dealer wins the game
                if dealer_hand.get_value() > player_hand.get_value():
                    outcome = 'Dealer wins! New Deal?'
                    score -= 1
                elif dealer_hand.get_value() == player_hand.get_value():
                    outcome = 'Its a tie and Dealer gets the game! New Deal?'
                    score -= 1
                else:
                    outcome = 'You win! New Deal?'
                    score += 1
                    
            # the game is stopped
            in_play = False
        else:
            outcome = 'You went bust and lose! New Deal?'
    else: 
        outcome = 'New Deal?'
      

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    
    canvas.draw_text('Blackjack', HEAD_POSITION, 40, 'Turquoise', 'sans-serif')
    canvas.draw_text('Score ' + str(score), SCORE_POSITION, 25, 'Black', 'sans-serif')
    canvas.draw_text(outcome, OUTCOME_POSITION, 22, 'Black', 'sans-serif')
    canvas.draw_text('Dealer', (60, 200), 25, 'Black', 'sans-serif')
    canvas.draw_text('Player', (60, 400), 25, 'Black', 'sans-serif')
   
    player_hand.draw(canvas, PLAYER_POSITION)
    dealer_hand.draw(canvas, DEALER_POSITION)


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
