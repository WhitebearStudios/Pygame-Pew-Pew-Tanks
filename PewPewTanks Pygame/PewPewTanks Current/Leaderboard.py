from Basic_functions import insert_dict_in_dict
from FileRW import *
from tkinter import *
from tkinter import font
from json import loads

def sort(leaderboard : dict, greatest_first = True):
    if len(leaderboard)<2: return leaderboard

    sort_dict = dict()
    i=0

    for key in leaderboard:
        val = leaderboard[key]
        if type(val)==list: compare1 = val[0]
        else: compare1 = val
        for i in range(len(sort_dict)):
            val_at_index = sort_dict[list(sort_dict.keys())[i]]
            if type(val_at_index)==list: compare2 = val_at_index[0]
            else: compare2 = val_at_index
            if(compare1<compare2 and not greatest_first) or (compare1>compare2 and greatest_first): break

        if len(sort_dict)>0:
            val_at_index = sort_dict[list(sort_dict.keys())[i]]
            if type(val_at_index)==list: compare2 = val_at_index[0]
            else: compare2 = val_at_index
            if(compare1>compare2 and not greatest_first) or (compare1<compare2 and greatest_first): i+=1

        sort_dict = insert_dict_in_dict({key : val}, sort_dict, i)
        
    return sort_dict

def leaderboard_from_file(file_name, skip_block = 0, greatest_first = True, file_encrypted = False):
    leaderboard = get_datas_from_file(file_name, 2, True, skip_block, file_encrypted)
    return sort(leaderboard, greatest_first)

def leaderboard_from_json(file_name, greatest_first = True):
    file = open(file_name, "r")
    print(file.read())
    leaderboard = loads(file.read())
    return sort(leaderboard, greatest_first)

def leaderboard_window(file_name : str, unit : str, json = False, skip_block = 0, greatest_first = True, file_encrypted = False):
    if json: leaderboard_dict = leaderboard_from_json(file_name, skip_block, greatest_first)
    else: leaderboard_dict = leaderboard_from_file(file_name, skip_block, greatest_first, file_encrypted)
    leaderboard_str_list = [None]*len(leaderboard_dict)
    i=0
    for key in leaderboard_dict:
        leaderboard_str_list[i] = str(leaderboard_dict[key][0])+" "+unit+" (+"+str(leaderboard_dict[key][1])+") - "+key
        i+=1

    root = Tk()
    root.geometry("550x400")
    #Customize this for other projects
    header_img = PhotoImage(file="bgCropped.gif")
    header_img = header_img.subsample(4, 5)

    h_scroll = Scrollbar(root, orient="horizontal")
    v_scroll = Scrollbar(root, orient="vertical")
    
    h_scroll.pack(side=BOTTOM, fill=X)
    v_scroll.pack(side=LEFT, fill=Y)

    big_font = font.Font(family = "Comic Sans MS", size=35, weight="bold")
    norm_font = font.Font(family = "Comic Sans MS", size = 12)

    #Customize this for other projects
    header = Canvas(root, width=600, height=200, background = "cyan")
    header.pack(fill=X, expand=True)
    header.create_image(12, 0, image=header_img, anchor="nw")
    header.create_text(170, 35, text="Leaderboard:", font=big_font)

    #Customize this for other projects
    t = Text(root, width = 50, height=6, wrap=NONE, font=norm_font, background="medium spring green",
                xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)
    for line in leaderboard_str_list: t.insert(END, line+"\n")

    t.pack()

    root.mainloop()

#leaderboard_window("PewPewTanksScores.txt", "Damage", file_encrypted=True)