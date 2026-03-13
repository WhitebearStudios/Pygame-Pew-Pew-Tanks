import math as m
import pygame

def lerp(x1, x2, val):
    lerp_val = x1+(x2-x1)*val
    #print("Between "+str(x1)+" and "+str(x2)+" at "+str(val)+" is "+str(lerp_val))
    return lerp_val
def lerp_coord(p1, p2, val, need_int = False):
    if need_int: return (int(lerp(p1[0], p2[0], val)), int(lerp(p1[1], p2[1], val)))
    else: return (lerp(p1[0], p2[0], val), lerp(p1[1], p2[1], val))
def dst(coord1, coord2):
    x = abs(coord1[0] - coord2[0])
    y = abs(coord1[1] - coord2[1])
    return m.sqrt(x*x+y*y)

def get_velocity_from_angle(angle, multiplier):
    x_scale = m.cos(m.radians(angle))
    y_scale = -m.sin(m.radians(angle))
    #print("Scales are "+str(x_scale)+" and "+str(y_scale))
    return (x_scale*multiplier, y_scale*multiplier)
def get_launch_angle(xy_diff, init_velocity, gravity):
    v2 = init_velocity*init_velocity
    v4 = v2*v2
    x2 = xy_diff[0]*xy_diff[0]
    x = xy_diff[0]
    y = xy_diff[1]
    g = gravity
    
    dst = g*(g*x2+2*y*v2)
    if dst>v4: return None #Target pos is too far away
    plus_minus = m.sqrt(v4-dst)
    return m.degrees(m.atan((v2+plus_minus)/(g*x))), m.degrees(m.atan((v2-plus_minus)/(g*x)))

def max(v1, v2):
    if v1>v2: return v1
    else: return v2
def min(v1, v2):
    if v1<v2: return v1
    else: return v2
def add_coords(c1, c2, need_int = False):
    if need_int: return (int(c1[0]+c2[0]), int(c1[1]+c2[1]))
    else: return (c1[0]+c2[0], c1[1]+c2[1])
def subtract_coords(c1, c2, need_int = False):
    if need_int: return (int(c1[0]-c2[0]), int(c1[1]-c2[1]))
    else: return (c1[0]-c2[0], c1[1]-c2[1])
def divide_vector(vec, div):
  return (vec[0]/div, vec[1]/div)

def check_path(bg : pygame.Surface, gcs : list, p1 : tuple, p2 : tuple, point_density : int, offset : tuple = (0, 0)):
    pdst = dst(p1, p2)
    num_points = int(pdst/point_density-1)

    for i in range(num_points):
        cp = lerp_coord(p1, p2, (i+1)/num_points, True)
        #print("Checknig point "+str(cp))
        if bg.get_at(subtract_coords(cp, offset)) in gcs: return False
    return True

keys = {"a" : pygame.K_a, "d" : pygame.K_d, "w" : pygame.K_w, "s" : pygame.K_s, "g" : pygame.K_g, "h" : pygame.K_h,
        "left" : pygame.K_LEFT, "right" : pygame.K_RIGHT, "up" : pygame.K_UP, "down" : pygame.K_DOWN,
        "enter" : pygame.K_RETURN, "space" : pygame.K_SPACE}

key_player_maps = {1 : [keys["a"], keys["d"], keys["w"],  keys["s"],  keys["space"]], 
    2 : [ keys["up"],  keys["left"],  keys["right"],  keys["down"],  keys["enter"]]}

key_control_maps = {"move_left" : [ keys["a"],  keys["left"]], 
    "move_right" : [ keys["d"],  keys["right"]], 
    "aim_up" : [ keys["w"],  keys["up"]], 
    "aim_down" : [ keys["s"],  keys["down"]],
    "shoot" : [ keys["space"],  keys["enter"]]}

#Learned/based off of code from https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame
def rotate_img(img, pos, img_origin, angle):
    img_rect = img.get_rect(topleft = (pos[0]-img_origin[0], pos[1]-img_origin[1]))
    offset_to_rotate = pygame.math.Vector2(pos) - img_rect.center

    rotated_pos = offset_to_rotate.rotate(-angle)
    new_img_center = (pos[0]-rotated_pos.x, pos[1]-rotated_pos.y)

    rotated_img = pygame.transform.rotate(img, angle)

    return rotated_img, rotated_img.get_rect(center = new_img_center)

