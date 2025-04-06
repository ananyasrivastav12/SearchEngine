import gzip
import json
import math
import sys
    
def read(inputFile):
    file = json.load(gzip.open(inputFile, 'rt'))
    file = file["corpus"]
    for i in file:
        i["text"] = i["text"].split(" ")
        i["text"] = list(filter(None, i["text"]))
    return file

def indexing(inputFile):
    docs = read(inputFile) 
    numD = len(docs)
    d = {}

    for l in range(numD):
        dic = {}
        for word in docs[l]['text']:
            if word not in dic:
                dic[word] = 1
            else:
                dic[word] += 1

        d[docs[l]['sceneId']] = dic
    return d

def indexing2(inputFile):
    docs = read(inputFile) 
    numD = len(docs)
    d = {}

    for l in range(numD):
        dic = {}
        for word in docs[l]['text']:
            if word not in dic:
                dic[word] = 1
            else:
                dic[word] += 1

        d[docs[l]['playId']] = dic
    return d

def docLength(inputFile):
    docs = read(inputFile) 
    numD = len(docs)
    sum = 0
    dic = {}

    for l in range(numD):
        dic[docs[l]['sceneId']] = len(docs[l]['text'])
        sum += len(docs[l]['text'])

    avg = sum/numD
    return dic, avg

def query(queriesFile):
    q = []
    queries = open(queriesFile, 'rt')
    querie = queries.readlines()
    for i in querie:
        q.append(i.strip('\n').split('\t'))

    return q

def BM25(queryy, index):
    query = []
    quer = []
    for x in range(3, len(queryy)):
        quer.append(queryy[x])

        if queryy[x] in query:
            pass
        else: 
            query.append(queryy[x])

    fi = {}
    for doc in index:
        f = {}
        for q in quer:
            if q in index[doc]:
                f[q] = index[doc][q]
            else:
                f[q] = 0

        fi[doc] = f
    
    qfi = {}
    for q in quer:
        print(quer)
        if q not in qfi:
            qfi[q] = 0
        if q in qfi:
            qfi[q] += 1
    
    niCount = {}
    for q in quer:
        ni = 0
        for doc in index:
            if q in index[doc]:
                ni += 1
        niCount[q] = ni

    N = len(read(inputFile))
    k1 = 1.8
    k2 = 5
    b = 0.75
    dl, avdl = docLength(inputFile)
    dic = {}
    
    for doc in index:
        sum = 0
        for q in query:
    
            K = k1*((1 - b)+ (b*dl[doc]/avdl))
            x = math.log((N - niCount[q] + 0.5)/(niCount[q] + 0.5))
            y = ((k1 + 1)* fi[doc][q])/(fi[doc][q]+K)
            z = ((k2 + 1)*qfi[q])/(qfi[q]+k2)

            prod = x*y*z
            
            sum += prod

        if sum !=0:
            dic[doc] = sum

    return dic


def ql(queryy, index):
    query = []
    for x in range(3, len(queryy)):
        query.append(queryy[x])

    c = 0
    D = {}
    for doc in index:
        D[doc] = 0
        for word in index[doc]:
            c += index[doc][word]
            D[doc] += index[doc][word]

    cqi = {}
    for q in query:
        cqi[q]=0
        for doc in index:
            if q in index[doc]:
                cqi[q] += index[doc][q]

    fqid = {}
    for doc in index:
        f = {}
        for q in query:
            f[q] = 0
            if q in index[doc]:
                f[q] = index[doc][q]
        fqid[doc] = f

    μ=300

    dic = {}
    for doc in index:
        sum = 0
        r=0
        for q in query:
            x = (fqid[doc][q] + (μ*(cqi[q]/c)))
            y = (D[doc] + μ)
            prod = math.log(x/y)
            sum += prod

            if fqid[doc][q] == 0:
                r+=1

        if r == len(query):
            pass
        else:
            dic[doc] = sum
    return dic

def write(outputFile, query, inputFile):

    f = open(outputFile, 'w') 
    
    for q in query:
        if q[1] == "scene":
            index = indexing(inputFile)
        if q[1] == "play":
            index = indexing2(inputFile)

        if q[2] == "bm25":
            l = BM25(q, index)
            l = sorted(l.items(), key=lambda item: item[1], reverse= True)
            counter = 0
            for i in range(len(l)):
                counter+=1
                f.write(q[0] + "\t"+ "skip" + "\t" + str(l[i][0])+ "\t" + str(i+1) + "\t" + str(l[i][1]) +"\t" + "ananyasrivas\n")
                if counter == 100:
                    break
                
        if q[2] == "ql":
            m = ql(q, index)
            m = sorted(m.items(), key=lambda item: item[1], reverse= True)
            p = 0
            for i in range(len(m)):
                p+=1
                f.write(q[0] + "\t"+ "skip" + "\t" + str(m[i][0])+ "\t" + str(i+1) + "\t" + str(m[i][1]) +"\t" + "ananyasrivas\n")
                if p == 100:
                    break        
                

def main(inputFile, queriesFile, outputFile):
    queryy = query(queriesFile)
    write(outputFile, queryy, inputFile)

        
if __name__ == '__main__':
    # Read arguments from command line, or use sane defaults for IDE.
    argv_len = len(sys.argv)
    inputFile = sys.argv[1] if argv_len >= 2 else 'shakespeare-scenes.json.gz'
    queriesFile = sys.argv[2] if argv_len >= 3 else 'trainQueries.tsv'
    outputFile = sys.argv[3] if argv_len >= 4 else 'train.results'

    main(inputFile, queriesFile, outputFile)