#Handy Functions for getting data from a file and storing it in a list or dictionary.
#List of each datas, each line List format: data1 tab data2 tab data3...
#                                           data1 tab data2 tab data3...
#List of dicts each line Dict Format: data1:data2
#                                     data1:data2

#One line in between blocks, two lines at end of file

from json import dumps, loads
from Basic_functions import str_to_list
from BinaryConverter import decrypt, encrypt

def get_datas_from_line(line, datas_to_find, dict_format = False):
    datas = [None]*datas_to_find
    data_counter = 0
    this_data = ""
    for char in line:
        if ((char=="\t" or char==" " or char=="\n") and not dict_format and data_counter<datas_to_find) or (char==":" and dict_format):
            datas[data_counter] = this_data
           
            data_counter+=1
            this_data = ""
        else:
            this_data+=char

    if dict_format:
        datas[1] = this_data[:-1]
        #See if value is list
        try_list = str_to_list(datas[1])
        if not try_list==None: datas[1] = try_list #List conversion succeeded
        return {datas[0] : datas[1]}
    else:
        return datas
       
       
def get_datas_from_file(file_name, datas_to_find, dict_format = False, skip_block = 0, file_encrypted = False):
    #print("Getting data from "+file_name+"...")
    file = open(file_name, "r")
    if file_encrypted: str_datas = decrypt(file.read())
    else: str_datas = file.readlines()
    file.close()
   
    #Get which lines to read from
    start_line, num_lines = get_to_block(str_datas, skip_block)
               
    #print(str(start_line)+" "+str(num_lines))
    if dict_format:
        datas = {}
    else:
        datas = [None]*num_lines
    li=1
    for line in str_datas:
        if li==start_line+num_lines:
            break
        elif li>=start_line:
            if dict_format:
                datas.update(get_datas_from_line(line, 2, True))
            else:
                #print("Data from line "+str(i)+": "+str(get_datas_from_line(line, dict_format, datas_to_find)))
                datas[li-start_line] = get_datas_from_line(line, datas_to_find)


        li+=1
    return datas


def get_to_block(str_datas, skip_block = 0):
    start_line = 1
    num_lines = 0
    li=1
    blocks_to_go = skip_block
    
    for line in str_datas:
        if line=="\n":
            blocks_to_go-=1
            if blocks_to_go==0:
                start_line = li+1 #Line after this one is start of next block
            if blocks_to_go<0:
                num_lines = li-start_line
                break
        li+=1


    return start_line, num_lines

#Datas to write should be list of lists or dictionary
def write_to_file(file_name, datas_to_write : list or dict, json = False, skip_block = 0, append_block = True, file_encrypted = False):
    #So function doesn't crash later
    if len(datas_to_write)==0: 
        print("You must provide something to write to the file.")
        return

    if json:
        file = open(file_name, "w")
        file.write(dumps(datas_to_write))
        file.close()
        return

    file = open(file_name, "r")
    str_datas = file.readlines()
    file.close()
    
    start_line, num_lines = get_to_block(str_datas, skip_block)
    
    str_to_write = ""
    if type(datas_to_write)==dict:
        for key in datas_to_write:
            str_to_write+=str(key)+":"+str(datas_to_write[key])+"\n"
    else:
        for line in datas_to_write:
            for item in line:
                str_to_write+=str(item)+"\t"
            str_to_write+="\n"

    if file_encrypted: 
        #Convert to binary
        str_to_write = encrypt(str_to_write)

    if start_line+num_lines<=1: #File is empty
        file = open(file_name, "a")
        file.write(str_to_write)
    else:
        #Get contents of file before and after insertion
        file = open(file_name, "w")
        before_insert = ""
        after_insert = ""
        li=1
        for line in str_datas:
            if li==1: 
                #All data in same file block should be same format (will mess up reading file)
                if file_encrypted: check_line = decrypt(line)
                else: check_line = line
                check_datas = datas_to_write
                if (not list(get_datas_from_line(check_line, 2, True).keys())==[None] and type(datas_to_write)==list) or (list(get_datas_from_line(check_line, 2, True).keys())==[None] and (type(datas_to_write)==dict or (type(check_datas)==str  and  ":" in check_datas))): 
                    print("Error: expected %s file format, got wrong format" % str(type(datas_to_write)))
                    break
            if (li<=start_line+num_lines and append_block) or (li<start_line and not append_block):
                before_insert+=line
            elif append_block or li>start_line+num_lines:
                after_insert+=line
            li+=1
        if before_insert[-2:]=="\n\n" and append_block: before_insert = before_insert[:-1]
        file.write(before_insert+str_to_write+"\n"+after_insert)
    file.close()

#Good for leaderboards
def update_dict_in_file(file_name, key, new_val, only_if = 2, #update the key... 0=if less 1=if greater
                                                    json = False, skip_block = 0, file_encrypted = False):
    if json: 
        file = open(file_name, "r")
        my_dict = loads(file.read())
        file.close()
    else: my_dict = get_datas_from_file(file_name, 2, True, skip_block, file_encrypted=file_encrypted)

    found_key = False
    for ikey in my_dict:
        if ikey==key and (only_if==2 or (only_if==0 and key<ikey) or (only_if==1 and key>ikey)):
            my_dict[key] = new_val
            found_key = True
            break
    if not found_key: my_dict.update({key : new_val})

    write_to_file(file_name, my_dict, json, skip_block, file_encrypted=file_encrypted)

def dict_key_in_file(file_name, key, json = False, skip_block = 0, file_encrypted = False):
    if json: 
        file = open(file_name, "r")
        print(file.read())
        my_dict = loads(file.read())
        file.close()
    else: my_dict = get_datas_from_file(file_name, 2, True, skip_block, file_encrypted=file_encrypted)
    #print("Highscores: "+str(my_dict))

    found_key = False
    for ikey in my_dict:
        if ikey==key:
            found_key = True
            break
    return found_key, my_dict.get(key, None)

#Function tests
#write_to_file("b.txt", [["Hi", "THERE"], ["HI", "THERE"]], 2)
#print(str(get_datas_from_file("b.txt", 2, False, 2)))
#update_dict_in_file("g.txt", "ghfgh", 45, 0)
