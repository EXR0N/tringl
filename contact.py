'''
module for collisions

started 19 October 2018 by Exr0n

        _____                     _____
       /     \                   /     \
      /   ___/                  /   /~\_\
     /   /         HELP!!      /   /
    /    \          \         /    \
~~~~~~~~~~~~~~~~~~~lol~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~()~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~/\~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

^^^ inspirational quotes w/ Exr0n:
    keep swimming, keep coding, or you will be dropped in the middle of the ocean.

'''
import math

def bumbo_cactoni(self, objcs):
    ''' super simple version on collision ispired by https://www.khanacademy.org/computer-programming/platformer-v2/6739704993808384 and will make Exr0n rage quit if it works'''
    print('bumbo has awoken')
    bs = self.game.block_size
    def find_phases(self, objcs):
        '''Create the phases in which collisions will be calculated'''
        s = (math.floor((self.newx+bs/2)/bs), math.floor((self.newy+bs/2)/bs))
        phases = [[], []]
        for objc in objcs:
            if not objc == self:
                o = (objc.newx/bs, objc.newy/bs)
                if objc.type == "block": objc.color = (0, 0, 50)
                if   (o[0] == s[0] +1 and o[1] == s[1]): # o right of s
                    phases[0].append((objc, -2))
                elif (o[0] == s[0] -1 and o[1] == s[1]): # o left of s
                    phases[0].append((objc, -4))
                elif (o[1] == s[1] +1 and o[0] == s[0]): # o top of s
                    phases[0].append((objc, -3))
                elif (o[1] == s[1] -1 and o[0] == s[0]): # o bot of s
                    phases[0].append((objc, -1)) # < zero means right next to

                elif (o[0] == s[0] -1 and o[1] == s[1] -1): # o NW of s
                    phases[1].append((objc, 4)) # 4 means to the NW of body
                elif (o[0] == s[0] +1 and o[1] == s[1] -1): # o NE of s
                    phases[1].append((objc, 1)) # 1 means to the NE of body
                elif (o[0] == s[0] +1 and o[1] == s[1] +1): # o SE of s
                    phases[1].append((objc, 2)) # 2 means to the SE of body
                elif (o[0] == s[0] -1 and o[1] == s[1] +1): # o SW of s
                    phases[1].append((objc, 3)) # 3 means to the SW of body
        #phases = phases[0] if phases[0] else phases[1] # this old: breaks if we are clipping a corner... specific cases.
        phases = phases[0] + phases[1] # so the ones from phases 1 will always be first
        return phases

    def find_contact(body, contc):
        '''Find the places things are touching eachother'''
        def overlap(body, objc):
            '''Is self overlapping with objc?'''
            my_corners = [(body.newx, body.newy), (body.newx+bs, body.newy), (body.newx, body.newy+bs), (body.newx+bs, body.newy+bs)]
            for point in my_corners:
                if(((point[0] > objc.posx and point[0] < objc.posx + bs) or body.newx == objc.newx) and # the point[0]/point[1] == objc.new(smtn) is not very good.
                   ((point[1] > objc.posy and point[1] < objc.posy + bs) or body.newy == objc.newy)): return point
            return False # if none of the above

        contacts = []
        p = overlap(body, contc[0])
        if p:
            print('Contact with:', str(contc+(p,)))
            return contc + (p,) # add $objc to contacts
        else: return None

    def super_special_magic_with_math_this_time(self, contc):
        '''Figure out the direction and run valid_pos on it.

            contact directions:

                    4           -1            1
                     \           ^            /
                       ,-------------------,
                       |                   |
                       |      block        |
                       |     occupied      |
                  -4 < |      by the       | > -2
                       |      player       |
                       |                   |
                       |___________________|

                     /           v           \
                    3           -3            2


        '''
        (objc, dirc, point) = contc
        if objc.type == "block": objc.color = (140, 0, 0) # debug
        if dirc == -1:
            self.vely = 0
            self.newy = objc.newy + bs
        elif dirc == -2:
            self.velx = 0
            self.newx = objc.newx - bs
        elif dirc == -3:
            self.vely = 0
            self.newy = objc.newy - bs
            self.on_ground = True
        elif dirc == -4:
            self.velx = 0
            self.newx = objc.newx + bs
        else:
            # here we solve a linear equation to figure out where we are coliding
            slope = point[1]/point[0] # get the slope of a line that represents our trajectory

            y_ax = slope * (objc[0]-point[0])
            # imagine drawing a line of slope $slope through $point. y_ax is the y pos of the point
            #   where the line intersects the left edge of the block we are colliding with
            #   (or rather where it would if the left edge of the block extended infinetly up and down)
            # it seems the issue is something about not controlling for which point we draw the line too and/or
            # which point on the objc we are testing for. although that doesnt really make sense because we are
            # testing it with a line defined by a point that we know enters the objc...

            # y = m * x + b
            # but we do know that slope represents m, and that the differnce between the x of the block and the x of the contacting point is what we define to be

            if y_ax > objc.posy and y_ax < objc.posy + bs: # collide on the side
                if dirc in [1, 2]: # hit player right
                    self.velx = 0
                    self.newx = objc.newx - bs
                else: # hit player left
                    self.velx = 0
                    self.newx = objc.newx + bs
            else: # <------------------    if not the side, meaning if top down
                if dirc in [1, 4]: # hit ceiling
                    self.vely = 0
                    self.newy = objc.newy + bs
                else: # hit floor
                    self.vely = 0
                    self.newy = objc.newy - bs
                    self.on_ground = True


        return self

    self.on_ground = False
    phases = find_phases(self, objcs)

    for thingy in phases:
        if thingy[0].type == "block": thingy[0].color = (0, 0, 120) # debug

    if phases: # if there are things around the player
        print(self.velx, self.vely)
        # for contc in phases: self = single_correct(self, contc) # old

        for contc in phases:
            (objc, dirc) = contc
            print(self)
            contc = find_contact(self, contc)
            if contc:
                if (self.type == "player"): # check for player action blocks
                    if   objc.type == "goal": self.level.win()
                    elif objc.type == "spike": self.level.die()
                self = super_special_magic_with_math_this_time(self, contc)
            '''# unintuitive but working way to check if overlap from the new place link above thingy (khan)
            if (self.newy + bs > objc.newy      and # self bottom is below other top
                self.newy      < objc.newy + bs and # self top is above other bottom
                self.newx + bs > objc.newx      and # self right past other left
                self.newx      < objc.newx + bs  ): # self left past other right
                # check player specific blocks
                if (self.type == "player"):
                    if   objc.type == "goal": self.level.win()
                    elif objc.type == "spike": self.level.die()

                dirc = super_special_magic_with_math_this_time(self, contc)
                if self.vely < 0: # hit bottom of block
                    self.vely = 0
                    self.newy = objc.newy + bs
                elif self.vely > 0: # hit top of block
                    self.vely = 0
                    self.newy = objc.newy - bs
                    self.on_ground = True

                elif self.velx < 0: # hit right of block
                    self.velx = 0
                    self.newx = objc.newx + bs
                elif self.velx > 0: # hit left of block
                    self.velx = 0
                    self.newx = objc.newx - bs
'''
    return self



























