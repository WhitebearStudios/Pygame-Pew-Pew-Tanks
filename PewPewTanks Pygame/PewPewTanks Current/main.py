#Words in adjsnouns.txt found in lists on internet
#Transparetn drawing code based off of code from https://stackoverflow.com/questions/6339057/draw-a-transparent-rectangles-and-polygons-in-pygame (As cited in game_object.py line 342)
#pixelFJ8pt1 font by MBommeli https://www.1001fonts.com/users/flashjunior/ free for commercial use (as cited in pygame_GUI.py line 15)
#All art by Maddox Riley!
#Sounds cited line 15 (shortly below)

#Initialize pygame and basic loop logic
import pygame
pygame.init()
clock = pygame.time.Clock()
exit = False
exit_loop = False

pygame.mixer.init()
#Sounds found on free site https://mixkit.co/free-sound-effects/explosion/, no author cited, edited by me
shoot_sound = pygame.mixer.Sound("Sounds/shoot_sound.wav")
explode_sound = pygame.mixer.Sound("Sounds/bullet_hit_sound.wav")
dead_tank_sound = pygame.mixer.Sound("Sounds/dead_tank_explode.wav")

#Color$
black = (0,0,0)
white = (255,255,255)
light_gray = (200,200,200)
light_light_gray = (245, 245, 245)

#Import random integer capability and code from other files
from random import randint

from game_object import *
from pygame_GUI import *
from pewpewclasses  import *
from FileRW import get_datas_from_file, update_dict_in_file, dict_key_in_file, write_to_file
from Leaderboard import leaderboard_window
from username_generator import rand_username
from Basic_functions import check_item_pair

score_file = "PewPewTanksScores.txt"
file_encrypted = True

#Setup starting UI
bg_header = pygame.transform.scale(pygame.image.load("bgCropped.gif"), (600, 375))

splash_size = (600, 600)
splash_display = pygame.display.set_mode(splash_size)

pygame.display.set_caption("PewPewTanks")

num_players = 0

#Draw background underneath buttons
def draw_GUI():
    global bg_header

    surf = pygame.Surface((600, 250))
    surf.fill(light_gray)

    splash_display.blit(bg_header, (0, 0))
    splash_display.blit(big_font.render("Pew Pew", True, black), (5, 5))
    splash_display.blit(big_font.render("Tanks", True, black), (5, 60))

    splash_display.blit(surf, (0, 350))
    splash_display.blit(med_font.render("Player Selection:", True, black), (5, 355))
    pygame.draw.rect(splash_display, black, pygame.Rect(0, 400, 600, 200), 10) #Border
    pygame.display.flip()
def give_rand_username(player_index : int):
    global players
    players[player_index].player_name = rand_username()

def play():
    global players, current_pop_up, num_players, ignore_list
    #print(str(ignore_list))
    if num_players<2: 
      current_pop_up = pop_up("You need at least 2 players to play this game.")
      return False
    else: 
        i=0
        for p in players:
            if p.player_name=="" and not check_item_pair(ignore_list, i, 2):
                current_pop_up = pop_up("Player "+str(i+1)+" needs a name!", True, "Surprise Me", i)
                return False
            if p.is_ai: pn = "(AI) "+p.player_name
            else: pn = p.player_name
            if dict_key_in_file(file_name, pn, file_encrypted=file_encrypted)[0] and not check_item_pair(ignore_list, i, 1):
                current_pop_up = pop_up("Player "+str(i+1)+"'s name was found in the leaderboard. Do you want to update your score?", True, b2_link_index=i)
                return False
            i+=1
        return True
def add_player():
    global players, num_players, buttons
    players.append(player_selection(players, buttons))
    buttons[0].rect.top+=35
    num_players+=1
    
def remove_player(player_index): #Easy part removing player, hard part moving rest of players up into empty spot
    global players, buttons, splash_display, num_players
    #print("Removing player "+str(player_index))

    if player_index==len(players)-1:
        buttons.pop().erase(splash_display, light_gray)
        players.pop().erase(splash_display, light_gray)
        
        buttons[0].erase(splash_display, light_gray)
        buttons[0].rect.top-=35
    else:
        for i in range(len(players)-1):
            if i<player_index: continue
            elif i==player_index:
                players.pop(i).erase(splash_display, light_gray)
                buttons.pop(i+2).erase(splash_display, light_gray)

                buttons[0].erase(splash_display, light_gray)
                buttons[0].rect.top-=35

                players[i].erase(splash_display, light_gray)
                players[i].rect.top-=35
                players[i].checkbox_rect.top-=35
                players[i].text_rect.top-=35

                buttons[i+2].erase(splash_display, light_gray)
                buttons[i+2].rect.top-=35
            else:
                players[i].erase(splash_display, light_gray)
                players[i].rect.top-=35
                players[i].checkbox_rect.top-=35
                players[i].text_rect.top-=35

                buttons[i+2].erase(splash_display, light_gray)
                buttons[i+2].rect.top-=35
        i=0
        for x in range(int(len(ignore_list)/2)):
            if ignore_list[i]==player_index:
                ignore_list.pop(i)
                ignore_list.pop(i)
            else:
                if ignore_list[i]>player_index: ignore_list[i]-=1
                i+=2
    num_players-=1
    return players, buttons, num_players
def accept_pop_up():
    global pop_up_buttons, current_pop_up
    #draw_GUI()
    current_pop_up = None
    pop_up_buttons.clear()
    draw_GUI()