#Base class
class game_object:
    def __init__(self, img, x, y):
        self.img = img
        self.x = x
        self.y = y
        self.speed = 1
        self.move = (0,0)
    def display(self, game_display, offset = (0, 0)):
        game_display.blit(self.img, subtract_coords((self.x, self.y), offset))
    def erase(self, game_display, background):
        game_display.blit(background, (self.x, self.y))
    def pre_update(self, max_coords, check_bounds = True):
        self.x+=self.move[0]
        self.y+=self.move[1]
        if check_bounds:
            #Stay in bounds
            if self.x<0: self.x = 0
            elif self.x>=max_coords[0]: self.x = max_coords[0]
            if hasattr(self, "get_size") and self.x+self.get_size()[0]>=max_coords[0]: self.x = self.max_coords[0]-self.get_size()[0]

            if self.y<0: self.y = 0
            elif self.y>=max_coords[1]: self.y = max_coords[1]
            if hasattr(self, "get_size") and self.y+self.get_size()[1]>=max_coords[1]: self.y = self.max_coords[1]-self.get_size()[1]

    def on_key_press(self, key_pressed):
        #Do fun stuff with keys
        pass
    def on_key_release(self, key_released):
        #Do fun stuff with keys
        pass
    def get_size(self):
        return self.img.get_size()
    def get_center(self, is_int = False):
        if is_int:
            return (int(self.x+self.get_size()[0]/2), int(self.y+self.get_size()[1]/2))
        else:
            return (self.x+self.get_size()[0]/2, self.y+self.get_size()[1]/2) 

#Extensions linked to other objects to display their attributes
class health_bar(game_object):
    def __init__(self, link_obj, width_offset, height_offset, max_health, time_to_change = 0, only_show_on_change = False, hide_delay : int = 0, length = 50, width = 5, health_col = (25, 255, 25), no_health_col = (255, 0, 0)): #Linked object must have position and health
        if not(hasattr(link_obj, "x") and hasattr(link_obj, "y") and hasattr(link_obj, "health")):
            print("Error: invalid linked object")
            return None
        self.link_obj = link_obj
        self.up = height_offset
        self.left = width_offset
        self.always_show = not only_show_on_change
        self.hd = hide_delay
        self.hide_counter = hide_delay
        self.new_health = max_health
        self.old_health = max_health
        self.max_health = max_health
        self.time = time_to_change
        self.counter = 0
        self.len = length
        self.w = width
        self.c1 = health_col
        self.c2 = no_health_col
    def pre_update(self):
        pass
    def erase(self, game_display, background):
        game_display.blit(background, (self.link_obj.x+self.left-self.len/2, self.link_obj.y-self.up))
    def display(self, background, offset = (0, 0)):
        start_x = self.link_obj.x+self.left-self.len/2
        #print("New: "+str(self.new_health)+"\n"+"Old: "+str(self.old_health)+"\n"+"Counter: "+str(self.counter))
        if self.time>0: health_lerp = lerp(self.new_health, self.old_health, self.counter/self.time)
        else: health_lerp = self.new_health
        end_green = start_x + lerp(0, self.len, health_lerp/self.max_health)
        #print("From "+str(start_x)+" to "+str(end_green))
        y = self.link_obj.y-self.up

        pygame.draw.line(background, self.c2, subtract_coords((end_green, y), offset), subtract_coords((start_x+self.len, y), offset), self.w)
        pygame.draw.line(background, self.c1, subtract_coords((start_x, y), offset), subtract_coords((end_green, y), offset), self.w)

    def update(self, background, offset = (0, 0)):
        if self.counter>0: self.counter-=1
        else: 
            self.old_health = self.new_health #Reset after showing change
            if self.hide_counter>0: self.hide_counter-=1

        if not self.new_health==max(0, self.link_obj.health): #Start change
            self.counter = self.time
            self.new_health = max(0, self.link_obj.health)
            self.hide_counter = self.hd

        if self.always_show or self.counter>0 or self.hide_counter>0: self.display(background, offset)

