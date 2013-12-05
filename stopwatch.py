# "Stopwatch: The Game"
# Author: SV
# mailto: sreeram.vasudevan@gmail.com

import simplegui
import time
import math

# define global variables
message = "0:00.0"
isRunning = False
success_reflex = 0
total_reflex = 0
tick = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):    
    t_str = str(t)
    
    # computing milliseconds
    deciseconds = t_str[-1]
    
    # computing seconds
    seconds = str(int(math.floor((t % 600) / 10)))
    if int(seconds) < 10:
        seconds = "0" + seconds
    elif int(seconds) >= 10 and int(seconds) < 60:
        pass
    else:
        seconds = "00"
        
    # computing minutes - after 10 minutes we reset the stopwatch
    minutes = str(int(math.floor(t / 600)))
    if int(minutes) > 10:
        minutes = "0"
    
    time_str = minutes + ":" + seconds + "." + deciseconds    
    return time_str
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global isRunning
    isRunning = True    
    timer.start()

def stop():
    global isRunning, message, success_reflex, total_reflex
    if isRunning == True:
      total_reflex += 1
      if message[-1] == '0':
          success_reflex += 1
    isRunning = False    
    timer.stop()
    
def reset():
    global success_reflex, total_reflex, message, tick, isRunning
    if isRunning == True:
        timer.stop()
        isRunning = False
    
    success_reflex = 0
    total_reflex = 0
    tick = 0
    message = format(tick)
    
# define event handler for timer with 0.1 sec interval
def time():
    global tick, message
    tick += 1
    message = format(tick)    
    
timer = simplegui.create_timer(100, time)

# define draw handler
def draw(canvas):
    canvas.draw_text(message, (75,110), 50, "White", "sans-serif")
    canvas.draw_text(str(success_reflex) + "/" + str(total_reflex), 
                     (250, 40), 25, "Green", "sans-serif")   
    
# create frame
sw_frame = simplegui.create_frame("Stopwatch: The Game", 300, 200)

# register event handlers
sw_frame.add_button("Start", start, 100)
sw_frame.add_button("Stop", stop, 100)
sw_frame.add_button("Reset", reset, 100)
sw_frame.set_draw_handler(draw)

# start frame
sw_frame.start()

# Please remember to review the grading rubric
