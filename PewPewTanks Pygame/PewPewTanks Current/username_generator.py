from FileRW import get_datas_from_file
from random import randint

source_name = "adjsnouns.txt"
adjectives = get_datas_from_file(source_name, 1)
nouns = get_datas_from_file(source_name, 3, False, 1)

def rand_username():
    a = adjectives[randint(0, len(adjectives)-1)][0]
    mod = randint(0, 3)
    if mod==0: a = a.upper()
    elif mod==1: a = a.lower()

    i1 = randint(0, len(nouns)-1)
    i2 = randint(0, 2)
    n = nouns[i1][i2]
    mod = randint(0, 3)
    if mod==0: n = n.upper()
    elif mod==1: n = n.lower()

    if randint(0, 2)==0: b = "_"
    else: b=""

    if randint(0, 2)==0:
        if randint(0, 2)==0: b2 = "_"
        else: b2=""

        num = str(randint(0, 10000))
    else:
        b2 = ""
        num = ""

    return a+b+n+b2+num

#print(rand_username())