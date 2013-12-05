# Implementation of classic arcade game Pong
# Author: SV
# Mailto: sreeram.vasudevan@gmail.com

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
LEFT = False
RIGHT = True

# initialize ball_pos and ball_vel for new bal in middle of table
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [2, 1]

# initialize paddle parameters
paddle1_pos = PAD_HEIGHT / 2
paddle2_pos = PAD_HEIGHT / 2
paddle1_vel = 0
paddle2_vel = 0
PADDLE_VEL = 5 # the speed with which either of the paddle moves

# initialize score variables score1 and score2
score1 = 0
score2 = 0

# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    
    # ball position
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    
    # horizontal velocity
    ball_vel[0] = -random.randrange(120, 240) / 100
    if direction == RIGHT:
        ball_vel[0] *= -1
        
    # vertical velocity
    ball_vel[1] = -random.randrange(60, 180) / 100


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    
    # set/reset the scores
    score1 = 0
    score2 = 0
    
    # set/reset the paddle positions
    paddle1_pos = HEIGHT / 2
    paddle2_pos = HEIGHT / 2
    
    # set/reset the ball
    direction = ball_vel[0] > 0
    spawn_ball(direction)

def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
        
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    if ball_pos[0] >= WIDTH - BALL_RADIUS - PAD_WIDTH or ball_pos[0] <= BALL_RADIUS + PAD_WIDTH: 
        # ball goes to side
        if paddle1_pos < ball_pos[1] < paddle1_pos + PAD_HEIGHT and ball_vel[0] < 0: # ball bounces from paddle1
            ball_vel[0] *= -1.1 # 10% increase in the velocity
            ball_vel[1] *= 1.1
        elif paddle2_pos < ball_pos[1] < paddle2_pos + PAD_HEIGHT and ball_vel[0] > 0: # ball bounces from paddle2
            ball_vel[0] *= -1.1 # 10% increase in the velocity
            ball_vel[1] *= 1.1
        else:
            if ball_vel[0] > 0: # ball falls in right gutter
                score1 += 1
            else:               # ball falls in left gutter
                score2 += 1  
            direction = ball_vel[0] < 0
            spawn_ball(direction) # start the ball from the center when falls in gutter
                
    if ball_pos[1] >= HEIGHT - BALL_RADIUS or ball_pos[1] <= BALL_RADIUS: # ball goes to bottom/top
        ball_vel[1] = -ball_vel[1]
            
    # draw ball
    c.draw_circle(ball_pos, BALL_RADIUS, 2, 'White', 'White')
            
    # update paddle's vertical position, keep paddle on the screen
    if (paddle1_pos <= HEIGHT - PAD_HEIGHT and paddle1_vel > 0) or (paddle1_pos >= 0 and paddle1_vel < 0):
        paddle1_pos += paddle1_vel
        
    elif (paddle2_pos <= HEIGHT - PAD_HEIGHT and paddle2_vel > 0) or (paddle2_pos >= 0 and paddle2_vel < 0):
        paddle2_pos += paddle2_vel
            
    # draw paddles
    c.draw_polygon([[0, paddle1_pos], [PAD_WIDTH, paddle1_pos], [PAD_WIDTH, paddle1_pos + PAD_HEIGHT ], [0, paddle1_pos + PAD_HEIGHT]], 1, 'White', 'White') 
    c.draw_polygon([[WIDTH, paddle2_pos], [WIDTH - PAD_WIDTH, paddle2_pos], [WIDTH - PAD_WIDTH, paddle2_pos + PAD_HEIGHT], [WIDTH, paddle2_pos + PAD_HEIGHT]], 1, 'White', 'White')
            
    # draw scores
    c.draw_text(str(score1), [40, 50], 30, 'White')    
    c.draw_text(str(score2), [WIDTH - 80, 50], 30, 'White')
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel = PADDLE_VEL
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel = -PADDLE_VEL    
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = -PADDLE_VEL
    if key == simplegui.KEY_MAP['s']:
        paddle1_vel = PADDLE_VEL
      
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP['down']:         
       paddle2_vel = 0
    if key == simplegui.KEY_MAP['up']:
       paddle2_vel = 0    
    if key == simplegui.KEY_MAP['w']: 
       paddle1_vel = 0
    if key == simplegui.KEY_MAP['s']:
       paddle1_vel = 0
    

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

# adding restart button to start a new game
frame.add_button("Restart", new_game, 100)

# start frame
new_game()
frame.start()
