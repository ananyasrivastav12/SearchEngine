import collections
import gzip
import math
import sys

def filetodict(input):
    urlsDict = {}
    dic = {}

    urls = gzip.open(input, 'rt').readlines()
    b = set()

    for url in urls:
        key, value = url.strip('\n').split('\t')
        
        b.add(value)

        if(key not in urlsDict):
            urlsDict[key] = set()
        
        if key not in dic:
            dic[key] = 0

        if value not in dic:
            dic[value]  = 1
        else:
            dic[value] = dic[value] + 1

        urlsDict[key].add(value)
    return urlsDict, b, dic

def inlinks(input):
    links, b, dic = filetodict(input)
    dict = {}

    pages = set()

    for i in links:
        pages.add(i)
        for j in links[i]:
                if j not in pages:
                    pages.add(j)

    return pages, links, dic
        
def pagerank(input, lambda_val, tau,P,L,c):

    N = len(P)

    oldPR = {}
    newPR = {}
    for i in P:
        oldPR[i] = 1/N

    while converge(oldPR, newPR, tau):
        if newPR:
            oldPR = newPR.copy()
        for i in P:
            newPR[i] = lambda_val/N
        x = 0
        for p in P:
            Q = set() if p not in L else L[p]
            if len(Q) > 0:
                for q in Q:
                    newPR[q] = newPR[q] + (1-lambda_val)*oldPR[p]/len(Q) 
            else:
                x = x + (1-lambda_val)*oldPR[p]/N
        for s in newPR:
            newPR[s] = newPR[s] + x
    return newPR            

def converge(old, new, tau):
    boole = True
    if len(new) == 0:
        return True
    x = 0
    for i in new:
        x += (new[i]-old[i])*(new[i]-old[i])

    x = math.sqrt(x)
    if x < tau:
        boole = False
    return boole

def writeToInlinks(inputFile, x,y,z,inlinksFile):

    f = open(inlinksFile, 'w') 

    counter = collections.Counter(z)
    most = counter.most_common(100)

    c = 1 
    for i in most:
        f.write(i[0] + "\t" + str(c) + "\t" + str(i[1]) + "\n")
        c += 1
    f.close()

def writePagerank(inputFile, pr,pagerankFile):

    f = open(pagerankFile, 'w') 
    
    counter = collections.Counter(pr)
    most = counter.most_common(100)

    rank = 1

    for i in most:
        f.write(i[0] + "\t" + str(rank) + "\t" + str(i[1]) + "\n")
        rank += 1
    f.close()


def main(inputFile, lambda_val, tau, inlinksFile, pagerankFile, k):
    p,l,c = inlinks(inputFile)
    pr = pagerank(inputFile, lambda_val, tau, p,l,c )
    writePagerank(inputFile, pr,pagerankFile)
    writeToInlinks(inputFile, p,l,c,inlinksFile)

if __name__ == '__main__':
         # Read arguments from command line; or use sane defaults for IDE.
     
    argv_len = len(sys.argv)
    inputFile = sys.argv[1] if argv_len >= 2 else "links.srt.gz"
    lambda_val = float(sys.argv[2]) if argv_len >=3 else 0.2
    tau = float(sys.argv[3]) if argv_len >=4 else 0.005
    inLinksFile = sys.argv[4] if argv_len >= 5 else "inlinks.txt"
    pagerankFile = sys.argv[5] if argv_len >= 6 else "pagerank.txt"
    k = int(sys.argv[6]) if argv_len >= 7 else 100
    main(inputFile, lambda_val, tau, inLinksFile, pagerankFile, k)



