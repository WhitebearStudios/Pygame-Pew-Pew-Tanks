#from main import tank_size
from game_object import *
from random import randint, random
from math import sin, cos, radians
import pygame

fire_col = (255, 200, 80)

#Tiny class for storing ground data
class ground_part:
    def __init__(self, pos, radius) -> None:
        self.coord = pos
        self.radius = radius

class tank(platformer):
    def __init__(self, player_num, start, img, img2, gravity_accel, start_health, num_players = 2):
        self.player_num = player_num
        self.face_right = self.player_num%2==1 and not player_num==num_players

        self.img = img
        self.img2 = img2
        self.x = start[0]
        self.y = start[1]
        self.aim = 0

        self.speed = 1
        self.aim_speed = 3
        self.accel = gravity_accel
        self.falling = True
        self.health = start_health
        self.smoke_counter = 0

        self.move = (0,0)
        self.move_gun = 0
        self.slope_angle = 0

        self.misses = 0
        self.got_hit = False

    def respawn(self, start):
        self.x = start[0]
        self.y = start[1]

    def display(self, barrel_size, gun_offset, game_display, ground_col, offset = (0, 0)):
        #Display tank's gun
        if self.face_right:
            pivot_point = (5, barrel_size[1]/2)
            my_offset = (self.x+gun_offset[0], self.y+gun_offset[1])
            ang = self.aim+self.slope_angle
        else:
            pivot_point = (barrel_size[0]-5, barrel_size[1]/2)
            my_offset = (self.x+20, self.y+gun_offset[1])
            ang = -self.aim+self.slope_angle

        gun_to_display, self.rotated_pos = rotate_img(self.img2, my_offset, pivot_point, ang)
        game_display.blit(gun_to_display, subtract_coords(self.rotated_pos, offset))

        #Display tank
        super().display(game_display, ground_col, offset)

    def update(self, barrel_size, gun_offset, game_display, ground_col, smoke_frequency, gun_rot, game_object_list, offset = (0, 0), update_collisions = True):
        #print("P"+str(self.player_num)+" Update: "+str(update_collisions))
        self.update_gun(gun_rot)
        super().update(game_display, ground_col, False, offset, update_collisions)
        self.display(barrel_size, gun_offset, game_display, ground_col, offset)

        if self.health<0:
            #Slowly puff smoke
            self.smoke_counter+=1
            if self.smoke_counter>=smoke_frequency:
                self.smoke_counter = 0
                spawn_floaty_smoke(self.get_center()[0], self.get_center()[1], game_object_list)

    def update_gun(self, gun_rot):
        self.aim += self.move_gun
        #Fit to bounds
        if self.aim<gun_rot[0]: self.aim = gun_rot[0]
        elif self.aim>gun_rot[1]: self.aim = gun_rot[1]

    def shoot(self, game_objects, gun_offset, barrel_size, bullet_type):
        gtp = self.gun_tip_pos(gun_offset, barrel_size)
        if self.face_right: launch_angle = self.aim+self.slope_angle
        else: launch_angle = self.slope_angle+(180-self.aim)

        smoke_puff(gtp[0], gtp[1], game_objects)

        return bullet_type(gtp[0], gtp[1], launch_angle)

    def gun_tip_pos(self, gun_offset, barrel_size):
        gun_radians = radians(self.aim)
        slope_radians = radians(self.slope_angle)
        if self.face_right:
            gun_x = self.x+gun_offset[0]*cos(slope_radians) + barrel_size[0]*cos(gun_radians)
        else:
            gun_x = self.x+20*cos(slope_radians) - barrel_size[0]*cos(gun_radians)
        gun_y = self.y+gun_offset[1]*sin(-slope_radians) + barrel_size[0]*sin(-gun_radians)
        #print("Barrel offset from tank is "+str(gun_x-self.x)+", "+str(gun_y-self.y))

        return (gun_x, gun_y)

    def check_if_shot(self, x, y, bullet_damage, explosion_rad, tank_size):
        explosion_dst = dst(add_coords(divide_vector(tank_size, 2), (self.x, self.y)), (x, y))
        within_explosion = max(0, explosion_rad*2-explosion_dst)

        damage = lerp(0, bullet_damage, within_explosion/(explosion_rad*2))
        self.health-=damage

        self.check_if_destroyed()
        return damage

    def direct_hit(self, bullet_max_damage):
        print("Direct hit!")
        self.health-=bullet_max_damage
        self.got_hit = True
        self.check_if_destroyed()

    def check_if_destroyed(self, dimg, dimg2, dimg3, game_object_list, gravity_accel, dead_tank_sound = None):
        if self.health<=0:
            tank_destroyed(self.x, self.y, game_object_list, gravity_accel)
            if not dead_tank_sound==None: dead_tank_sound.play()
            self.img = dimg
            if self.face_right:
                self.img2 = dimg2
            else:
                self.img2 = dimg3

    def on_key_press(self, key_pressed, player_move_restriction = None):
        if self.health>0 and key_pressed in key_player_maps[self.player_num]: #Can only move if: not exploded, key controls this player, (all players can move or this player specifically can move)
            if player_move_restriction==None or  player_move_restriction==self.player_num:
                if key_pressed in key_control_maps["move_left"]:
                    self.move = (-self.speed, self.move[1])
                    #if move_aim_restriction:
                    #    players_can_aim = False

                elif key_pressed in key_control_maps["move_right"]:
                    self.move = (self.speed, self.move[1])
                    #if move_aim_restriction:
                    #    players_can_aim = False

            if player_move_restriction==None or  player_move_restriction==self.player_num:
                if key_pressed in key_control_maps["aim_up"]:
                    self.move_gun = self.aim_speed

                elif key_pressed in key_control_maps["aim_down"]:
                    self.move_gun = -self.aim_speed

            if key_pressed in key_control_maps["shoot"] and (player_move_restriction==None or  player_move_restriction==self.player_num):
                self.shoot()

    def on_key_release(self, key_released):
        if key_released in key_player_maps[self.player_num]:
            if key_released in key_control_maps["move_left"] or key_released in key_control_maps["move_right"]:
                self.move = (0, self.move[1])
                
            if key_released in key_control_maps["aim_up"] or key_released in key_control_maps["aim_down"]:
                self.move_gun = 0

