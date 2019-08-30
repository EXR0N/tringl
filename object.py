'''
module for the classes that handle the things in the game

started 15 October 2018 ish by Exr0n

'''

import time, math, pygame
import contact # contact.py from current directory
start_time = time.time()

game_state = 0
game_objects = []


player = None
"""
def __init__(window=None, blockSize=None, objects=None, player_start=None):
    '''Set global vars so all the classes and stuff can use them.
    This function should be called in main.py, or wherever this module is going to be imported to.'''
    if window:
        global game_window
        game_window = window

    if blockSize:
        global block_size, term_vel
        block_size = blockSize
        term_vel = int(blockSize/2 -2) # terminal velocity, not more that half block size because if it were then it may be possible to glitch through blocks

    if objects:
        global game_objects
        game_objects = objects

    if player_start:
        global player, camera_x, camera_y
        player = player_start
        camera_x = -player_start.posx + block_size * 6.5
        camera_y = -player_start.posy + block_size * 4.5

    # NTFS: $game_state is probably not going to be used, its just here just in case. Try not to use it in any classes or methods or things for easy removal in the future.
    #global game_state
    #game_state = 0
"""


class Object:
    '''Anything that can be collided within the game.'''
    def __init__(self, type, game, level, posx, posy, clr):
        self.type = type
        # super-instances
        self.game = game
        self.level = level
        # position/velocity variables
        self.posx = posx # x position
        self.posy = posy # y position
        self.velx = 0
        self.vely = 0
        self.newx = posx
        self.newy = posy

        if not clr: clr=(0, 0, 70) # we need this here and not in the args part because in the args part it dosent make it the value if the value is passed by the call as None
        self.color = clr # rgb

        self.block_size = self.game.block_size

    def draw(self):
        '''Draw a rectangle based on the position and size vars, and then attach a sprite to it.'''
        # TODO: make this thingy attach a sprite to stuff, because right now everything is just a red rectangle
        dx = self.posx + self.level.camera_x; dy = self.posy + self.level.camera_y # draw_x, draw_y
        pygame.draw.rect(self.game.win, self.color, (dx, dy, self.block_size, self.block_size))

    def __repr__(self):
        return f'({self.posx}, {self.posy})'

    def __str__(self):
        return self.__repr__()

    def __getitem__(self, key):
        return [self.posx, self.posy][key]



class Newton(Object):
    '''Anything that can, and is affected by gravity.'''

    def __init__(self, type, game, level, posx, posy, color=(0, 200, 0)):
        super().__init__(type, game, level, posx, posy, color)

    def apply_gravity(self):
        '''Apply gravity to $self.velocity'''
        self.vely += 4 #if self.vely == 0 else math.ceil(0.25 * abs(self.vely))

    def apply_velocity(self):
        '''Do all the velocity calcs then with that change $self.posx and $self.posy'''
        term_vel = self.game.term_vel

        def valid_pos(self, vect, objc):
            '''Move the object to a valid place, somewhere not inside another object'''
            if vect == 1: # top
                self.vely += objc.posy + self.block_size - self.posy +1
            if vect == 2: # right
                self.velx += objc.posx - self.block_size - self.posx -1
            if vect == 3: # bottom
                self.vely += objc.posy - self.block_size - self.posy
            if vect == 4: # left
                self.velx += objc.posx + self.block_size - self.posx +1

        self.apply_gravity()

        # terminal velocity
        if self.velx >  term_vel: self.velx =  term_vel
        if self.velx < -term_vel: self.velx = -term_vel
        if self.vely >  term_vel: self.vely =  term_vel
        if self.vely < -term_vel: self.vely = -term_vel

        # update the new position
        self.newx = self.posx + self.velx
        self.newy = self.posy + self.vely

        # collisions (this changes self.newx and self.newy)
        #self = contact.algebra_magic(self, self.level.objects)
        self = contact.bumbo_cactoni(self, self.level.objects)

        # change the actual position
        self.posx = self.newx
        self.posy = self.newy
        ''' this is now handled by the collision engine, but the commented code goes with contact.algebra_magic()
        self.posx += self.velx
        self.posy += self.vely
        '''

        if self.on_ground:
            self.velx = int(self.velx * 0.2) # friction with the ground
        else: self.velx = int(self.velx * 0.95); self.vely = int(self.vely * 0.9)

    def motion_lines(self): # TODO: make this work
        bs = self.game.block_size
        line_start_scale = int(bs/2 + 5)
        line_len_scale = 1.2
        center_x = int(self.newx + bs/2)
        center_y = int(self.newy + bs/2)

        start_x = int(center_x - (self.velx - (abs(self.velx)-1))*line_start_scale) # the positive/negative part of the velocity multiplied by the scale factor
        start_y = int(center_y - (self.vely - (abs(self.vely)-1))*line_start_scale)

        end_x = int(start_x - self.velx * line_len_scale)
        end_y = int(start_y - self.vely * line_len_scale)

        start_x += self.level.camera_x; end_x += self.level.camera_x
        start_y += self.level.camera_y; end_y += self.level.camera_y

        pygame.draw.line(self.game.win, (0, 0, 0), (start_x, start_y), (end_x, end_y))

    def draw(self):

        self.apply_velocity()
        #self.valid_pos() # this function already called in self.apply_velocity()
        #self.motion_lines()
        super().draw()


class Player(Newton):
    '''The player.'''
    # player static variables
    league_stats = {
        "basic": {"sped": 16, "jump": 31, "rang": 0, "atck": 0, "body": 0},
        "rouge": {"sped": 0, "jump": 0, "rang": 0, "atck": 0, "body": 0},
        "boost": {"sped": 0, "jump": 0, "rang": 0, "atck": 0, "body": 0},
        "witch": {"sped": 0, "jump": 0, "rang": 0, "atck": 0, "body": 0},
        "fight": {"sped": 0, "jump": 0, "rang": 0, "atck": 0, "body": 0},
        "armor": {"sped": 0, "jump": 0, "rang": 0, "atck": 0, "body": 0}}
    empty_stats= {"sped": 0, "jump": 0, "rang": 0, "atck": 0, "body": 0}
    stat_upgrade_modifier = {"sped": 0, "jump": 0, "rang": 0, "atck": 0, "body": 0} # each level does this amount for stats

    def __init__(self, game, level, posx, posy, league, upgd=empty_stats, color=(146, 149, 176)):
        super().__init__("player", game, level, posx, posy, color)

        self.league = league # todo: could look for a better name rather than league, class, or type
        self.upgd = upgd # what upgrades we have

        self.stat = self.apply_upgrades(self.league, self.upgd)
        self.on_ground = False
        self.jump = 0 # currently trying to jump?

    def apply_upgrades(self, league, upgd):
        '''Change the stats of the player based on the $upgd arg and class, basicly apply upgrades'''
        end = self.league_stats[league]
        for (key, val) in upgd.items():
            end[key] += self.stat_upgrade_modifier[key] * val
        return end

    def move_left(self):
        self.velx -= self.stat["sped"]-abs(self.velx) # see below

    def move_right(self):
        self.velx += self.stat["sped"]-abs(self.velx) # dont increase speed past self.stat["sped"]

    def try_jump(self):
        if self.on_ground:
            self.jump = 3

    def draw(self):
        '''Overwrite of the Newton draw to add jumping detection, etc'''
        print('')
        # jump
        if self.jump:
            self.vely -= self.stat["jump"]-abs(self.vely) # same as the move functions
            self.jump -= 1

        super().draw()

print(f'Imported objects.py in {time.time()-start_time} seconds.')