def proceed_pop_up():
    global pop_up_buttons, current_pop_up
    current_pop_up = None
    pop_up_buttons.clear()
    draw_GUI()

#Lists of changeable objects in GUI
buttons = [add_players_button,
    play_button
    ]
players = []
current_pop_up = None
pop_up_buttons = []
ignore_list = []

draw_GUI()

#GUI update loop
update_rects = []
while not exit_loop:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            exit==True
            exit_loop = True
            break
        if event.type==pygame.MOUSEBUTTONDOWN: #Mouse click input
            for button in buttons:
                if button.rect.collidepoint(pygame.mouse.get_pos()) and current_pop_up==None: 
                    if button.text=="-": #Input list to edit
                        remove_player(int((button.rect.top-415)/35))
                    elif button.text=="Add Player":
                        add_player()
                    elif button.text=="Play":
                        exit_loop = play()
                    else:
                        button.action()
            for pb in pop_up_buttons:
                if pb.rect.collidepoint(pygame.mouse.get_pos()): 
                    if pb.text=="Proceed": 
                        proceed_pop_up()
                        ignore_list.append(pb.link_index)
                        ignore_list.append(1)
                        exit_loop = play()
                    elif  pb.text=="Surprise Me": 
                        accept_pop_up()
                        ignore_list.append(pb.link_index)
                        ignore_list.append(2)
                        give_rand_username(pb.link_index)
                    else:
                        accept_pop_up()
            pi=0
            for p in players:
                if p.checkbox_rect.collidepoint(pygame.mouse.get_pos()): 
                    p.is_ai += 1
                    if p.is_ai==3: p.is_ai = 0
                if p.text_rect.collidepoint(pygame.mouse.get_pos()): 
                    if p.ent_name: p.ent_name = False
                    else:
                        can_enter = True
                        ci=0
                        for check in players:
                            if check.ent_name and not ci==pi: 
                                can_enter = False
                                break
                            ci+=1

                        p.ent_name = can_enter
                pi+=1
        if event.type==pygame.KEYDOWN:
            #Text box input code based off of https://www.geeksforgeeks.org/how-to-create-a-text-input-box-with-pygame/
            if event.key==pygame.K_BACKSPACE:
                for p in players:
                    if p.ent_name: 
                        p.player_name = p.player_name[:-1]
            elif event.key==pygame.K_DELETE:
                for p in players:
                    if p.ent_name: 
                        p.player_name = ""
            elif event.key==pygame.K_RETURN:
                for p in players: p.ent_name = False
            else:
                for p in players:
                    if p.ent_name and len(p.player_name)<=26:
                        p.player_name+=event.unicode

    update_rects.clear()

    for p in players:
        p.display(splash_display)
        update_rects.append(p.rect)

    for button in buttons:
        if not button.text=="Add Player" or num_players<5: button.display(splash_display)
        update_rects.append(button.rect)

    if not current_pop_up==None: 
        current_pop_up.display(splash_display, pop_up_buttons)
        update_rects.append(current_pop_up.rect)
    for pb in pop_up_buttons:
        pb.display(splash_display)
        update_rects.append(pb.rect)
        
    pygame.display.update(update_rects)

if exit: 
  print("An error occured.")
  quit()

#-----------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------GAME SETUP--------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------

winner = 0
damage_dealt = [0]*num_players

#Game Display Config
FPS = 60

cam_pad = 200
space_between_players = 1000
win_width = 1000
win_height = 600
def in_window(p : tuple, span = (0, 0)):
    far_corner = add_coords(p, span, True)
    return (p[0]<win_width and p[0]>0 and p[1]<win_height and p[1]>0) or (far_corner[0]<win_width and far_corner[0]>0 and far_corner[1]<win_height and far_corner[1]>0)

game_win_dimensions = (cam_pad*2 + space_between_players*(num_players-1), win_height)
cam_pan_start = 100*num_players
cam_pan_start_counter = cam_pan_start

prev_scroll = None
scroll_target = None

lerp_time = 75
scroll_blend_counter = lerp_time
ai_action_delay = 120

scroll = 0
screen_offset = (0, 0)

game_display = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('PewPewTanks-Running')

#Text popups
popup_pos = (100, 50)
popup_life = 100

#Exit rules
can_fire_multi = True
player_has_fired = False
bullet_stopped = False

last_bullet_x = None

#Setup Images
tank_size = (65, 45)
barrel_size = (45, 15)
bomb_size = (15, 15)
fuel_can_size = (85, 135)
arrow_size = (45, 35)
robot_size = (30, 25)

fine_tune = False
ft_speed = 1
gun_rot = (-45, 90) #Gun rotation restriction
#Gets net angle between gun and slope angle
def can_aim_net(sa, ga, face_right):
    if sa==None or ga==None: return False
    if face_right: aim_for_net_angle = ga-sa
    else: aim_for_net_angle = ga+sa
    #print("GA: %s SA: %s Net: %s" % (str(ga), str(sa), str(net_angle)))
    return aim_for_net_angle>gun_rot[0] and aim_for_net_angle<gun_rot[1]

