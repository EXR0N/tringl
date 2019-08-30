'''
<game name> by Minecire and Exr0n
dev started Oct 14, 2018
to date: code by Exr0n

******** LAST UPDATED 11 nov 2018 ********

practices:
    Here are Exr0n's python coding practices, which he uses in this code. Understanding them will make reading the code easier (hopefully):
    comments:
        a one line comment (#) directly followed by stuff is a code comment
        on the other hand, if its followed by space, its probably a human reading comment

        "TODO:" (to do) marks a work in progress, something that needs to be done
        "OBTW:" (oh by the way) marks an important note, like a comment that affects the whole file or program
        "NTFS:" (note to future self) marks a note to anyone who will develop this code, also quite important

    variables:
        var names are kinda important, and how they are named often tells you something about their use

        a good rule of thumb is that the longer the name, the more important it is or the larger it's scope
        global variables are almost always fully spelled out, with underscores if it is multiple words
        if a variable is fully spelled out, it is probably quite important or central to an important part of the code

        in comments and docstrings, a "$" is used to denote the next thing is a variable name to reduce confusion

        "fli" is often used as the generic counter or storage var in for loops.
        Lateley, I have not used this as much, but it used to be quite prevelent, and I might go back to it if I get lazy
        Also, if there are nested for loops, and I used $fli, then i will probably start using $flj and $flk and so on
        "tvar0" is often used as a variable name for something that is really just there temporarily. Again, I dont use this
        as much anymore but still good to know about


resources: (these are things that we are going to want to come back to, so we save them here for now. Really just a paste bin, for important-ish things for future reference)
    pygame starter:
    https://www.youtube.com/watch?v=i6xMBig-pP4
    use as computer app?
    https://www.reddit.com/r/pygame/comments/3er80c/distributing_packaging_a_pygame_game/


'''
def read_data():
    '''Read level data from the ./levels directory'''
    from os import walk
    (_, dirs, _0) = next(walk('levels'))
    #^ and    ^ means we arent using them and no-one else should cuz they private
    all_data = ["start_buffer"]
    for dirname in sorted(dirs):
        with open(f'levels/{dirname}/data.txt') as map:
            print(map)
            all_data.append(eval(map.read())) # note ntfs this could screw up cuz eval
    return all_data + ["end_buffer"]



field = ["start_buffer",
        {'player':[(0,1)], 'goal':[(15,2),(15,1),(15,0)], 'ground':[(6,3),(4,5),(5,3),(5,4),(4,4),(4,3),(3,3),(3,7),(3,6),(3,5),(3,4),(2,4),(2,3),(1,3),(9,6),(9,7),(12,4),(13,4),(13,5),(14,4),(14,5),(14,6),(15,4),(15,5),(15,6),(15,7),(15,8),(9,2),(9,1),(9,0),(9,-3),(9,-1),(9,-2),(0,2),(1,2),(2,2),(3,2),(4,2),(5,2),(6,2),(15,3),(13,3),(12,3),(9,5),(14,3)]},
        {'player':[(4,8)], 'goal':[(6,0),(13,1)], 'ground':[(0,7),(0,8),(0,9),(0,10),(0,11),(1,3),(1,4),(1,5),(1,6),(1,7),(1,10),(1,11),(3,11),(4,6),(4,11),(5,6),(5,11),(6,4),(6,6),(6,11),(7,6),(7,11),(8,4),(8,5),(8,6),(8,9),(8,10),(11,6),(11,9),(12,9),(13,9),(14,8),(15,7)]},
        {'player':[(0,4)], 'goal':[(15,3),(15,4),(15,5),(15,6)], 'ground':[(0,6),(0,7),(0,8),(0,9),(0,10),(1,6),(1,7),(1,8),(2,6),(2,7),(8,8),(8,9),(9,8),(9,9),(10,8),(10,9),(11,8),(11,9),(12,8),(12,9),(12,10),(13,8),(13,9),(13,10),(14,8),(14,9),(14,10),(15,8),(15,9),(15,10),(15,11)]},
        "end_buffer"]

field = read_data()
print(field)

block_size = 64
screen_size = (14, 10)
size = (screen_size[0]*block_size, screen_size[1]*block_size)
framerate = 6


import pygame, time, math
#import importlib as imp

from sys import path as a; from os import path; a.append(path.dirname(__file__)); del a, path # add the absolute path of this file to sys.path
import object

clock = pygame.time.Clock()
pygame.init()
win = pygame.display.set_mode(size) # init a window with a size
pygame.display.set_caption("Window Title!") # set the window title

