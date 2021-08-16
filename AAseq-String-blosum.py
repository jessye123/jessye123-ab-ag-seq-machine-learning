import math
import operator
import numpy as np
import csv
from Bio.SubsMat import MatrixInfo


def score_match(pair, matrix):
    if pair not in matrix:
        return matrix[(tuple(reversed(pair)))]
    else:
        return matrix[pair]
    
def euclidean_Distance(point1, point2, length):    
    if (point1[length-1].upper() != point2[length-1].upper()):
        return 1000  # not same antigen, return large distance
    
    distance = 0
    for x in range(1,4):  # H chain dis
        distance += pow(string_Distance(point1[x], point2[x]), 2)      
    for x in range(5,8):
        distance += pow(string_Distance(point1[x], point2[x]), 2)
        
    return math.sqrt(distance)

def get_k_Neighbors(trainingSet, testPoint, k):
    distances = []
    length = len(testPoint)-1
    for x in range(len(trainingSet)):
        dist = euclidean_Distance(testPoint, trainingSet[x], length)
        distances.append((trainingSet[x], dist))
    distances.sort(key=operator.itemgetter(1))
    
    neighbors = []
    for x in range(k):      
        neighbors.append(distances[x])
    return neighbors

def get_Resp(neighbors):
    class_Votes = {}
    numb_class = {}
 
    for x in range(len(neighbors)):
        if neighbors[x][1]==0:
            return neighbors[x][0][-1]
        else:
            resp = neighbors[x][0][-1]
            if resp in class_Votes:
                class_Votes[resp] += 1/(neighbors[x][1]*neighbors[x][1]) 
                numb_class[resp] += 1     ##this is weighted kNN algorithms1numb_class[resp] += 1
            else:
                class_Votes[resp] = 1/float(neighbors[x][1]*neighbors[x][1])
                numb_class[resp] = 1

    for x in class_Votes:
        class_Votes[resp] = class_Votes[resp]/numb_class[resp]

    sorted_Votes = sorted(class_Votes.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_Votes[0][0]



def get_Accu(testSet, predictions):
	correct = 0
	for x in range(len(testSet)):
		if testSet[x][-1] == predictions[x]:
			correct += 1
	return (correct/float(len(testSet))) * 100.0

def Oldstring_Distance(string1, string2):
    n = len(string1)
    m = len(string2)    
    if (n == 0): 
        return m
    if (m == 0): 
        return n
    
    dmatrix = [[0 for x in range(m)] for y in range(n)] 
    
    for i in range(n):
        dmatrix[i][0] = i
    for j in range(m):
        dmatrix[0][j] = j
        
    for i in range(1,n):
        si = string1[i-1]     
        for j in range(1,m):
            sj = string2[j-1]        
            if (si.upper() == sj.upper()):
                cost = 0
            else:
                cost = 1
            
            dmatrix[i][j] = min(min (dmatrix[i-1][j]+3, dmatrix[i][j-1]+3), dmatrix[i-1][j-1] + cost)     
    return dmatrix[n-1][m-1]

# use string Distance with Blosum 62
def string_Distance(string1, string2):
    string1 = string1.strip()
    string2 = string2.strip()
    n = len(string1)
    m = len(string2)    
    if (n == 0): 
        return m
    if (m == 0): 
        return n
    
    dmatrix = [[0 for x in range(m)] for y in range(n)] 
    
    for i in range(n):
        dmatrix[i][0] = i
    for j in range(m):
        dmatrix[0][j] = j
        
    for i in range(1,n):
        si = string1[i-1]     
        for j in range(1,m):
            sj = string2[j-1]        
            if (si.upper() == sj.upper()):
                cost = 0
            else:
                blosum = MatrixInfo.blosum62
                pair = (si, sj)
                myscore = score_match(pair, blosum)
                
                pairi = (si, si)
                myscorei = score_match(pairi, blosum)
                
                pairj = (sj, sj)
                myscorej = score_match(pairj, blosum)
                
                testcost = (myscorei+myscorej)/2 - myscore
                cost = testcost/2
                
            dmatrix[i][j] = min(min (dmatrix[i-1][j]+3, dmatrix[i][j-1]+3), dmatrix[i-1][j-1] + cost)     
    return dmatrix[n-1][m-1]


# ********start main program ************
print ("hello Jessica")

#load the csv, Only load related datas
mydata=[]
with open('data_combine.csv',newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        mydata.append(row)
mydata=mydata[1:]

# 2 neighbors, can change to different number for test&plot
k = 2
print("Leave one out validation for %d nearest neighbors:" %k)


predictions=[]
TP = 0
TN = 0
FP = 0
FN = 0

for x in range(len(mydata)):
    traingData = np.delete(mydata,(x),0) 
    #print (x)
    neighbors = get_k_Neighbors(traingData, mydata[x], k)
    #print (neighbors)
    result = get_Resp(neighbors)
    
    predictions.append(result)
    mistake = ''
    myre= repr(result)[1]
    
    if (repr(result) != repr(mydata[x][-1])):
        mistake += 'mistake'
        if (myre == 'Y'):
            FP += 1
        else:
            FN += 1   
    else: 
        if (myre == 'Y'):
            TP += 1
        else:
            TN += 1           
        
    print( str(x) + '> predicted=' + repr(result) + ', actual=' + repr(mydata[x][-1]) + mistake +repr(mydata[x][-2]))
    
accuracy = get_Accu(mydata, predictions)
print('K='+repr(k)+', Accuracy: ' + repr(accuracy) + '%')

print("done")