file_names = ["Tank.gif", "Tank Barrel.gif", "Tank Barrel Left.gif", 
            "Red Tank.gif", "Red Tank Barrel.gif", "Red Tank Barrel Flipped.gif", 
            "Yellow Tank.gif", "Yellow Tank Barrel.gif", "Yellow Tank Barrel Flipped.gif", 
            "Blue Tank.gif", "Blue Tank Barrel.gif", "Blue Tank Barrel Flipped.gif", 
            "Purple Tank.gif", "Purple Tank Barrel.gif", "Purple Tank Barrel Flipped.gif", 
            "bomb.gif", 
            "Dead Tank.gif", "Dead Tank Barrel.gif", "Dead Tank Barrel Flipped.gif", 
            "FuelCan.gif", 
            "P1Arrow.gif", "P2Arrow.gif", "P3Arrow.gif", "P4Arrow.gif", "P5Arrow.gif", 
            "Robot.gif"]

image_names = ["green_tank", "green_tank_barrel", "green_tank_barrel_flip", 
            "red_tank", "red_tank_barrel", "red_tank_barrel_flip", 
            "yellow_tank", "yellow_tank_barrel", "yellow_tank_barrel_flip", 
            "blue_tank", "blue_tank_barrel", "blue_tank_barrel_flip", 
            "purple_tank", "purple_tank_barrel", "purple_tank_barrel_flip", 
            "bullet",
            "dead tank", "dead barrel right", "dead barrel left",
            "fuel_can", "p1_arrow", "p2_arrow", "p3_arrow", "p4_arrow", "p5_arrow",
            "ai_symbol"]

images = {}

i=0
for f in file_names:
    try:
        images.update({image_names[i] : pygame.transform.scale(pygame.image.load("Tanks/"+f), tank_size)})
    except:
        try:
            images.update({image_names[i] : pygame.transform.scale(pygame.image.load("Arrows/"+f), arrow_size)})
        except:
            try:
                images.update({image_names[i] : pygame.transform.scale(pygame.image.load("Barrels/"+f), barrel_size)})
            except:
                if f=="FuelCan.gif":
                    images.update({image_names[i] : pygame.transform.scale(pygame.image.load(f), fuel_can_size)})
                elif f=="bomb.gif":
                    images.update({image_names[i] : pygame.transform.scale(pygame.image.load(f), bomb_size)})
                elif f=="Robot.gif":
                    images.update({image_names[i] : pygame.transform.scale(pygame.image.load(f), robot_size)})
    i+=1

tanks = ["green_tank", "red_tank", "yellow_tank", "blue_tank", "purple_tank"]

#Color Config
grass_col = (155, 255, 155)
background_col = (100, 200, 255)

#Game Config
start_health = 100
bullet_max_damage = 25
health_bar_offset = 15

fuel_move_restriction = False
move_aim_restriction = False
player_move_restriction = None
players_can_move = True
players_can_aim = True

fuel_max = 200
class fuel:
    def __init__(self, fuel):
        self.x = win_width/2
        self.y = 90
        self.health = fuel
fuel_level = fuel_max
fuel_bar_ref = fuel(fuel_max)
fuel_bar_width = 200

smoke_frequency = 50

gravity_accel = 0.2
slope_rotate_amplify = 1.5
bullet_init_velocity = 15

gun_offset = (tank_size[0]/1.5, 10)

craters = []
explosion_rad = 45