def algebra_magic(self, objcs):
    bs = self.game.block_size
    def find_phases(self, objcs):
        '''Create the phases in which collisions will be calculated'''
        s = (math.floor((self.newx+bs/2)/bs), math.floor((self.newy+bs/2)/bs))
        phases = [[], []]
        for objc in objcs:
            if not objc == self:
                o = (objc.newx/bs, objc.newy/bs)
                if objc.type == "block": objc.color = (0, 0, 50)
                if   (o[0] == s[0] +1 and o[1] == s[1]): # o right of s
                    phases[0].append((objc, -2))
                elif (o[0] == s[0] -1 and o[1] == s[1]): # o left of s
                    phases[0].append((objc, -4))
                elif (o[1] == s[1] +1 and o[0] == s[0]): # o top of s
                    phases[0].append((objc, -3))
                elif (o[1] == s[1] -1 and o[0] == s[0]): # o bot of s
                    phases[0].append((objc, -1)) # < zero means right next to

                elif (o[0] == s[0] -1 and o[1] == s[1] -1): # o NW of s
                    phases[1].append((objc, 4)) # 4 means to the NW of body
                elif (o[0] == s[0] +1 and o[1] == s[1] -1): # o NE of s
                    phases[1].append((objc, 1)) # 1 means to the NE of body
                elif (o[0] == s[0] +1 and o[1] == s[1] +1): # o SE of s
                    phases[1].append((objc, 2)) # 2 means to the SE of body
                elif (o[0] == s[0] -1 and o[1] == s[1] +1): # o SW of s
                    phases[1].append((objc, 3)) # 3 means to the SW of body
        #phases = phases[0] if phases[0] else phases[1] # this old: breaks if we are clipping a corner... specific cases.
        phases = phases[0] + phases[1] # so the ones from phases 1 will always be first
        return phases

    def find_contact(body, contc):
        '''Find the places things are touching eachother'''
        def overlap(body, objc):
            '''Is self overlapping with objc?'''
            my_corners = [(body.newx, body.newy), (body.newx+bs, body.newy), (body.newx, body.newy+bs), (body.newx+bs, body.newy+bs)]
            for point in my_corners:
                if(((point[0] > objc.posx and point[0] < objc.posx + bs) or body.newx == objc.newx) and # the point[0]/point[1] == objc.new(smtn) is not very good.
                   ((point[1] > objc.posy and point[1] < objc.posy + bs) or body.newy == objc.newy)): return point
            return False # if none of the above

        contacts = []
        p = overlap(body, contc[0])
        if p:
            print('Contact with:', str(contc+(p,)))
            return contc + (p,) # add $objc to contacts
        else: return None

    def super_special_magic_with_math_this_time(self, contc):
        '''
            Figure out the direction and run valid_pos on it.

            contact directions:

                    4           -1            1
                     \           ^            /
                       ,-------------------,
                       |                   |
                       |      block        |
                       |     occupied      |
                  -4 < |      by the       | > -2
                       |      player       |
                       |                   |
                       |___________________|

                     /           v           \
                    3           -3            2
        '''
        (objc, dirc, point) = contc
        if objc.type == "block": objc.color = (140, 0, 0) # debug
        if dirc < 0:
            return -dirc
        else:
            slope = point[1]/point[0]

            def find_direction(body, contact, block):
                '''Return a contact side, given the body, the objc, the body corner, and the objc corner'''
                (objc, d, point) = contact

                y_ax = slope * (block[0]-point[0])
                #x_ax = (block[1]-point[1]) / slope

                if y_ax > objc.posy and y_ax < objc.posy + bs: # collide on the side
                    return 2 if d in [1, 2] else 4
                else:
                    return 1 if d in [1, 4] else 3 # if not the side, meaning if top down

            '''if dirc == 1:
                blox = objc.posx
                bloy = objc.posy + bs
            if dirc == 2:
                blox = objc.posx
                bloy = objc.posy
            if dirc == 3:
                blox = objc.posx + bs
                bloy = objc.posy
            if dirc == 4:
                blox = objc.posx + bs
                bloy = objc.posy + bs'''
            return find_direction(self, contc, objc)

    def valid_pos(self, vect, objc):
        '''Move the object to a valid place, somewhere not inside another object'''
        # TODO: fix this (scaling)
        if vect == 1: # top
            #scale = self.vely
            self.vely += objc.newy + bs - self.newy #+1
            #scale = self.vely / scale
            #self.velx *= scale
        if vect == 2: # right
            #scale = self.velx
            self.velx += objc.newx - bs - self.newx #-1
            #scale = self.velx / scale
            #self.vely *= scale
        if vect == 3: # bottom
            #scale = self.vely
            self.vely += objc.newy - bs - self.newy
            #scale = self.vely / scale
            #self.velx *= scale

            self.on_ground = True
        if vect == 4: # left
            #scale = self.velx
            self.velx += objc.newx + bs - self.newx #+1
            #scale = self.velx / scale
            #self.vely *= scale
        print(self.velx, self.vely)
        return self

    def single_correct(self, calc): # calc is a single thing from find_phases
        '''Correct for one contact'''
        self.newx = self.posx + self.velx; self.newy = self.posy + self.vely
        contc = find_contact(self, calc)
        if contc: # if we are contacting this thing
            # check player specific blocks
            if (self.type == "player"):
                if   calc[0].type == "goal": self.level.win()
                elif calc[0].type == "spike": self.level.die()

            dirc = super_special_magic_with_math_this_time(self, contc)
            self = valid_pos(self, dirc, contc[0])
        return self

    self.on_ground = False
    phases = find_phases(self, objcs)

    for thingy in phases:
        if thingy[0].type == "block": thingy[0].color = (0, 0, 120) # debug

    if phases:
        print(self.velx, self.vely)
        for contc in phases:
            #temp_s += str(thingy)
            self = single_correct(self, contc)
    return self



print('')
