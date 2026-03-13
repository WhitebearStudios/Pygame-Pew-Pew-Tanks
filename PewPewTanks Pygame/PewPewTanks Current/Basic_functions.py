import math as m
 
 #Basic functions
def is_int(num):
    try:
        test = 0+int(num)
    except:
        print(str(num)+" is not a number!")
        return False
    else:
        return True
def is_binary(bi):
    try:
        test = 0+int(bi)
    except:
        print(str(bi)+" is not binary!")
        return False
    else:
        for char in bi:
            if not (char=="0" or char=="1"):
                print(str(bi)+" is not binary!")
                return False
        return True
def check_option_is_valid(option_entered, options):
    for option in options:
        if option_entered == option:
            return True, option
    for option in options:
        if option_entered == option.lower():
            return True, option
    for option in options:
        if option_entered == option.upper():
            return True
    print("'"+option_entered+"' is not a valid option!")
    return False, None
def list_to_and_str(fun_list):
    fun_str = ""
    for item in fun_list:
        fun_str+=str(item)+" and "
    return fun_str[:-5]
def every_two_chars_to_list(fun_string):
    #print("Looking through "+multi_charge)
    i=0
    this_str = ""
    charge_list = [None]*(int(len(fun_string)/2))
    for char in fun_string:
        #print("Char is "+char+" i is "+str(i))
        this_str+=char
        if i%2==1:
            charge_list[int((i+1)/2-1)] = this_str
            this_str = ""
        i+=1
    return charge_list
    
def str_to_list(fun_str, errors_are_fine = False):
    this_item = ""
    fun_list = []
    read_item = False
    error = False
    ignore_list = ["[", "]", " "]
    for char in fun_str:
        if char in ignore_list:
            pass
        elif char=="'" or char=='"':
            if read_item:
                fun_list.append(this_item)
                this_item = ""
                read_item = False
            else:
                read_item = True
        elif char==",":
            if is_int(this_item):
                fun_list.append(int(this_item))
                this_item = ""
            elif read_item:
                error = True
                break
        else:
            if read_item or is_int(char):
                this_item+=char
            else:
                error = True
                break
    if error:
        if not errors_are_fine: print("An error occured converting "+fun_str+" to a list")
        return None
    else:
        if is_int(this_item): fun_list.append(int(this_item))
        return fun_list

def print_dict(my_dict):
    keys = list(my_dict.keys())
    vals = list(my_dict.values())
    for i in range(len(keys)):
        print(str(keys[i])+" : "+str(vals[i]))
        
def dict_items_to_str(dict):
    keys = list(dict.keys())
    vals = list(dict.values())
    new_dict = {}
    for i in range(len(dict)):
        new_dict.update({str(keys[i]) : str(vals[i])})
        
    return new_dict
        
def comp_dicts(dict1, dict2):
    if not len(dict1)==len(dict2): 
        print("return 1")
        return False
    keys = list(dict1.keys())
    vals = list(dict1.values())
    for i in range(len(keys)):
        key = keys[0]
        try: val = dict2[key]
        except: 
            print("return 2")
            return False
        if not val in vals:  
            print("return 3")  
            return False
        else: 
            keys.remove(key)
            vals.remove(val)
     
    print("return 4")
    return len(keys)==0 and len(vals)==0

def closest_space_index(fun_str : str, start_index : int = 0):
    if start_index>len(fun_str): return len(fun_str)
    for i in range(start_index, len(fun_str)):
        if fun_str[i]==" ": break
    space_dst_forward = i-start_index
    i=start_index
    while i>0 and abs(i-start_index)<=space_dst_forward:
        if fun_str[i]==" ": break
        else: i-=1
    space_dst_backward = abs(i-start_index)
    if space_dst_forward<space_dst_backward: return space_dst_forward+start_index
    else: return space_dst_backward+start_index

def insert_dict_in_dict(dict_to_insert : dict, orig_dict : dict, i : int):
    new_dict = dict()

    if len(orig_dict)==0: return dict_to_insert
    if i==len(orig_dict):
        orig_dict.update(dict_to_insert)
        return orig_dict

    for ii in range(len(orig_dict)):
        if ii==i:
            for key in dict_to_insert:
                new_dict.update({key : dict_to_insert[key]})
            key_at_index = list(orig_dict.keys())[ii]
            new_dict.update({key_at_index : orig_dict[key_at_index]})
        else:
            key_at_index = list(orig_dict.keys())[ii]
            new_dict.update({key_at_index : orig_dict[key_at_index]})
    return new_dict
        
def get_player_name(players): #Returns lowest available player number
    pn=1
    name_taken = True
    while name_taken:
        name_taken = False
        for p in players:
            if p.player_name == "Player "+str(pn):
                name_taken = True
                break
        if name_taken: pn+=1
    return "Player "+str(pn)

def check_item_pair(list_to_check: list, it1, it2):
    i=0
    for item in list_to_check:
        if i==len(list_to_check)-1: return False #If the first item is the last item in the list then the second item cant be after
        if item==it1:
            if list_to_check[i+1]==it2: return True
        i+=1
    return False

def remove_returns(fun_str):
    new_str = ""
    for char in fun_str:
        if not char=="\n": new_str+=char
    return new_str

def basic_comp_strs(str1, str2):
    i=0
    for char in str1:
        if i>=len(str2):
            print("Out of range")
            break
        print("Line "+str(i+1)+": "+str(char==str2[i]))
        i+=1

def compress_num(num):
    compressed = ""
    for b in num:
        if str(b)=="\n": 
            compressed+="\n"
            continue
        prev_char = None
        i=0
        is_zero = b[0]=="0"
        for char in str(b):
            if not ((char=="0" and is_zero) or (char=="1" and not is_zero)):
                compressed+=str(i)+prev_char
                is_zero = char=="0"
                i=0
            i+=1
            prev_char = char
        compressed+=str(i)+prev_char
        is_zero = char=="0"
        i=0
    return compressed
def unpack_num(cnum):
    num = ""
    i=0
    #Newlines mess up pairs of numbers used in loop
    #print(str(len(cbi)/2+xtra))
    for x in range(int(len(cnum)/2+cnum.count("\n")/2)):
        if cnum[i]=="\n": 
            num+="\n"
            i+=1
            continue
        for x in range(int(cnum[i])):
            num+=cnum[i+1]
        i+=2
    return num