#GAME CLASSES/FUNCTS
class my_tank(tank):
    def __init__(self, player_num : int, player_name : str, is_ai : bool = False):
        self.name = player_name
        self.ai = is_ai

        #AI actions: 0=idle, 1=move left, 2=move right, 3=aim and fire, 4=move left a bit, 5=move right a bit 6=shoot
        self.ai_action = 0
        self.ai_aim_target = None
        self.ai_action_counter = ai_action_delay
        self.aim_error = 0
        self.waiting_for_shot = False
        self.ai_move_counter = 0
        self.ai_target = None

        my_tank_name = tanks[player_num-1]
        if player_num%2==1 and num_players==player_num: gun_img = images[my_tank_name+"_barrel_flip"]
        else: gun_img = images[my_tank_name+"_barrel"]
        super().__init__(player_num, (cam_pad+space_between_players*(player_num-1), 50), images[my_tank_name], gun_img, gravity_accel, start_health, num_players)
        self.max_coords = (win_width, win_height)
    #def respawn(self):
        #if self.player_num==1:
            #super().respawn(p1_start)
        #else:
            #super().respawn(p2_start)

    def pre_update(self, max_coords, check_bounds=True):
        #Don't phase through things that you can't see
        on_screen =  not (self.x-screen_offset[0]<0 or self.x-screen_offset[0]>=win_width or self.y-screen_offset[1]<0)
        if on_screen: super().pre_update(max_coords, check_bounds)

    def update(self, bg, offset = (0, 0)):
        global fuel_level, fuel_move_restriction, players_can_move, players_can_aim, player_move_restriction, game_objects
        move_action = int(self.face_right)+1

        if self.health>0:
            if bullet_stopped and self.waiting_for_shot:
                self.aim_error = self.ai_target.x-last_bullet_x
                if abs(self.aim_error)<tank_size[0]/2 and self.ai==2: 
                    self.aim_error = 0
                    print("Hit target!")
                elif abs(self.aim_error)>abs(self.ai_target.x-self.x)*0.8:
                    self.aim_error = 0
                    self.misses = 3
                    print("Missed horribly, change position next turn")
                else: print("My error was "+str(self.aim_error))
                self.waiting_for_shot = False

            #Its the start of the ai's turn; decide what to do
            if player_move_restriction==self.player_num and self.ai_action==0 and self.ai>0 and not player_has_fired and cam_pan_start_counter<=0 and not self.falling:
                self.ai_get_target()
                if self.misses>2 or self.got_hit:
                    print("Moving to different position")
                    self.ai_move_counter = randint(35, 75)
                    self.aim_error = 0
                    if self.face_right: self.ai_action = 5
                    else: self.ai_action = 4
                else:
                    print("Missed "+str(self.misses))

                    if fuel_level>0: 
                        print("Stopped move adjustment, starting targeting")
                        self.try_aim_target(3, move_action)
                    else: 
                        print("Out of fuel, aim")
                        self.try_aim_target(3, 3, 45)
            
            if self.ai_action_counter>0 and self.ai_action>0:
                self.ai_action_counter-=1
                #If aiming make sure tank is still
                if self.ai_action==3: self.move = (0, self.move[1])
                #if self.ai_action<3 or self.ai_action>3: print("Waiting to move")
                #else: print("Waiting to shoot")
            else:
                if self.ai_action==1 or self.ai_action==2: 
                    self.move = (self.speed*(int(self.ai_action==2)*2-1), self.move[1])
                    print("Seeing if in range, else keep moving")
                    self.try_aim_target(3, move_action)
                elif self.ai_action==3:
                    if player_move_restriction==self.player_num: 
                        if not can_aim_net(self.slope_angle, self.ai_aim_target, self.face_right):
                            print("Unable to aim, move")
                            if fuel_level<=0: 
                                print("Uhoh")
                            self.ai_action = move_action
                        else:
                            if self.face_right: net_angle = self.aim+self.slope_angle
                            else: net_angle = self.aim-self.slope_angle
                            self.move = (0, self.move[1]) #Stop the tank!!
                            if abs(net_angle-self.ai_aim_target)<1 and (not player_has_fired or can_fire_multi):
                                #print("Aim "+str(self.aim)+" Slope "+str(self.slope_angle)+" Net "+str(net_angle)+" Target "+str(self.ai_aim_target))
                                self.move_gun = 0
                                #Delay then shoot
                                self.ai_action = 6
                                self.ai_action_counter = int(ai_action_delay/2)

                            elif net_angle>self.ai_aim_target:
                                if abs(net_angle-self.ai_aim_target)<5: self.move_gun = -1
                                else: self.move_gun = -self.aim_speed
                                if move_aim_restriction:
                                    players_can_move = False

                            elif net_angle<self.ai_aim_target:
                                if abs(net_angle-self.ai_aim_target)<5: self.move_gun = 1
                                else: self.move_gun = self.aim_speed
                                if move_aim_restriction:
                                    players_can_move = False

                elif self.ai_action==4 or self.ai_action==5: 
                    self.move = (self.speed*(int(self.ai_action-3==2)*2-1), self.move[1])
                    self.ai_move_counter-=1
                    #Figure out next action on next iteration of update()
                    if self.ai_move_counter<=0:
                        self.ai_action = 0
                        #Reset so tank doesn't keep going back and forth
                        self.got_hit = False
                        self.misses = 0

                elif self.ai_action==6:
                    self.shoot()
                    #Reset
                    self.ai_action_counter = ai_action_delay
                    self.ai_action = 0
                    self.ai_aim_target = None
                    self.waiting_for_shot = True

                if player_move_restriction==self.player_num and fuel_level<=0 and self.ai and self.ai_aim_target==None and not player_has_fired: #This AI is out of fuel so they are confused what to do
                    print("Out of fuel, aim")
                    self.try_aim_target(3, 3, 45)


            if player_move_restriction==self.player_num and fuel_level<=0: #This tank is out of fuel
                self.move = (0, self.move[1]) #Stop the tank!!
                players_can_move = False
                players_can_aim = True

            
        on_screen =  not (self.x-offset[0]<0 or self.x-offset[0]>=win_width or self.y-offset[1]<0)
        super().update(barrel_size, gun_offset, bg, [grass_col], smoke_frequency, gun_rot, game_objects, offset, on_screen)
        if fuel_move_restriction and not self.move[0]==0:
            fuel_level-=1

    def ai_get_target(self, auto_flip = True):
        distances = dict() #target : distance
        closest_target = {None : game_win_dimensions[0]+1} #Max distance
        #Get x-diff to players in tank's direction
        for i in range(num_players):
            if i==self.player_num-1: continue #Can't target self
            t_obj = game_objects[i*3]
            if ((self.face_right and t_obj.x>self.x) or (not self.face_right and t_obj.x<self.x)) and t_obj.health>0:
                distances.update({t_obj : abs(t_obj.x-self.x)})
        #Can't find tank in this direction
        if len(distances)==0:
            if auto_flip:
                flip_tank(self.player_num)
                self.ai_get_target()
                return
            else:
                return False
        #Get closest distance
        for t_obj in distances:
            if distances[t_obj]<list(closest_target.values())[0]:
                closest_target = {t_obj : distances[t_obj]}

        closest_target = list(closest_target.keys())[0]
        if not self.ai_target==closest_target:
            self.aim_error = 0 #Reset targeting
        self.ai_target = closest_target
        #print("Targeting "+closest_target.name)
        return True

    def get_ai_launch_angle(self):
        if self.ai==2: #Use correct vairables for formula
            print("Grrrrr")
            correct_y_t = win_height-self.ai_target.y
            correct_y = win_height-self.y
            xy_diff = (abs(self.ai_target.x-self.x+self.aim_error), correct_y_t-correct_y)
        else: #Use broken variables that somehow still work sometimes for the formula
            print("Using okay formula")
            xy_diff = (abs(self.ai_target.x-self.x+self.aim_error), abs(self.ai_target.y-self.y))
        return get_launch_angle(xy_diff, bullet_init_velocity, gravity_accel)

    def try_aim_target(self, action_if_in_range, action_if_cant_reach, def_shoot_angle = None):
        global screen_offset
        if not action_if_cant_reach==self.ai_action: 
            print("----------delay next action")
            self.ai_action_counter = ai_action_delay

        if (self.ai_target.x<self.x and self.face_right) or (self.ai_target.x>self.x and not self.face_right):
            flip_tank(self.player_num)
        t_angle = self.get_ai_launch_angle()
        if t_angle==None: #Target too far away or can't reach angle at current slope
            print("Target too far away, Move towards target")
            self.ai_action = action_if_cant_reach
            if not def_shoot_angle==None:
                if can_aim_net(self.slope_angle, def_shoot_angle, self.face_right): self.ai_aim_target = def_shoot_angle
                else: 
                    if self.face_right: self.ai_aim_target = def_shoot_angle+self.slope_angle
                    else: self.ai_aim_target = def_shoot_angle-self.slope_angle
        else: #Target in range, aim
            if abs(self.ai_target.x-self.x)<400:
                if in_window(subtract_coords((self.x, self.y), screen_offset), tank_size) and in_window(subtract_coords((self.ai_target.x, self.ai_target.y), screen_offset), tank_size): 
                    if check_path(game_display, [grass_col], (self.x, self.y), (self.ai_target.x, self.ai_target.y), 25, screen_offset): 
                        print("Choosing lower angle")
                        t_angle =  min(t_angle[0], t_angle[1])
                        ang_offset = -2
                    else:
                        ang_offset = 2
                        t_angle =  max(t_angle[0], t_angle[1])
                else:
                    print("Waiting to display")
                    return
            else: 
                ang_offset = 2
                t_angle =  max(t_angle[0], t_angle[1])
            if not can_aim_net(self.slope_angle, t_angle+ang_offset, self.face_right):
                print("Can't reach angle at current slope")
                self.ai_action = action_if_cant_reach #Move right towards target
                if not def_shoot_angle==None: 
                    self.ai_aim_target = def_shoot_angle
                else:
                    self.ai_aim_target = None
            else:
                print("Target in range, aim")
                self.ai_aim_target = t_angle+ang_offset
                self.ai_action = action_if_in_range
                print("----------delay next action")
                self.ai_action_counter = ai_action_delay


    def shoot(self):
        global player_has_fired, bullet
    
        bullet = super().shoot(game_objects, gun_offset, barrel_size, my_bomb)
        player_has_fired = True
        shoot_sound.play()

    def check_if_shot(self, x, y, bullet_damage, explosion_rad, shooter_of_bullet_index):
        global damage_dealt
        damage = super().check_if_shot(x, y, bullet_damage, explosion_rad, tank_size)
        damage_dealt[shooter_of_bullet_index] += int(damage)
        print("Player "+str(shooter_of_bullet_index+1)+" dealt "+str(damage)+" damage.")
        return damage
    def direct_hit(self, bullet_max_damage, shooter_of_bullet_index):
        super().direct_hit(bullet_max_damage)
        global damage_dealt
        damage_dealt[shooter_of_bullet_index] += int(bullet_max_damage)
        print("Player "+str(shooter_of_bullet_index+1)+" dealt "+str(bullet_max_damage)+" damage.")

    def on_key_press(self, key_pressed):
        global player_move_restriction, players_can_aim, players_can_move, move_aim_restriction, fine_tune
        try:
            my_turn = key_pressed in key_player_maps[self.player_num]
        except:
            my_turn = player_move_restriction==self.player_num and key_pressed in key_player_maps[1]
        else:
            my_turn = not player_move_restriction==None and (player_move_restriction==self.player_num and key_pressed in key_player_maps[1])
        #Use only player 1's controls if only one tank moves at a time
        if not self.ai and self.health>0 and my_turn: #Can only move if: not exploded, key controls this player, (all players can move or this player specifically can move)
            if players_can_move:
                if key_pressed in key_control_maps["move_left"]:
                    self.move = (-self.speed, self.move[1])
                    #if move_aim_restriction:
                    #    players_can_aim = False
    
                elif key_pressed in key_control_maps["move_right"]:
                    self.move = (self.speed, self.move[1])
                    #if move_aim_restriction:
                    #    players_can_aim = False
                    
            if players_can_aim:
                if key_pressed in key_control_maps["aim_up"]:
                    if fine_tune:
                        self.move_gun = 1
                    else:
                        self.move_gun = self.aim_speed
                    if move_aim_restriction:
                        players_can_move = False
    
                elif key_pressed in key_control_maps["aim_down"]:
                    if fine_tune:
                        self.move_gun = -1
                    else:
                        self.move_gun = -self.aim_speed
                    if move_aim_restriction:
                        players_can_move = False

            if key_pressed in key_control_maps["shoot"] and (not player_has_fired or can_fire_multi):
                self.shoot()

    def on_key_release(self, key_released):
        try:
            my_turn = player_move_restriction==None and key_released in key_player_maps[self.player_num]
        except:
            my_turn = player_move_restriction==self.player_num and key_released in key_player_maps[1]
        else:
            my_turn = not player_move_restriction==None and (player_move_restriction==self.player_num and key_released in key_player_maps[1])
        if not self.ai and my_turn: #Add move restriction functionality to always use 1st player's controls 
            if key_released in key_control_maps["move_left"] or key_released in key_control_maps["move_right"]:
                self.move = (0, self.move[1])
                
            if key_released in key_control_maps["aim_up"] or key_released in key_control_maps["aim_down"]:
                self.move_gun = 0

    def check_if_destroyed(self):
        super().check_if_destroyed(images["dead tank"], images["dead barrel right"], images["dead barrel left"], game_objects, gravity_accel, dead_tank_sound)