class Level:
    '''Construct and run a level.'''
    def __init__(self, game, map):
        self.game = game
        self.map = map
        self.state = 0 # 0 = initing, 1 = running, 2 = win
        self.generate_level()

    def win(self):
        self.do_animation('win')
        self.state = 2

    def die(self):
        self.do_animation('death')

    def do_animation(self, type):
        if   type == 'death':
            self.game.win.fill( (255, 100, 100) )
            (self.player.posx, self.player.posy) = self.map['player'][0] # reset the player position
            self.player.posx *= block_size; self.player.posy *= block_size # do the scaling
            #self.set_cam_pos(self.player) # todo not used
            self.player.velx = 0; self.player.vely = 0 # reset velocity
            time.sleep(0.2)
        elif type == 'win':
            self.game.win.fill( (150, 180, 150) )
            pygame.display.update()

    def set_cam_pos(self, player):
        self.camera_x = (self.game.size[0]-block_size)/2-self.player.posx
        self.camera_y = (self.game.size[1]-block_size)/2-self.player.posy # reset camera pos

    def generate_level(self):
        '''From a level dict, generate the current level.'''
        def create_non_newton(self, pos, type, color=(0, 0, 50)):
            temp = object.Object(type, self.game, self, pos[0]*block_size, pos[1]*block_size, color) # make the item
            self.objects.append(temp) # add to appropriate lists
            if item_pos[1]*self.game.block_size > self.lowest_block: self.lowest_block = item_pos[1] * block_size # update the lowest item
            return self

        curr = self.map
        print(f'curr is equal to {curr}')
        # init vars
        self.objects = []
        self.newtons = []
        self.goals = [] # TODO: may not need this
        # TODO: make a function that draws an item given a position and a block type and then adds that item to the correct arrays. support for block, spike, goal
        # make player
        self.player = object.Player(self.game, self, curr["player"][0][0]*self.game.block_size, curr["player"][0][1]*self.game.block_size, "basic")
        self.objects.append(self.player); self.newtons.append(self.player)
        # draw all the blocks
        self.lowest_block = 0
        try:
            for item_pos in curr["ground"]: # create all the blocks
                self = create_non_newton(self, item_pos, "block", (0, 0, 50))
        except: pass
        try:
            for item_pos in curr["goal"]: # and then create the goals
                self = create_non_newton(self, item_pos, "goal", (0, 200, 0))
        except: pass
        try:
            for item_pos in curr["spike"]: # and then with the spikes
                self = create_non_newton(self, item_pos, "spike", (99, 13, 0))
        except: pass

        self.state = 1

    def outside_events(self):
        '''Handle events from pygame and also do keys, basicly read input from outside'''
        # listen for key presses
        k_down = pygame.key.get_pressed() # returns an array of all the keys, and at each index either a 1 or 0
        if k_down[pygame.K_LEFT]: # left arrow key
            self.player.move_left()
        if k_down[pygame.K_RIGHT]: # right arrow key
            self.player.move_right()
        if k_down[pygame.K_UP]: # up arrow key
            self.player.try_jump()
        if k_down[pygame.K_DOWN]:
            self.player.jump = 0
            self.player.vely = 0 if self.player.vely < 0 else self.player.vely
        if k_down[pygame.K_SPACE]:
            self.win()

        for event in pygame.event.get(): # pygame.event.get() returns a list for everything that a user might do, such as key presses, mouse, etc
            #print(event)
            if event.type == pygame.QUIT:
                print('Exit')
                self.game_state = 0
                exit()

    def step(self):
        self.game.win.fill( (105, 105, 105) ) # draw the background over everything

        self.outside_events() # handle outside events

        if self.player.posy > self.lowest_block + 5*block_size: # on death
            self.die()

        self.set_cam_pos(self.player)

        # draw everything
        for item in self.objects:
            # tvar0 = time.time()
            item.draw()

        # show cursor with a little circle
        pygame.draw.circle(self.game.win, (255, 255, 255), pygame.mouse.get_pos(), 5)

        pygame.display.update() # update the display OBTW: TODO: this function takes forever for some reason.

    def run(self):
        self.pause = False

        while self.state == 1:

            k_down = pygame.key.get_pressed()
            if k_down[pygame.K_x]:
                print('pause key pressed!')
                self.pause = not self.pause
                time.sleep(0.2)
            elif k_down[pygame.K_b]:
                print('manual step')
                self.step()
            del k_down
            #print(self.pause)

            if not self.pause:
                self.step() # do one frame
                clock.tick(framerate) # wait a bit


        return self.state


class Game:
    '''Holds a game TODO: write this better'''
    def __init__(self, window, levels, block_size=64, size=(14, 10), framerate=60, background=(105, 105, 105)):
        start_time = time.time()
        self.win = window
        self.levels = levels
        self.block_size = block_size
        self.term_vel = math.floor(block_size/2) -2
        self.width  = size[0]
        self.height = size[1]
        self.size = (self.width*block_size, self.height*block_size)
        self.background = background

        self.game_state = 0

        win.fill( self.background ) # background

        #object.__init__(win, block_size)
        # make the game

        self.init_game()

        while self.game_state:
            if type(field[self.game_state]) == type({}): # if it is a level
                self.current = Level(self, field[self.game_state])
                self.current.run()
            else:
                # else do a cutscene
                self.cutscene(field[self.game_state])
            self.game_state += 1

    def init_game(self):
        def start_screen(self):
            time.sleep(2)
            return self

        self = start_screen(self) # do the start screen

        self.game_state = 1 # start the game
        return self.game_state

    def cutscene(self, scene):
        if scene == "end_buffer":
            print('\n\n******** Yay, you won! ********\n')
            exit()
        else:
            pass # TODO: make cutscenes work

    def get_data(self):
        pass

game = Game(win, field, block_size=block_size, size=screen_size, framerate=framerate)
