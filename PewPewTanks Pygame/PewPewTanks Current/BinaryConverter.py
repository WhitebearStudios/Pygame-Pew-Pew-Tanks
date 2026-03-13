from Basic_functions import check_option_is_valid, is_binary, is_int, remove_returns, str_to_list
from math import pow

def num_to_bi(num):
    if type(num)==list:
        i=0
        for n in num:
            if not num[i]=="\n": num[i] = int(n)
            i+=1
    else: num = [int(num)]

    bi_str_l = [None]*len(num)
    b_i = 0
    for n in num:
        if n=="\n": 
            bi_str_l[b_i] = n
            b_i+=1
            continue
        i = 7
        bi_str = ""
        while n>0:
            if pow(2, i)>n:
                bi_str+="0"
                #print(str(m.pow(2, i))+" is bigger than "+str(n))
            else:
                n-=int(pow(2, i))
                bi_str+="1"
                #print("Subtracted "+str(m.pow(2, i)))
            i-=1
        while i>=0:
            bi_str+="0"
            i-=1
        bi_str_l[b_i] = bi_str
        b_i+=1
    if len(bi_str_l)==1: return bi_str_l[0]
    else: return bi_str_l

def bi_to_num(bi, split_bytes = True):
    if split_bytes:
        i=(len(remove_returns(bi))-1)%8
    else:
        i=len(remove_returns(bi))-1
    num = 0
    nums = [None]*int(len(remove_returns(bi))/8+bi.count("\n"))
    num_counter = 0
    for char in bi:
        if char=="\n":
            nums[num_counter] = "\n"
            num=0
            num_counter+=1
            continue
        if char=="1":
            num+=pow(2, i)
        i-=1
        if i<0:
            i=7
            nums[num_counter] = int(num)
            num=0
            num_counter+=1
    if len(nums)==1:
        return nums[0]
    else:
        return nums
def str_to_num(fun_str):
    num_list = [None]*len(fun_str)
    i=0
    for char in fun_str:
        if not char=="\n": num_list[i] = ord(char)
        else: num_list[i] = char
        i+=1
    return num_list
def num_to_uni(num):
    return chr(num)
def num_list_to_message(num_list : list):
    str_list = [None]*num_list.count("\n")
    fun_str = ""
    i=0
    for num in num_list:
        if num=="\n": 
            if fun_str=="": fun_str = "\n" #Line empty, let file management know
            str_list[i] = fun_str
            fun_str = ""
            i+=1
        else: fun_str+=num_to_uni(num)
    if len(str_list)==1: return str_list[0]
    else: return str_list

def compress_bi(bi : list): #number binary starts with follwed by number of occurences of alternating numbers ex: 01001010 = 01121111\t
    compressed = ""
    for b in bi:
        if b=="\n": 
            compressed+="\n"
            continue
        i=0
        is_zero = b[0]=="0"
        compressed+=b[0]
        for char in b:
            if not ((char=="0" and is_zero) or (char=="1" and not is_zero)):
                compressed+=str(i)
                is_zero = not is_zero
                i=0
            i+=1
        compressed+=str(i)+"\t"
    return compressed
def unpack_bi(cbi):
    bi = ""
    first_char = True
    zeroes = None
    for char in cbi:
        if char=="\n": 
            bi+="\n"
            first_char = True
        elif char=="\t":
            first_char = True
        elif first_char:
            zeroes = char=="0"
            first_char = False
        else:
            if zeroes==None: print("Error: order of operations bad unpacking binary")
            if zeroes: add = "0"
            else: add = "1"
            for x in range(int(char)):
                bi+=add
            zeroes = not zeroes
    return bi

def encrypt(plain_text : str):
    return compress_bi(num_to_bi(str_to_num(plain_text)))
def decrypt(compressed_binary : str):
    return num_list_to_message(bi_to_num(unpack_bi(compressed_binary)))

