import collections
from curses.ascii import isalnum, isalpha
from itertools import count
from operator import indexOf
import re
from selectors import PollSelector
from string import punctuation 
from collections import Counter
import matplotlib.pyplot as plt

A = "tokenization-input-part-A.txt"
B = "tokenization-input-part-B.txt"

def read(x):
    file = open(x, "rt")
    readFile = file.read()
    return readFile

def abbreviate(x):
    readFile = read(x)
    a=''

    for letter in range(0, len(readFile)):
        char = readFile[letter]
        if (char == "'"):
            a = readFile.replace("'", "")

        if char == ".":
            if( readFile[letter+1].isalnum()):
                if not readFile[letter-2].isalnum():
                    b = a.replace(".", "")
                
    return b

def punctuate(x):
    f = abbreviate(x)
    a = f
    for letter in range(0, len(f)):
        
        if (f[letter] == "M" and f[letter+1] == "r" and f[letter+2] == "s" and f[letter+3] == "." and f[letter+4] == " "): #Mrs.
            a = re.sub(r"(?<=Mrs)\.\s(?=[A-Za-z])", "", a)
            
        elif (f[letter] == "M" and f[letter+1] == "r" and f[letter+2] == "." and f[letter+3] == " "): #Mr.
            a = re.sub(r"(?<=Mr)\.\s(?=[A-Za-z])", "", a)

    a = re.sub(f"[{re.escape(punctuation)}]", " ", a)

    return a


def tokenize(x): 
    a = punctuate(x)       
    tokens = a.lower().split()
    return tokens

def stop(x):
    stopList = open("stopwords.txt", "rt")
    stopList = stopList.read().split()

    tokens = tokenize(x)

    stopped = []

    for token in tokens:
        if not token in stopList:
            stopped.append(token)

    return stopped

def stemminga(x):
    stopped = stop(x)
    vowel = ["a","e","i","o", "u"]

    for word in range(0, len(stopped)-1):
        l = len(stopped[word])
        
        if stopped[word].endswith("sses"):
            stopped[word] = stopped[word].replace("sses", "ss")
    
        elif (stopped[word].endswith("ied") and len(stopped[word]) > 4):
            stopped[word] = stopped[word].replace("ied", "i")

        elif (stopped[word].endswith("ies") and len(stopped[word]) > 4):
            stopped[word] = stopped[word].replace("ies", "i")
        
        elif (stopped[word].endswith("ss") or stopped[word].endswith("us")):
            stopped[word] = stopped[word]

        elif (stopped[word].endswith("s") and stopped[word-1] not in vowel):
            stopped[word] = stopped[word].replace("s", "")

    return stopped

def short(str):

    #CVCV, CVC, VCV, or VC

    if len(str) >= 2:
        tf = False

        if re.search(r'[bcdfghjklmnpqrstvwxyz]*[aeiou]+[bcdfghjklmnpqrstvwxyz]+', str) != None: #cvc
            tf = True
        elif re.search(r'[bcdfghjklmnpqrstvwxyz]]*[aeiou]+[bcdfghjklmnpqrstvwxyz]]+[aeiou]*', str) != None: #cvcv
            tf = True
        elif re.search(r'[aeiou]+[bcdfghjklmnpqrstvwxyz]+[aeiou]*', str) != None: #vcv
            tf = True
        elif re.search(r'[aeiou]+[bcdfghjklmnpqrstvwxyz]+', str) != None: 
            tf = True

    return tf

def stemmingb(x):
    stopped = stemminga(x)
    vowel = ["a","e","i","o", "u"]
    boole = False

    for word in range(0, len(stopped)-1):
        l = len(stopped[word])

        if (stopped[word].endswith("eedly") and (stopped[word][l-6] not in vowel) and (stopped[word][l-7] in vowel)):
            stopped[word] = stopped[word].replace("eedly", "ee")

        elif (stopped[word].endswith("eed") and (stopped[word][l-6] not in vowel) and (stopped[word][l-7] in vowel)):
            stopped[word] = stopped[word].replace("eed", "ee")

        elif (stopped[word].endswith("ingly")):
            for i in stopped[word]:
                if i in vowel:
                    stopped[word] = stopped[word].replace("ingly", "")
                    boole = True

        elif (stopped[word].endswith("edly")):
            for i in stopped[word]:
                if i in vowel:
                    stopped[word] = stopped[word].replace("edly", "")
                    boole = True

        elif (stopped[word].endswith("ing")):
            for i in stopped[word]:
                if i in vowel:
                    stopped[word] = stopped[word].replace("ing", "")
                    boole = True

        elif (stopped[word].endswith("ed")):
            for i in stopped[word]:
                if i in vowel:
                    stopped[word] = stopped[word].replace("ed", "")
                    boole = True

        else: boole = False

        if boole == True:
            if len(stopped[word]) > 2:
                l = len(stopped[word])

                if (stopped[word].endswith("at") or stopped[word].endswith("bl") or stopped[word].endswith("iz")):
                    stopped[word] += "e"

                elif (stopped[word][l-2] == stopped[word][l-1]):
                    if (stopped[word][l-1] != "l" and stopped[word][l-1] != "s" and stopped[word][l-1] != "z"):
                        stopped[word] = stopped[word].replace(stopped[word][l-1], "")

                elif (short(stopped[word])):
                   stopped[word] = stopped[word] + "e"

    return stopped


def writeA():
    file = open("tokenized-A.txt", "wt")
    
    output = stemmingb(A)
    for item in output:
        file.write(item)
        file.write("\n")
    
    
def write300():
    file = open("terms-B.txt", "wt")
    
    output = stemmingb(B)

    counter = collections.Counter(output)

    most = counter.most_common(300)

    for item in most:

       file.write(item[0] + " " + str(item[1]))
       file.write("\n")
    

def graph():
    z = stemmingb(B)
    i = 0
    arr1 = []
    arr2 = []
    plot = set()
    for word in z:
        i += 1
        plot.add(word)
        arr1.append(len(plot))
        arr2.append(i)
    plt.plot(arr2, arr1)
    plt.ylabel("Words in Vocabulary")
    plt.xlabel("Words in Collection")
    plt.show()


def main():
    val = input("Which file do you want? A or B?")

    if(val == "A"):
        return stemmingb(A)

    if(val == "B"):
        return stemmingb(B)


if __name__ == "__main__":
   print(main())

#writeA()
#write300()