class my_bomb(bomb):
    def __init__(self, x, y, angle_launched):
        super().__init__(x, y, images["bullet"], gravity_accel, bullet_init_velocity, angle_launched)
    def update(self, bg, shooter_of_bullet : my_tank, offset = (0, 0)):
        global bullet_stopped, last_bullet_x, text_splash, game_objects, bullet
        bullet_data, last_bullet_x, bullet = super().update(bullet_max_damage, game_objects, craters, bg, [grass_col], explosion_rad, tank_size, bullet, offset, False, shooter_of_bullet.player_num-1)
        bullet_stopped = bullet_data>=0 #Function returns -1 if no fun things happen (kablooies)

        if bullet_stopped: explode_sound.play()
        if bullet_data==0: 
            text_splash = pop_message(popup_pos, popup_life, "Miss!", med_font, black, (100, 50), (150, 75))
            shooter_of_bullet.misses+=1
        elif bullet_data==1: 
            text_splash = pop_message(popup_pos, popup_life, "Hit!", med_font, black, (75, 50), (125, 75))
            shooter_of_bullet.misses = 0
        elif bullet_data==2:
            text_splash = pop_message(popup_pos, popup_life, "Direct Hit!", med_font, black, (150, 50), (200, 75))
            shooter_of_bullet.misses = 0
