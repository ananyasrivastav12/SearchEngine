import gzip
import json
import os
import sys

    
def read(inputFile):
    file = json.load(gzip.open(inputFile, 'rt'))
    file = file["corpus"]
    for i in file:
        i["text"] = i["text"].split(" ")
        i["text"] = list(filter(None, i["text"]))
    return file

def indexing(input):
    file = read(input)
    dic = dict()
    for i in file:
        text = i['text']
        for j in range(len(text)):
            if text[j] not in dic:
                dic[text[j]] = [(i['playId'], i['sceneId'], j)]
            else:
                dic[text[j]].append((i['playId'], i['sceneId'], j)) 
    return dic

def query(queriesFile):
    q = []
    queries = open(queriesFile, 'rt')
    querie = queries.readlines()
    for i in querie:
        q.append(i.strip('\n').split('\t'))
    return q

def boole(dic, boolea):
    a = set()
    b = set()
    dictio = {}
    
    for d in dic:
        for i in dic[d]:
            a.add(i)
    if boolea == "and":
        for items in a:
            dictio[items] = 0
        for d in dic:
            for i in dic[d]:
                if i in dictio:
                    dictio[i] += 1
                
                if dictio[i] == len(dic):
                    b.add(i)
        return b    
    return a


def documentAtATime(query, index):
    dicti = {}
    dic_final = {}
    for q in range(3, len(query)):
        r = query[q].split()
        dicti[q-3] = r
        dic_final[q-3] = set()

    dictionary = {}
    dic = {}
    a = set()
    first = []

    for m in dicti:
        for l in dicti[m]:
            dictionary[l] = index[l]
    
    for q in range(3, len(query)):
        r = query[q].split()
        l = len(r[0])-1
        
    for i in dicti:
        first.append(dicti[i][0])

    for i in range(len(first)):
        for j in dictionary[first[i]]:
            play = j[0]
            scene = j[1]
            position = j[2]
            count = 0
            for k in range(len(dicti[i])):
                new_pos = position + k
                word = dicti[i][k]
                if not ((play, scene, new_pos) in dictionary[word]):
                    count +=1

            if  count == 0:
                if query[1] == 'play':
                    dic_final[i].add(play)
                if query[1] == 'scene':
                    dic_final[i].add(scene)
    return list(boole(dic_final, query[2]))


def write(query, lst, outputFolder):
    file = open(outputFolder+ "/" + query[0] + ".txt",'w')
    lst = sorted(lst)
    for i in lst:
        file.write(i+"\n")
    file.close()


def main(inputFile, queriesFile, outputFolder):
    quer = query(queriesFile)
    index = indexing(inputFile)
    for i in quer:
        write(i, documentAtATime(i, index), outputFolder)


if __name__ == '__main__':
    # Read arguments from command line, or use sane defaults for IDE.
    argv_len = len(sys.argv)
    inputFile = sys.argv[1] if argv_len >= 2 else 'shakespeare-scenes.json.gz'
    queriesFile = sys.argv[2] if argv_len >= 3 else 'trainQueries.tsv'
    outputFolder = sys.argv[3] if argv_len >= 4 else 'results/'
    if not os.path.isdir(outputFolder):
        os.mkdir(outputFolder)
    main(inputFile, queriesFile, outputFolder)

def average(read):
    sum = 0
    count = 0
    for i in read:
        sum = sum + len(i['text'])
        count += 1
    avg = sum / count