class bomb( side_fall_obj):
    def __init__(self, x, y, img, gravity_accel, bullet_init_velocity, angle_launched):
        super().__init__(img, x, y, gravity_accel)
        init_velocity = get_velocity_from_angle(angle_launched, bullet_init_velocity) 
        #print("Init velocity is "+str(init_velocity))
        self.move = init_velocity

    def pre_update(self, max_coords):
        super().pre_update(max_coords, False)
    def update(self, bullet_max_damage, game_objects, craters, game_display, ground_col, explosion_rad, tank_size, bullet, offset = (0, 0), delete_on_exit_screen = False, shooter_of_bullet_index = None):
        super().update(game_display, ground_col, offset)

        #Bounds Check
        if delete_on_exit_screen and (self.x-offset[0]<0 or self.x-offset[0]>=game_display.get_size()[0] or self.y-offset[1]<0 or self.y-offset[1]>=game_display.get_size()[1]):
            bullet = None
            #del self
            return -1, self.x, bullet
        #Hit the ground
        if not self.falling:
            #Bomb effects
            kaboom(self.x, self.y, 2, game_objects)
            craters.append(ground_part((self.x, self.y), explosion_rad))

            #Check if any tanks were hit
            hit = False
            for obj in game_objects:
                if issubclass(type(obj), tank) and obj.health>0:
                    if shooter_of_bullet_index==None: hit = hit or obj.check_if_shot(self.x, self.y, bullet_max_damage, explosion_rad)>0
                    hit = hit or obj.check_if_shot(self.x, self.y, bullet_max_damage, explosion_rad, shooter_of_bullet_index)>0

            #Delete exploded bomb
            bullet = None
            #del self
            if hit: return 1, self.x, bullet
            else: return 0, self.x, bullet

        #Check for tank collisions
        for obj in game_objects:
            if issubclass(type(obj), tank) and obj.health>0:
                tank_rect = pygame.Rect(obj.x, obj.y, tank_size[0], tank_size[1])
                if tank_rect.collidepoint(self.x, self.y):
                    if shooter_of_bullet_index==None: obj.direct_hit(bullet_max_damage)
                    else: obj.direct_hit(bullet_max_damage, shooter_of_bullet_index)

                    #Bomb effects
                    kaboom(self.x, self.y, 2, game_objects)
                    craters.append(ground_part((self.x, self.y), explosion_rad))

                    #Delete exploded bomb
                    bullet = None
                    #del self
                    return 2, self.x, bullet
        return -1, self.x, bullet