class fuel_bar(health_bar):
    def __init__(self) -> None:
        super().__init__(fuel_bar_ref, fuel_bar_width/2, 0, fuel_max, 0, False, length=fuel_bar_width, width=15, health_col=(150, 150, 50))
    def update(self):
        super().update(game_display)
class fuel_img(game_object):
    def __init__(self):
        super().__init__(images["fuel_can"], win_width/2-fuel_bar_width/2-20, 20)
    def update(self):
        super().display(game_display)
def update_fuel_bar():
    global num_players
    fuel_bar_ref.health = fuel_level
    game_objects[num_players*3].update()
    game_objects[num_players*3+1].update()

#Setup ground shape
circle_coords = []
for i in range(randint(4*(num_players-1), 8*(num_players-1))):
    rad = randint(100, 300)
    #print(str(rad))
    circle_coords.append(ground_part((randint(0, game_win_dimensions[0]), game_win_dimensions[1]), rad))
#Draw ground
def draw_ground():
    for coord in circle_coords:
        pygame.draw.circle(game_display, grass_col, subtract_coords(coord.coord, screen_offset), coord.radius)
        #print("Drew a circle at " +str(x_cor)+", "+str(display_dimensions[1]))
def draw_craters():
    for coord in craters:
        pygame.draw.circle(game_display, background_col, subtract_coords(coord.coord, screen_offset), coord.radius)



#-----------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------GAME CODE-----------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------

#Number of objects in game at start
num_objs = num_players*3+2
game_objects = [None]*num_objs
bullet = None
delete_objs = []

static_objs = [health_bar, linked_text, text_arrow, fuel_bar, fuel_img, particle]
post_update_types = [health_bar]
post_update_objs = []

for i in range(num_players*3):
    my_num = int(i/3)
    #Tank
    if i%3==0: game_objects[i] = my_tank(my_num+1, players[my_num].player_name, players[my_num].is_ai)
    #Health bar
    elif i%3==1: game_objects[i] = health_bar(game_objects[i-1], tank_size[0]/2, health_bar_offset, start_health, 75, True, 50)
    #Player name
    else: game_objects[i] = text_arrow(game_objects[i-2], 0, 45, "name", small_font, black, win_width, images["p%s_arrow" % str(my_num+1)], images["ai_symbol"])
  
#Functions about tanks in game
def one_player_left():
    i=0
    players_down = 0
    for p in range(num_players):
        if game_objects[i].health<=0: players_down+=1
        i+=3
    return players_down>=num_players-1
def find_last_player(): #Returns index of first player found standing
    for pi in range(num_players):
        if game_objects[pi*3].health>0: return pi*3
    return 0 #All players down somehow
def flip_tank(player_num):
    my_tank = game_objects[(player_num-1)*3]
    game_objects[(player_num-1)*3].face_right = not my_tank.face_right
    #Flip barrel img right orientation
    if (player_num%2==0 and my_tank.face_right) or (player_num%2==1 and not my_tank.face_right): game_objects[(player_num-1)*3].img2 = images[tanks[player_num-1]+"_barrel_flip"]
    else: game_objects[(player_num-1)*3].img2 = images[tanks[player_num-1]+"_barrel"]
    print("Flipped "+my_tank.name)

#Fuel bar for each turn
game_objects[num_players*3] = fuel_bar()
game_objects[num_players*3+1] = fuel_img()

text_splash = None #Messages during game

#Test particles
#game_objects.append(my_particle(0, 0, black, (15, 9), 100, 50, 0.4))
#smoke_puff(250, 250)