#Text that moves with object
class linked_text(game_object):
    def __init__(self, link_obj, width_offset, height_offset, str_name, font, color, size = (75, 25)): #Linked object must have position and health
        if not(hasattr(link_obj, "x") and hasattr(link_obj, "y") and hasattr(link_obj, str_name)):
            print("Error: invalid linked object")
            return None
        self.link_obj = link_obj
        self.up = height_offset
        self.left = width_offset
        self.counter = 0
        self.size = size
        self.attr_name = str_name
        
        self.font = font
        self.col = color
    def pre_update(self):
        pass
    #def erase(self, game_display, background):
        #game_display.blit(background, (self.link_obj.x-self.left, self.link_obj.y-self.up))
    def display(self, background, offset = (0, 0)):
        pos = (self.link_obj.x-self.left-self.size[0]/2, self.link_obj.y-self.up)
        surf = pygame.transform.scale(self.font.render(getattr(self.link_obj, self.attr_name, "NA"), True, self.col), self.size)

        background.blit(surf, subtract_coords(pos, offset))

    def update(self, background, offset = (0, 0)):
        self.display(background, offset)


#2D Game object affected by gravity, like collectibles or projectiles
class side_fall_obj(game_object):
    def __init__(self, img, x, y, accel):
        super().__init__(img, x, y)

        #Add extra modifiers
        self.accel = accel
        self.falling = True
        
    def fall(self, background, ground_col, offset = (0, 0)):
        max_y = background.get_size()[1]-10
        in_ground = self.in_ground(background, ground_col, offset, None)

        if( self.y > max_y or in_ground):
            if self.y > max_y: self.y = max_y #Dont go below screen
            self.move = (self.move[0], 0) # On Ground
            self.falling = False
        else:
            #print("Falling "+str(self.accel))
            self.move = (self.move[0], self.move[1]+self.accel) # Falling
            self.falling = True

    def in_ground(self, background, ground_col, offset = (0, 0), my_pos = None):
        if my_pos==None: my_pos = self.get_coll_point(True)
        max_coords = background.get_size()

        my_pos = subtract_coords(my_pos, offset)

        if my_pos[0] >= max_coords[0]:
           my_pos = (max_coords[0]-1, my_pos[1])
        if my_pos[1] >= max_coords[1]:
            my_pos = (my_pos[0], max_coords[1]-1)
            #print("Error: '"+str(my_pos)+"' is greater than the bounds of "+str(max_coords))
            #return None
        try:
            return background.get_at(my_pos) in ground_col
        except:
            return None

    def update(self, background, ground_col, offset = (0, 0)): #Trigger after drawing background
        self.fall(background, ground_col, offset)
        super().display(background, offset)

    def get_coll_point(self, is_int = False):
        if is_int:
            return (int(self.x+self.get_size()[0]/2), int(self.y+self.get_size()[1]))
        else:
            return (self.x+self.get_size()[0]/2, self.y+self.get_size()[1])

#Object that fits to slopes, good for characters or enemies
class platformer(side_fall_obj):
    def __init__(self, img, x, y, accel):
        super().__init__(img, x, y, accel)
        self.slope_angle = 0

    def display(self, background, ground_col, offset = (0, 0)):
        s = self.get_size()
        half_w, half_h = s[0]/2, s[1]/2
        if not self.falling and not self.move[0]==0: #Update rotation
            coll_corner_l = (int(self.x), int(self.y+s[1]))
            coll_corner_r = (int(self.x+s[0]), int(self.y+s[1]))

            ground_slope_l = self.move_to_ground_change(background, ground_col, offset, self.in_ground(background, ground_col, offset, coll_corner_l), coll_corner_l)
            ground_slope_r = -self.move_to_ground_change(background, ground_col, offset, self.in_ground(background, ground_col, offset, coll_corner_r), coll_corner_r)

            #Show slope detected
            #pygame.draw.line(background, (0, 0, 0), coll_corner_r, (coll_corner_r[0], coll_corner_r[1]-ground_slope_r), 3)
            #pygame.draw.line(background, (0, 0, 0), coll_corner_l, (coll_corner_l[0], coll_corner_l[1]+ground_slope_l), 3)

            if abs(ground_slope_l)<abs(ground_slope_r):
                self.slope_angle = m.degrees(m.atan2(ground_slope_l, half_w))
            else:
                self.slope_angle = m.degrees(m.atan2(ground_slope_r, half_w))
            #print("SlopeL: "+str(ground_slope_l))
            #print("SlopeR: "+str(ground_slope_r))
            #print("Rotate "+str(self.slope_angle)+" degrees")

        center = (self.x+half_w, self.y+half_h)
        obj_to_display, self.rotated_pos = rotate_img(self.img, center, (half_w, half_h), self.slope_angle)
        background.blit(obj_to_display, subtract_coords(self.rotated_pos, offset))

    def update(self, background, ground_col, display = True, offset = (0, 0), update_collisions = True):
        if update_collisions: self.fall(background, ground_col, offset)

        #Move out of ground because moving left and right might move inside a hill
        if update_collisions and not self.falling and not self.move[0]==0: 
            self.y+=self.move_to_ground_change(background, ground_col, offset)

        #if update_collisions and self.in_ground(background, ground_col, offset, self.get_center(True)):
            #print("Stuck") 

        if display: self.display(background, ground_col, offset) #Use new display function   

    def move_to_ground_change(self, background, ground_col, offset = (0, 0), move_out_of_ground = True, coll_point = None):
        go_up = 0

        if coll_point==None: coll_point = self.get_coll_point(True)

        if move_out_of_ground:
            #print("Moving up")
            
            while coll_point[1] >= 0:
                if self.in_ground(background, ground_col, offset, coll_point): 
                    go_up-=1
                    coll_point = add_coords(coll_point, (0, -1))
                else: break
        else:
            #print("Moving down")
            max_y = background.get_size()[1]-10
            
            while coll_point[1] < max_y:
                if not self.in_ground(background, ground_col, offset, coll_point): 
                    go_up+=1
                    coll_point = add_coords(coll_point, (0, 1))
                else: break
        
        return go_up



