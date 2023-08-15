import math
import sys

def read(input):
    file = open(input, "rt")
    lines = []
    for line in file:
        lines.append(line.split())
    return lines

def data(input):
    file = read(input)
    dic = {}
    queries = []

    for line in file:
        if line[0] not in queries:
            queries.append(line[0])

        if line[0] not in dic:
            dic[line[0]] = {}

        (dic[line[0]])[line[2]] = [line[3], line[4]]
    return queries, dic


def qrel(input):
    data = read(input)
    dic = {}
    for line in data:
        if line[0] not in dic:
            dic[line[0]] = {}
        dic[line[0]][line[2]] = line[3]
    return dic


def rr(query): #ok
    min = math.inf
    rel = 0
    for id in dat[query]:
        if id not in qr[query]:
            rel = 0
        else:
            rel = float(qr[query][id])

        if rel > 0:
            m = float(dat[query][id][0])
            if m < min:
                min = m
            return 1/min
    return 0
            
def Precision(query, x):
    count = 0
    rel = 0
    if x == 0:
        return 0
    for id in dat[query]:
        if int(dat[query][id][0]) <= x:
            if id not in qr[query]:
                rel = 0
            else:
                rel = int(qr[query][id])
            if rel > 0:
                count += 1
    return count/x

def Precision15(query):
    return Precision(query, 15)


def totalRel(query):
    count = 0
    for id in qr[query]:
        if int(qr[query][id]) > 0:
            count += 1
    return count
            

def Recall(query):
    count = 0
    for id in dat[query]:
        if int(dat[query][id][0]) <= 20:
            if id not in qr[query]:
                rel = 0
            else:
                rel = int(qr[query][id])
            if rel > 0:
                count += 1
    return count/totalRel(query)


def Precision25(query):
    return Precision(query, 25)

def Recall25(query):
    count = 0
    for id in dat[query]:
        if float(dat[query][id][0]) <= 25:
            if id not in qr[query]:
                rel = 0
            if id in qr[query]:
                rel = float(qr[query][id])
            if rel > 0:
                count += 1
    return count/totalRel(query)

def F1(query):
    r = Recall25(query)
    p = Precision25(query)

    if r+p == 0:
        return 0
    return 2*r*p/(r+p)

def AP(query):
    sum = 0
    t = totalRel(query)

    for id in dat[query]:
        if id in qr[query]:
            if int(qr[query][id]) > 0:
                r = int(dat[query][id][0])
                sum += Precision(query,r)

    return sum/t



def dcg75(query):
    dcg = 0

    for id in dat[query]:
        if id in qr[query]:
            r = int(dat[query][id][0])
            if r==1:
                dcg += float(qr[query][id])
            if (r > 1 and r <= 75):
                dcg += float(qr[query][id])/math.log2(r)
    
    return dcg
            

def idcg(query):

    lst = []
    idcg = 1

    for id in qr[query]:
        lst.append(int(qr[query][id]))
    else:
        lst.append(0)

    liist = sorted(lst, reverse= True)

    for i in range(0, 75):
        if i == 0:
            idcg = liist[i]
        else:
            idcg += liist[i]/math.log2(i+1)
    return idcg

def ndcg(query):
    return dcg75(query)/idcg(query)

def all():
    sumRR = 0
    sumNDCG = 0
    sumP = 0
    sumR = 0
    sumF1 = 0
    sumAP = 0
    dic = {}

    for query in q:
        sumRR += rr(query)
        sumNDCG += ndcg(query)
        sumP += Precision15(query)
        sumR += Recall(query)
        sumF1 += F1(query)
        sumAP += AP(query)

    dic['rr'] = sumRR/len(q)
    dic['ndcg'] = sumNDCG/len(q)
    dic['p'] = sumP/len(q)
    dic['r'] = sumR/len(q)
    dic['f1'] = sumF1/len(q)
    dic['ap'] = sumAP/len(q)

    return dic

def write(outputFile):
    f = open(outputFile, 'w') 

    for query in q:
        f.write('NDCG@75'+'\t' +'\t'+ query + "\t" +'\t' + str(ndcg(query)) + "\n")
        f.write('RR'+'\t' +'\t' + query + "\t" +'\t'+ str(rr(query))+ "\n")
        f.write('P@15'+'\t'+'\t' + query + "\t" +'\t'+ str(Precision15(query))+ "\n")
        f.write('R@20'+'\t' +'\t'+ query + "\t" +'\t'+ str(Recall(query))+ "\n")
        f.write('F1@25'+'\t' +'\t'+ query + "\t" +'\t'+ str(F1(query))+ "\n")
        f.write('AP'+'\t' +'\t'+ query + "\t" +'\t'+ str(AP(query))+ "\n")

    x = all()
    f.write('NDCG@75'+'\t' +'\t' + "all" + "\t" +'\t'+ str(x['ndcg'])+ "\n")
    f.write('MRR'+'\t' +'\t'+ "all" + "\t" +'\t'+ str(x['rr'])+ "\n")
    f.write('P@15'+'\t' +'\t'+ "all" + "\t" +'\t'+ str(x['p'])+ "\n")
    f.write('R@20'+'\t' +'\t'+ "all" + "\t" +'\t'+ str(x['r'])+ "\n")
    f.write('F1@25'+'\t' +'\t'+ "all" + "\t" +'\t'+ str(x['f1'])+ "\n")
    f.write('MAP'+'\t' +'\t'+ "all" + "\t" +'\t'+str(x['ap'])+ "\n")
    
    f.close()

if __name__ == '__main__':
    # Read arguments from command line, or use sane defaults for IDE.
    argv_len = len(sys.argv)
    runFile = sys.argv[1] if argv_len >= 2 else 'simple.trecrun'
    qrelsFile = sys.argv[2] if argv_len >= 3 else 'qrels'
    outputFile = sys.argv[3] if argv_len >= 4 else 'simple.eval'

qr = qrel(qrelsFile) 
q, dat = data(runFile)


def main():
    write(outputFile)
main()