#Main loop
#States: 
# forever: play forever, ignoring player states
# freeforall: play with no rules, return when a player is destroyed
# turn: allow one player to move and fire
def play_tanks(exit_state : str = "forever", player_turn : int = None, exit_delay = 300, extra_time_when_exploded = 0):
    global game_win_dimensions, fuel_move_restriction, move_aim_restriction, game_objects, players_can_move, players_can_aim, player_move_restriction, can_fire_multi, bullet_stopped, player_has_fired, scroll, screen_offset, bullet, text_splash, winner, prev_scroll, scroll_target, scroll_blend_counter, cam_pan_start_counter, fine_tune

    this_tank = game_objects[(player_turn-1)*3]
    if this_tank.health<=0: 
        print(this_tank.name+" is blown up so skip")
        return False #Skip dead tanks
    else:
        print(this_tank.name+"'s HP: "+str(this_tank.health))

    #If a player has nobody to shoot at, give them the option to flip their tank
    found_target = this_tank.ai_get_target(False)
    if not found_target and this_tank.ai<=0: 
        flip = Button(pygame.Rect(850, 500, 140, 75), light_gray, None, 5, black, None, "Flip", big_font, black)
    else: flip = None

    exit_game = False
    exit_counter = exit_delay

    player_move_restriction = player_turn
    exit_types = ["forever", "freeforall", "turn"]
    if not exit_state in exit_types:
        print("Error: invalid exit state")
        return
    exit_counter = exit_delay
    if exit_state=="turn": 
        fuel_move_restriction = True
        move_aim_restriction = True
        can_fire_multi = False
        if player_turn==None:
            print("Error: no turn provided") 
            return

    while not exit_game:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                #Dev tools
                '''
                #Manual scroll
                if event.key==pygame.K_i:
                    scroll-=50
                    screen_offset = (scroll, 0)
                elif event.key==pygame.K_o:
                    scroll+=50
                    screen_offset = (scroll, 0)
               
                #Destroy tanks instantly
                elif event.key==pygame.K_1:
                    game_objects[0].health = -1
                    game_objects[0].check_if_destroyed()
                elif event.key==pygame.K_2:
                    game_objects[3].health = -1
                    game_objects[3].check_if_destroyed()
                elif event.key==pygame.K_3:
                    game_objects[6].health = -1
                    game_objects[6].check_if_destroyed()
                elif event.key==pygame.K_4:
                    game_objects[9].health = -1
                    game_objects[9].check_if_destroyed()
                '''

                if event.key==pygame.K_LSHIFT:
                    fine_tune = True
                else:
                    for obj in game_objects:
                        obj.on_key_press(event.key)
            if event.type == pygame.KEYUP:
                if event.key==pygame.K_LSHIFT:
                    fine_tune = False
                else:
                    for obj in game_objects:
                        obj.on_key_release(event.key)
            if event.type==pygame.MOUSEBUTTONDOWN:
                if not flip==None:
                    if flip.rect.collidepoint(pygame.mouse.get_pos()):
                        flip_tank(player_turn)


        #for obj in game_objects:
            #obj.erase(game_display, background)

        for obj in game_objects:
            if not type(obj) in static_objs: obj.pre_update(game_win_dimensions)
        if not bullet==None: bullet.pre_update(game_win_dimensions)
            
        if not text_splash==None:
          text_splash.pre_update()
          if text_splash.life<=0: text_splash = None
        
        game_display.fill(background_col) #Display background

        #Update screen scrolling
        if cam_pan_start_counter>0:
            scroll = int(lerp(game_win_dimensions[0]-win_width, 0, cam_pan_start_counter/cam_pan_start))
            cam_pan_start_counter-=1
        else:
            if scroll_blend_counter>0: scroll_blend_counter-=1
            if player_turn==None: scroll = 0 #(game_objects[0].x+game_objects[1].x)/2 Average of player positions
            elif not bullet==None and exit_state=="turn":
                if not scroll_target==None and not scroll_target==0:
                    if not scroll_target==None: prev_scroll = scroll
                    scroll_target = 0
                    scroll_blend_counter = lerp_time
                padx = win_width/2
                #Smooth blend between target change
                #print("Cam on bullet")
                if not prev_scroll==None: scroll = int(lerp(bullet.x+bullet.move[0]-padx, prev_scroll, scroll_blend_counter/lerp_time))
                else: scroll = bullet.x+bullet.move[0]-padx
            else:
                #print("Cam on player"+str(player_turn))
                if not scroll_target==player_turn:
                    if not scroll_target==None: prev_scroll = scroll
                    scroll_target = player_turn
                    scroll_blend_counter = lerp_time
                if this_tank.face_right: padx = cam_pad
                else: padx = win_width-cam_pad
                #Smooth blend between target change
                if not prev_scroll==None: scroll = int(lerp(this_tank.x-padx, prev_scroll, scroll_blend_counter/lerp_time))
                else: scroll = this_tank.x-padx

        #print(str(scroll))
        screen_offset = (scroll, 0)
        #screen_offset = (0, 0)
        

        draw_ground()
        draw_craters()
        pygame.draw.rect(game_display, grass_col, pygame.Rect(0, game_win_dimensions[1]-10, game_win_dimensions[0]+1, 11))

        delete_objs.clear()
        post_update_objs.clear()
        for obj in game_objects:
            if type(obj) in post_update_types: 
                post_update_objs.append(obj)
            else:
                if not (type(obj)==fuel_bar or type(obj)==fuel_img):
                    obj.update(game_display, screen_offset)
            #Delete spent particles
            if hasattr(obj, "life") and obj.life<=0: 
                delete_objs.append(obj)
        if not bullet==None: bullet.update(game_display, game_objects[(player_turn-1)*3], screen_offset)

        for obj in post_update_objs: #Draw health bars on top of everything else
            obj.update(game_display, screen_offset)
            
        if not text_splash==None:
          text_splash.display(game_display)

        if players_can_move and fuel_move_restriction:
            update_fuel_bar()

        #Arrow to show who's turn it is
        down_arrow = rotate_img(images["p1_arrow"], (0,0), divide_vector(arrow_size, 2), -90)[0]
        game_display.blit(down_arrow, subtract_coords((this_tank.x+10, this_tank.y-95), screen_offset))

        for del_obj in delete_objs:
            game_objects.remove(del_obj)
            del del_obj

        if not flip==None: flip.display(game_display)

        pygame.display.flip()

        if exit_counter<=0:
            exit_game = True

        if bullet_stopped and exit_state=="turn":
            if one_player_left(): exit_counter+=extra_time_when_exploded
            extra_time_when_exploded = 0 #Only add once
            players_can_move = False
            players_can_aim = False
            exit_counter-=1
            #print("Stopping")

        if exit_state=="freeforall": #Exit when only one player is left
            if one_player_left(): exit_counter-=1

        #If a player has nobody to shoot at, give them the option to flip their tank
        found_target = this_tank.ai_get_target(False)
        if not found_target and this_tank.ai<=0: 
            flip = Button(pygame.Rect(850, 500, 140, 75), light_gray, None, 5, black, None, "Flip", big_font, black)
        else: flip = None
        
            
    #Reset variables for next turn
    global fuel_level
    fuel_level = fuel_max
    player_has_fired = False
    bullet_stopped = False
    #Reset AI action to update target
    game_objects[(player_turn-1)*3].ai_action = 0

    fuel_move_restriction = False
    move_aim_restriction = False
    player_move_restriction = None
    players_can_move = True
    players_can_aim = True

    if exit_game: print("Game Exited Successfully!")
    else: return -1

    winner = find_last_player()
    return one_player_left()

