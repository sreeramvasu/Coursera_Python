# Mini-project #7 - Full rice rocks game
# Author: SV
# Mailto: sreeram.vasudevan@gmail.com

import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5

# game over message
over_message = 'NEW GAME'

# some globals for number of rocks
# the number of rocks at any time should not exceed 30
MAX_ROCKS = 30   

# this is to ensure that rocks are not too close to the ship so that we dont lose lives early :)
ROCK_SHIP_DISTANCE = 100
# to tell how long a missile will be available
MISSILE_AGE = 60
# here explosion age is 23 because the explosion image is 1 X 24 grid
EXPLOSION_AGE = 23

# to check the progress of the game
is_started = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2013.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        if is_started:
            if not self.thrust:
                canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
            else:
                canvas.draw_image(self.image, (self.image_center[0] + self.image_size[0], self.image_center[1]), self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        # updating the angular velocity
        self.angle += self.angle_vel
        
        # updating the position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        # updating the velocity
        if self.thrust:
            acceleration = angle_to_vector(self.angle)
            self.vel[0] += acceleration[0] * 0.1
            self.vel[1] += acceleration[1] * 0.1
        else:
            self.vel[0] *= 0.99
            self.vel[1] *= 0.99
            
    def shoot(self):
        ''' This method governs the firing behaviour of the ship '''
        # we create missile when space is pressed. The velocity is kept to be 6 times the forward of the ship
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
        a_missile = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)                
    
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound and is_started:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
               
        if is_started:  
            if self.animated == True:  # Have set animated true only for explosion
                # draw the explosion image                
                explosion_dim = [24, 1]  # the explosion image is defined in a 24 X 1 grid
                # we set the age of the explosion image
                explosion_index = [self.age % explosion_dim[0], (self.age // explosion_dim[0]) % explosion_dim[1]]
                canvas.draw_image(explosion_image, [self.image_center[0] + explosion_index[0] * self.image_size[0], 
                     self.image_center[1] + explosion_index[1] * self.image_size[1]], 
                     self.image_size, self.pos, self.image_size)
                
            else:  
                # draw the normal sprite - bullet, asteroid
                canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)                
    
    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]      
        
        # update age
        self.age += 1
        
    def is_colliding(self, another):
        # finding collision between two objects
        # if distance between the position of two objects is less than the sum of radii, then it is colliding
        return dist(self.pos, another.pos) <= self.radius + another.radius

           
def draw(canvas):
    global time, is_started, lives, rock_group, missile_group, exploded_group, over_message
    
    # animate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # drawing the lives and scores
    canvas.draw_text('Lives', (50, 50), 25, 'White', 'sans-serif')
    canvas.draw_text(str(lives), (150, 50), 25, 'White', 'sans-serif')
    canvas.draw_text('Score', (650, 50), 25, 'White', 'sans-serif')
    canvas.draw_text(str(score), (750, 50), 25, 'White', 'sans-serif')    
    
    # draw ship and sprites
    # drawing ship
    my_ship.draw(canvas)
    
       
    # drawing rock and updating them
    sprite_processor(rock_group, canvas)
    
    # drawing missile and updating them
    sprite_processor(missile_group, canvas)
    
    # drawing explosions and updating them
    sprite_processor(exploded_group, canvas)
    
    if collide(rock_group, my_ship):
        lives -= 1
        if lives == 0:
            over_message = 'GAME OVER'
            is_started = False
            rock_group = set([])
            missile_group = set([])
            exploded_group = set([])
            my_ship.pos = [WIDTH / 2, HEIGHT / 2]
            my_ship.vel = [0, 0]
            soundtrack.pause()
            
    group_collide(rock_group, missile_group)
    
    # update ship 
    my_ship.update()
        
    # draw splash screen if not started
    if not is_started:       
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], splash_info.get_size())
        canvas.draw_text(over_message, (300, 50), 40, 'White', 'sans-serif')
            

# timer handler that spawns a rock    
def rock_spawner():
    global rock_group
    
    if len(rock_group) < MAX_ROCKS and is_started:
        rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
                
        while dist(rock_pos, my_ship.pos) < ROCK_SHIP_DISTANCE:
            rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]        
    
        rock_vel = [random.random() * 0.7 - 0.3, random.random() * 0.7 - 0.3]
        rock_angle_vel = random.random() * 0.2 - 0.1
        
        a_rock = Sprite(rock_pos, rock_vel, 0, rock_angle_vel, asteroid_image, asteroid_info)
        rock_group.add(a_rock)
        
# processing sprites - Rocks, Explosions and missiles
def sprite_processor(sprite_group, canvas):   
    # to update a sprite and draw a sprite
    
    # remove expired missiles from missile_group
    for missile in missile_group:
        if missile.age > MISSILE_AGE:
            missile_group.remove(missile)
            
    # remove expired explosions from explosion_group
    for exploded in exploded_group:
        if exploded.age > EXPLOSION_AGE:
            exploded_group.remove(exploded)      
            
    for sprite in sprite_group:
        sprite.update()
        sprite.draw(canvas)
    
# object - group collision
def collide(group, obj_collide):
    # we check if an object(ship, missile, rock) collide with group(rock group)
    global exploded_group   
    return_value = False
    
    for obj in group:
        if obj.is_colliding(obj_collide):
            group.remove(obj)
            return_value = True
            a_explode = Sprite(obj.pos, (0,0), 0, 0, explosion_image, explosion_info, explosion_sound)
            exploded_group.add(a_explode)
            
    return return_value

# group - group collision
def group_collide(group_a, group_b):
    # to check if two of the groups are colliding or not
    
    global score
    count = 0        
    for obj_b in group_b:
        if collide(group_a, obj_b):
            count += 1
            group_b.remove(obj_b)
    
    score += count
    
# key handlers to control ship   
def keydown(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.angle_vel -= 0.05
    
    if key == simplegui.KEY_MAP['right']:
        my_ship.angle_vel += 0.05
    
    if key == simplegui.KEY_MAP['up']:
        my_ship.thrust = True
        if is_started:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
    
    if key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
        
        
def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.angle_vel += 0.05
        
    if key == simplegui.KEY_MAP['right']:
        my_ship.angle_vel -= 0.05
        
    elif key == simplegui.KEY_MAP['up']:
        my_ship.thrust = False
        ship_thrust_sound.pause()
        

# mouse handler for splash screen
def click(pos):
    global is_started, score, lives
    
    lives, score = 3, 0   # initial reset
    center = [ WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    if not is_started: 
        is_started = True
        soundtrack.rewind()
        soundtrack.play()
        
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

# initializing the groups for rocks, missiles and explosions
rock_group = set([])
missile_group = set([])
exploded_group = set([])

# register handlers
frame.set_draw_handler(draw)

# key and mouse handlers
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