class text_arrow(linked_text): #Must be tank obj (pos, health, is ai)
    def __init__(self, link_obj, width_offset, height_offset, str_name, font, color, ww, my_arrow, robo_img, size=None):
        if size==None: 
            rect = font.render(getattr(link_obj, str_name, "NA"), True, color).get_rect()
            size = (rect.width, rect.height)
        super().__init__(link_obj, width_offset, height_offset, str_name, font, color, size)
        #Max coords for later
        self.ww = ww

        self.arrow = my_arrow
        self.robo = robo_img

    def update(self, background, offset=(0, 0)):
        text = self.font.render(getattr(self.link_obj, self.attr_name, "NA"), True, self.col)
        if not self.size == None: 
            surf = pygame.transform.scale(text, self.size)
            pos = (self.link_obj.x+self.link_obj.get_size()[0]/2-self.left-self.size[0]/2, self.link_obj.y-self.up)
        else: 
            surf = text
            pos = (self.link_obj.x+self.link_obj.get_size()[0]/2-self.left-text.get_rect().width/2, self.link_obj.y-self.up)

        display_pos = subtract_coords(pos, offset)
        too_left = display_pos[0]<0
        too_right = display_pos[0]>self.ww

        if self.link_obj.ai>0: 
            robo_offset = (35, 0)
        else: robo_offset = (35, 0)

        if too_left: #Display arrow showing other players where they are
            if self.link_obj.health>0: #Only show alive off-screen tanks
                left_arrow = rotate_img(self.arrow, (0,0), divide_vector(self.arrow.get_size(), 2), 180)[0]
                pos = (25, self.link_obj.y-offset[1])
                if self.link_obj.ai>0: background.blit(self.robo, subtract_coords(pos, (0, 25)))
                background.blit(left_arrow, (25, pos[1]))
                background.blit(surf, subtract_coords(add_coords(pos, robo_offset), (0, 25)))
        elif too_right:
            if self.link_obj.health>0: #Only show alive off-screen tanks
                if not self.size==None: pos = (self.ww-self.size[0], self.link_obj.y-offset[1])
                else: pos = (self.ww-text.get_rect().width, self.link_obj.y-offset[1])
                if self.link_obj.ai>0: background.blit(self.robo, subtract_coords(pos, (35, 25)))
                background.blit(self.arrow, (self.ww-45, pos[1]))
                background.blit(surf, subtract_coords(pos, (0, 25)))
        else: 
            if self.link_obj.ai>0: 
                pos = subtract_coords(pos, (35, 0))
                background.blit(self.robo, subtract_coords(pos, offset))
            super().display(background, subtract_coords(offset, robo_offset))

#Draw preset particle bursts
def spawn_smoke_particle(size, x, y, game_object_list):
    angle = randint(0, 359)
    darkness = randint(0, 85)
    game_object_list.append( particle(x, y, (darkness, darkness, darkness),  get_velocity_from_angle(angle, randint(2, 4)), randint(55, 85), size, 0.1, "circle", True, size/3))
def spawn_floaty_smoke(x, y, game_object_list):
    #print("Float")
    darkness = randint(0, 85)
    size = randint(5, 12)
    game_object_list.append( particle(x, y, (darkness, darkness, darkness), ((random()-0.5)*4, 0), randint(65, 150), size, 0.01, "circle", True, size*3, -0.02))
def spawn_fire_particle(size, x, y, game_object_list):
    col_offset = randint(-85, 85)
    angle = randint(0, 359)
    rr =  max(0,  min(255, fire_col[0]+col_offset/4))
    g =  max(0,  min(255, fire_col[1]+col_offset/2))
    b =  max(0,  min(255, fire_col[2]+col_offset))
    game_object_list.append( particle(x, y, (rr, g, b),  get_velocity_from_angle(angle, randint(2, 4)), randint(55, 85), size, 0.1, "circle", False, size/3))
def spawn_spark_particle(x, y, game_object_list, gravity_accel):
    col_offset = randint(0, 85)
    angle = randint(0, 359)
    size = randint(1, 4)
    rr =  max(0,  min(255, fire_col[0]))
    g =  max(0,  min(255, col_offset))
    b =  max(0,  min(255, col_offset/2))
    game_object_list.append( particle(x, y, (rr, g, b),  get_velocity_from_angle(angle, randint(5, 8)), randint(55, 85), size, 0.15, "circle", False, size/2, gravity_accel/1.5))

def smoke_puff(x, y, game_object_list):
    #print("Puff!")
    for i in range(randint(4, 8)):
        darkness = randint(0, 85)
        angle = randint(0, 359)
        size = randint(7, 15)
        game_object_list.append( particle(x, y, (darkness, darkness, darkness),  get_velocity_from_angle(angle, randint(2, 4)), randint(55, 85), size, 0.25, "circle", True, size/2))
def kaboom(x, y, awesomeness : int, game_object_list): #Awesomeness is how awesome the explosion should be
    print("Kaboom")
    particles_to_spawn = randint(5, 10)*awesomeness
    smoke = int(particles_to_spawn/3*2)
    for i in range(smoke):
        spawn_smoke_particle(randint(10*awesomeness, 35*awesomeness), x, y, game_object_list)
    for i in range(particles_to_spawn-smoke):
        spawn_fire_particle(randint(6*awesomeness, 20*awesomeness), x, y, game_object_list)
def tank_destroyed(x, y, game_object_list, gravity_accel):
    for i in range(randint(5, 10)):
        spawn_smoke_particle(randint(10, 35), x, y, game_object_list)
    for i in range(randint(3, 8)):
        spawn_spark_particle(x, y, game_object_list, gravity_accel)