i=0
print("Player %s's turn" % str(i%num_players+1))
while not play_tanks("turn", i%num_players+1, 75, 250): #While more than one player left
    i+=1
    print("Player %s's turn" % str(i%num_players+1))
#play_tanks("freeforall")

#Update leaderboard file
for pi in range(num_players):
    my_player = game_objects[pi*3]
    if my_player.ai: pn = "(AI) "+my_player.name
    else: pn = my_player.name
    dd = damage_dealt[pi]
    key = dict_key_in_file(score_file, pn, file_encrypted=file_encrypted)
    if key[0]:
        update_dict_in_file(score_file, pn, [key[1][0]+dd, dd], 1, file_encrypted=file_encrypted)
    else: write_to_file(score_file, {pn : [dd, dd]}, file_encrypted=file_encrypted)


#Remove fuel bars
game_objects.pop(num_players*3)
game_objects.pop(num_players*3)

#Show health bars
for i in range(num_players):
    game_objects[i*3+1].always_show = True

#Text for congrats
winner_name = game_objects[winner].name
win_text = [big_font.render(winner_name+" has won the game!", True, black)]
if win_text[0].get_rect().width>=win_width: 
    win_text = [big_font.render(winner_name, True, black), big_font.render("has won the game!", True, black)]
    if win_text[0].get_rect().width>=win_width:
        win_text[0] = pygame.transform.scale(win_text[0], (win_width-30, win_text[0].get_rect().height))

#Put winner in center of screen
screen_offset = (game_objects[winner].x-win_width/2, 0)
#screen_offset = (0, 0)

def show_leaderboard():
    leaderboard_window(score_file, "Damage", file_encrypted=file_encrypted)

#Exit button
exit_b = Button(pygame.Rect(845, 510, 140, 75), light_gray, None, 5, black, None, "Exit", big_font, black)
#Leaderboard button
lb_b = Button(pygame.Rect(15, 530, 260, 45), light_gray, None, 5, black, None, "Show Leaderboard", small_font, black)

#Exit screen loop, players are there but can't move
exit = False
while not exit:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if exit_b.rect.collidepoint(pygame.mouse.get_pos()): exit = True
            if lb_b.rect.collidepoint(pygame.mouse.get_pos()): show_leaderboard()
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                scroll-=50
                screen_offset = (scroll, 0)
            elif event.key==pygame.K_RIGHT:
                scroll+=50
                screen_offset = (scroll, 0)

    game_display.fill(background_col)
    draw_ground()
    draw_craters()
    pygame.draw.rect(game_display, grass_col, pygame.Rect(0, game_win_dimensions[1]-10, game_win_dimensions[0]+1, 11))

    delete_objs.clear()
    for obj in game_objects:
        #Delete spent particles
        if hasattr(obj, "life") and obj.life<=0: 
            delete_objs.append(obj)

        else: obj.update(game_display, screen_offset)

    #Display exit button, winning text
    exit_b.display(game_display)
    lb_b.display(game_display)
    yo = 0
    for t in win_text:
        game_display.blit(t, (win_width/2-t.get_width()/2, 15+yo))
        yo+=60

    for del_obj in delete_objs:
        game_objects.remove(del_obj)
        del del_obj

    pygame.display.flip()

#Remove addition symbols for next game
highscores = get_datas_from_file(score_file, 2, True, file_encrypted=file_encrypted)
for key in highscores:
    highscores[key][1] = 0
#Update File
write_to_file(score_file, highscores, append_block=False, file_encrypted=file_encrypted)

#Exit
pygame.quit()
quit()