from math import ceil
from Basic_functions import closest_space_index, get_player_name

import pygame
from game_object import min

file_name = "PewPewTanksScores.txt"

black = (0,0,0)
white = (255,255,255)
light_gray = (200,200,200)
light_light_gray = (245, 245, 245)

#SFPixelate font by ShyFoundry Fonts https://www.1001fonts.com/users/shyfonts/ free for personal use (not used)
#pixelFJ8pt1 font by MBommeli https://www.1001fonts.com/users/flashjunior/ free for commercial use
big_font = pygame.font.Font("pixelFJ8pt1__.TTF", 55)
med_font = pygame.font.Font("pixelFJ8pt1__.TTF", 35)
small_font = pygame.font.Font("pixelFJ8pt1__.TTF", 20)
    
class Button:
    def __init__(self, rect : pygame.Rect, color, link_index = None, border = 0, border_color = None, action = None, 
            text : str = None, font : pygame.font.Font = None, text_color = None) -> None:
        self.link_index = link_index
        self.rect = rect
        self.col = color
        self.border = border
        self.b_col = border_color
        self.action = action
        self.text = text
        self.font = font
        self.text_col = text_color
    def display(self, surf : pygame.Surface):
        if self.rect.collidepoint(pygame.mouse.get_pos()): 
            #print("Hover")
            highlight_col = (min(self.col[0]+50, 255), min(self.col[1]+50, 255), min(self.col[2]+50, 255))
            pygame.draw.rect(surf, highlight_col, self.rect)
        else: pygame.draw.rect(surf, self.col, self.rect)

        if self.border>0: pygame.draw.rect(surf, self.b_col, self.rect, self.border) #Button border
        text_border = self.rect.width/30
        if not self.text==None: surf.blit(self.font.render(self.text, True, self.text_col), (self.rect.left+text_border+self.border, self.rect.top+text_border+self.border))
    def erase(self, bg, bg_col):
        pygame.draw.rect(bg, bg_col, self.rect)
        pygame.display.update(self.rect)
class player_selection:
    def __init__(self, players, buttons) -> None:
        self.rect = pygame.Rect(10, 412+len(players)*35, 580, 35)
        self.checkbox_rect = pygame.Rect(self.rect.left+60, self.rect.top+5, 25, 25)
        self.text_rect = pygame.Rect(self.rect.left+90, self.rect.top+5, 480, 25)
        self.ent_name = False
        self.is_ai = False
        self.player_name = get_player_name(players)
        buttons.append(Button(pygame.Rect(self.rect.left+3, self.rect.top+3, 25, 25), light_gray, None, 3, black, None, "-", small_font, black)) #Button to delete player

    def display(self, surf):
        global small_font
        pygame.draw.rect(surf, light_gray, self.rect)
        pygame.draw.rect(surf, black, self.rect, 3)

        surf.blit(small_font.render("AI", True, black), (self.rect.left+35, self.rect.top+8))
        pygame.draw.rect(surf, black, self.checkbox_rect)
        if self.is_ai>0: 
            if self.is_ai==1: col = light_light_gray
            else: col = (255, 0, 0)
            pygame.draw.rect(surf, col, pygame.Rect(self.checkbox_rect.left+5, self.checkbox_rect.top+5, 15, 15))

        if self.ent_name: pygame.draw.rect(surf, light_light_gray, self.text_rect)
        if not self.player_name == "": surf.blit(small_font.render(self.player_name, True, black), (self.text_rect.left, self.text_rect.top+5))
    def erase(self, bg, bg_col):
        pygame.draw.rect(bg, bg_col, self.rect)
        pygame.display.update(self.rect)
class pop_up:
    def __init__(self, text : str, can_proceed : bool = False, b2_text : str = "Proceed", b2_link_index = None, rect : pygame.Rect = pygame.Rect(100, 100, 400, 400), color = light_gray, 
                 border = 4, border_color = black, 
                 font : pygame.font.Font = small_font, text_color = black, fit_height_to_text = True) -> None:
        self.link = b2_link_index
        self.rect = rect
        self.col = color
        self.border = border
        self.b_col = border_color
        self.text = text
        self.font = font
        self.text_col = text_color
        self.proceed = can_proceed
        self.b2_text = b2_text

        if fit_height_to_text:
            self.rect.height = 8+ceil(len(text)/25+1)*22
    def display(self, surf : pygame.Surface, pop_up_buttons):
        pygame.draw.rect(surf, self.col, self.rect)
        if self.border>0: pygame.draw.rect(surf, self.b_col, self.rect, self.border) #Rectangle border

        text_border = self.rect.width/40
        if not self.text==None: 
            if len(self.text)<25:
                surf.blit(self.font.render(self.text, True, self.text_col), (self.rect.left+text_border+self.border, self.rect.top+text_border+self.border))
            else: #Fun text formatting code
                text_left = self.text
                num_rows = ceil(len(text_left)/25)
                for y in range (num_rows):
                    split = closest_space_index(text_left, 25)
                    my_y = y*22
                    if y==0: omit_space = 0
                    else: omit_space = 1
                    surf.blit(self.font.render(text_left[omit_space:split], True, self.text_col), (self.rect.left+text_border+self.border, self.rect.top+text_border+self.border+my_y))
                    text_left = text_left[split:]

        if self.proceed:
            if self.b2_text=="Proceed": w = 115
            elif self.b2_text=="Surprise Me": w = 165
            x1 = (115+35+w)/2
            x2 = x1+115+35
            pop_up_buttons.append(Button(pygame.Rect(300-x1, self.rect.top+self.rect.height+5, 115, 35), light_gray, None, 3, black, None, "Go Back", small_font, black))
            pop_up_buttons.append(Button(pygame.Rect(35+x2, self.rect.top+self.rect.height+5, w, 35), light_gray, self.link, 3, black, None, self.b2_text, small_font, black))
        else: pop_up_buttons.append(Button(pygame.Rect(255, self.rect.top+self.rect.height+5, 70, 35), light_gray, None, 3, black, None, "Okay", small_font, black))

play_button = Button(pygame.Rect(10, 130, 105, 70), light_gray, None, 6, black, None, "Play", med_font, black)
add_players_button = Button(pygame.Rect(220, 412, 160, 35), light_gray, None, 3, black, None, "Add Player", small_font, black)