'''
#Demo for taking plain text and going through the steps

f = open("PewPewTanksScores.txt", "r")
bi = num_to_bi(str_to_num(f.read()))
f.close()
c = compress_bi(bi)
bis = ""
for bims in bi: bis+=bims
print("Original: "+bis)
print("Compressed: "+c)
print("Compressing saved "+str(len(bis)-len(c))+" chars!")
u = unpack_bi(c)
print("Unpack: "+u)
if bis==u: print("Hooray!!!")
else: print("Grrrrr")

#f = open("PewPewTanksScores.txt", "w")
#f.write(c)
#f.close()

bts = num_list_to_message(bi_to_num(u))
print("Highscores: "+bts)
'''

'''
#Demo for reading encrypted file
f = open("PewPewTanksScores.txt", "r")
c = f.read()
f.close()
u = unpack_bi(c)
bts = num_list_to_message(bi_to_num(u))
print("Highscores: "+str(bts))
'''

'''
#Demo for fixing files with spaces instead of tabs
strshfskdhfhsdfksdf = ""
file = open("PewPewTanksScores.txt", "r")
hs = encrypt(file.read())
file.close()
i=0
chars_left = len(hs)
while chars_left>0:
    if hs[i]==" ": 
        strshfskdhfhsdfksdf+="\t"
        while hs[i]==" ": 
            i+=1
            chars_left-=1
    else: 
        strshfskdhfhsdfksdf+=hs[i]
        i+=1
        chars_left-=1
file = open("PewPewTanksScores.txt", "w")
file.write(strshfskdhfhsdfksdf)
file.close()
'''

'''
file = open("PewPewTanksScores.txt", "r")
hs = encrypt(file.read())
file.close()
file = open("PewPewTanksScores.txt", "w")
file.write(hs)
file.close()
'''

#----------------------------------------------------------User Input Stuff---------------------------------------------------
def use():
    options = ["a", "b", "c"]
    user_input = ""
    while options == options:
        is_valid = False
        while not is_valid:
            user_input = input("Would you like to [a]convert a binary number to decimal, [b] convert a decimal(s) to binary number, or [c] convert a string to decimals?")
            if user_input=="exit": break
            is_valid = check_option_is_valid(user_input, options)

        if user_input=="exit": break

        if user_input==options[0]:
            is_valid = False
            while not is_valid:
                num_to_convert = input("Please type in a binary number: ")
                try:
                    num_to_convert = str_to_list(num_to_convert)
                except:
                    is_valid = is_binary(num_to_convert)
                else:
                    for num in num_to_convert:
                        is_valid = is_binary(num)
                        if not is_valid: 
                            print("An item in your list is not binary!")
                            break
            if type(num_to_convert)==list:
                num = []
                for this_bi in num_to_convert:
                    num.append(bi_to_num(this_bi))
            else:
                num = bi_to_num(num_to_convert, True)
            print("Your number is "+str(num))
            options = ["y", "n"]
            is_valid = False
            while not is_valid:
                user_input = input("Would you like to lookup this decimal(s) in Unicode? (y or n): ")
                is_valid = check_option_is_valid(user_input, options)
            if user_input=="y":
                if type(num)==list:
                    message = ""
                    for n in num:
                        message+=chr(n)
                    print("Your secret message is "+message)
                else:
                    print("Your character is "+chr(num))
            
        elif user_input==options[1]:
            is_valid = False
            while not is_valid:
                num_to_convert = input("Please type in a number: ")
                try:
                    num_to_convert = str_to_list(num_to_convert)
                except:
                    is_valid = is_int(num_to_convert)
                else:
                    for num in num_to_convert:
                        is_valid = is_int(num)
                        if not is_valid: 
                            print("An item in your list is not a number!")
                            break
            if type(num_to_convert)==list:
                bi_num = []
                for num in num_to_convert:
                    bi_num.append(num_to_bi(num))
            else:
                bi_num = num_to_bi(num_to_convert)
            print("Your binary number is "+str(bi_num))

        elif user_input==options[2]:
            string_to_convert = input("Please type in something to convert: ")
            print(str( str_to_num(string_to_convert)))