#Simple class with velocity to create particle effects
class particle(game_object):
    def __init__(self, x, y, color, init_velocity, life, size, velocity_stop = 0, shape : str = "circle", fade = True, death_size = None, gravity = 0):
        self.x = x
        self.y = y
        self.color = color
        self.move = init_velocity
        self.life = life
        self.start_life = life
        self.start_size = size
        self.size = size
        self.stop = velocity_stop
        self.shape = shape
        self.fade = fade
        self.fall = gravity
        if death_size==None:
            self.death_size = size
        else:
            self.death_size = death_size
    def display(self, background, offset = (0, 0)):
        #Read about transparent drawing on https://stackoverflow.com/questions/6339057/draw-a-transparent-rectangles-and-polygons-in-pygame
        if self.fade:
            target_rect = pygame.Rect(subtract_coords((self.x, self.y), offset), (0, 0)).inflate(self.size*2, self.size*2)
            s = pygame.Surface(target_rect.size, pygame.SRCALPHA)
            #s.set_alpha(self.life*(255/self.start_life))
            if self.shape == "circle":
                pygame.draw.circle(s, (self.color[0], self.color[1], self.color[2], max(0, self.life)*(255/self.start_life)), (self.size, self.size), self.size)
            #Add more shapes
            background.blit(s, target_rect)

        elif self.shape == "circle":
            pygame.draw.circle(background, self.color, subtract_coords((self.x, self.y), offset), self.size)
        #Add more shapes
    def update(self, background, offset = (0, 0)):
        self.display(background, offset)

        self.x+=self.move[0]
        self.y+=self.move[1]
        if self.move[0]>0:
            if self.move[1]>0:
                self.move = ( max(0, self.move[0]-self.stop), max(0, self.move[1]-self.stop)+self.fall)
            else:
                self.move = ( max(0, self.move[0]-self.stop), self.move[1]+self.stop+self.fall)
        else:
            if self.move[1]>0:
                self.move = (self.move[0]+self.stop, max(0, self.move[1]-self.stop)+self.fall)
            else:
                self.move = (self.move[0]+self.stop, self.move[1]+self.stop+self.fall)

        self.size = lerp(self.death_size, self.start_size, self.life/self.start_life)
        self.life-=1
    def pre_update(self):
        pass

#Text with pop!
class pop_message(game_object):
    def __init__(self, pos, life, text, font, color, start_size, end_size = None) -> None:
        self.pos = pos
        self.text = text
        self.font = font
        self.col = color
        self.total_life = life
        self.life = life
        self.start_size = start_size
        self.size = start_size
        if end_size==None: self.end_size = start_size
        else: self.end_size = end_size
    def pre_update(self):
        self.life-=1
        self.size = (int(lerp(self.start_size[0], self.end_size[0], (self.total_life-self.life)/self.total_life)), int(lerp(self.start_size[1], self.end_size[1], (self.total_life-self.life)/self.total_life)))
    def display(self, game_display, offset=(0, 0)):
        my_text = pygame.transform.scale(self.font.render(self.text, True, self.col), self.size)
        #Adjust position for size change
        centered_pos = add_coords(subtract_coords(self.pos, offset), divide_vector(subtract_coords(self.end_size, self.size), 2))
        game_display.blit(my_text, centered_pos)

