#Hayden Donovan
#University of Nevada-Reno
#CS426 Team 25 (Gage Christensen, Daniel Enriquez, Noah Wong, Jared Lam)
#AVPD
#4/11/2021

import avpd_help as avpd
import numpy as np
from os import listdir
from os.path import isfile, join
import sys


TRANSFER_DATA = 0.95
PERCENT_CUTOFF = 0.3

corpus_loc = ''

std_divisor = 5
if len(sys.argv) > 1 and (avpd.listContains(['U'], sys.argv[len(sys.argv)-1]) or avpd.listContains(['H'], sys.argv[len(sys.argv)-1]))==False:
    std_divisor = float(sys.argv[len(sys.argv)-1])

#dirList = [f for f in listdir(corpus_loc) if isfile(join(corpus_loc, f))]

#I want to test the first 5 authors against eachother, lets see
u1 = ['0001b.txt', '0001c.txt', '0001d.txt', '0001a.txt']
u2 = ['0002a.txt', '0002b.txt']
#u3 = ['0003a.txt', '0003b.txt', '0003c.txt', '0003d.txt', '0003e.txt', '0003f.txt', '0003g.txt', '0003h.txt', '0003i.txt', '0003j.txt', '0003k.txt', '0003l.txt', '0003p.txt']
u4 = ['0004a.txt', '0004b.txt', '0004c.txt', '0004d.txt']
u5 = ['0005a.txt', '0005b.txt', '0005c.txt']
u6 = ['0006a.txt', '0006b.txt', '0006c.txt']
u7 = ['0007a.txt', '0007b.txt']
u8 = ['0008a.txt', '0008b.txt']


Hamilton = ['Hamilton1.txt', 'Hamilton2.txt', 'Hamilton3.txt', 'Hamilton4.txt']
Jay = ['Jay (1).txt', 'Jay (2).txt', 'Jay (3).txt', 'Jay (4).txt']
Madison = ['Madison (1).txt', 'Madison (2).txt', 'Madison (3).txt', 'Madison (4).txt']

uList = []

if len(sys.argv) > 1 and avpd.listContains(['H'], sys.argv[len(sys.argv)-1]):
    print("Initiating Hamilton Mode")
    uList = [Hamilton, Jay, Madison]
elif len(sys.argv) > 1 and avpd.listContains(['U'], sys.argv[len(sys.argv)-1]):
    print("Initiating User Corpus Mode")
    uList = [u1, u2, u5, u6]
    corpus_loc = 'H:/Downloads/2539/download/CORPUS_TXT/'
else:
    print("Loading from last save...")


#Push these lists onto their own list
uStrings = []
uXlist = []


if len(sys.argv) > 1 and (avpd.listContains(sys.argv, 'U') or avpd.listContains(['H'], sys.argv[len(sys.argv)-1])):
    for u in range(len(uList)):
        #make a list for each u_x
        uStrings.append([])
        for i in range(len(uList[u])):
            #make a list for each u_x_y
            uStrings[u].append([])
            doc_loc = ''
            if(len(sys.argv) > 1 and avpd.listContains(['H'], sys.argv[len(sys.argv)-1])):
                doc_loc = uList[u][i]
            else:
                doc_loc = corpus_loc+uList[u][i]
            with open(doc_loc, 'r') as file:
                data = file.read()
                uStrings[u][i] = (avpd.fileToSentenceList(data))
                file.close()
    avpd.saveList(uStrings, 'uStrings.txt')

else:
    uStrings = avpd.loadList('uStrings.txt')
    
print("Building xLists [", end='')
for user in range(len(uStrings)):
    uXlist.append([])
    print('=',end='',flush=True)
    for doc in range(len(uStrings[user])):
        uXlist[user].append([])
        for sent in uStrings[user][doc]:
            uXlist[user][doc].append(avpd.make_X(sent))
print(']\n')

#Create Student Data for each student and compare everyone against eachother
cnt = 0
verificationIndex = 0

print("Choose Model: Input in range")
print("Choose document for verification: Input in range or 0 to ignore")
print("Choose document for unkown verification: Input in range or 0 to ignore")
print("========================================================================")

while True:

    cnt = input(str('Which user to model [1, ' + str(len(uXlist)) + '] : '))
    if(cnt=='q'):
        break
    else:
        try:
            cnt = int(cnt)-1
        except:
            print('ERR: Out of bounds; picking first element')
            cnt = 0
    print("Calculating u",cnt+1,"...", sep='', flush=True)

    u = uXlist[cnt]

    #Initiate vars
    xList, xBar, Phi_list, A, SigmaX, lamb, vList, omegaList, k, PhiHat = avpd.create_AVPD_data()

    verificationIndex = input(str("What document for verification [1, " + str(len(u)) + "] : ")) 
    try:
        verificationIndex = int(verificationIndex)
        if verificationIndex != -1:
            verificationIndex = verificationIndex-1
        if verificationIndex > len(u)-1:
            verificationIndex = len(u)-1
            #-1 suggests that we are not using a known validator
    except:
        print("\tERR: using default value")
        verificationIndex = len(u)-1

    #Oh my god... I wrote unKOWN for every single one
    #...
    #***KOWN***
    unkownVerificationIndex = input(str("What document for unkown verification [1, " + str(len(u)) + "] - {"+str(verificationIndex+1)+"} : ")) 
    try:
        unkownVerificationIndex = int(unkownVerificationIndex)
        if unkownVerificationIndex != -1:
            unkownVerificationIndex = unkownVerificationIndex-1
            #print("minus 1", unkownVerificationIndex)
        if unkownVerificationIndex != -1 and (unkownVerificationIndex > len(u)-1 or unkownVerificationIndex == verificationIndex):
            print("invalid number")
            for i in range(len(u)-1):
                if i != verificationIndex:
                    unkownVerificationIndex = i
                    break
        
    except:
        print("\tERR: using default value")
        for i in range(len(u)-1):
            if i != verificationIndex:
                unkownVerificationIndex = i
                break

    #In this u, add all but the last doc
    for i in range(len(u)):
        if i != verificationIndex and i!=unkownVerificationIndex:
            for j in u[i]:
                xList.append(j)

    #Build model with supplied data
    xBar, Phi_list, A, SigmaX, lamb, vList, omegaList, k, PhiHat = avpd.init_from_xList(xList, TRANSFER_DATA)


    #SHOW PHI HAT==========================================
    #print(PhiHat)
    #SHOW PHI HAT==========================================


    modelDist = []
    falseDist = []
    veriDist = []
    uVeriDist = []

    #Getting model distances
    for i in xList:
        modelDist.append(avpd.getNorm((i-xBar) - PhiHat))
    decisionBoundary = np.mean(modelDist) + np.std(modelDist)/std_divisor
    print("\nDecision Boundary 1:\t", decisionBoundary, sep='')

    #Getting verification distances
    if verificationIndex != -1:
        for i in u[verificationIndex]:
            veriDist.append(avpd.getNorm((i - xBar) - PhiHat))

    if unkownVerificationIndex != -1:
        for i in u[unkownVerificationIndex]:
            uVeriDist.append(avpd.getNorm((i - xBar) - PhiHat))

    #Getting intruder distances
    countFP = 0
    for i in range(len(uXlist)):
        
        if i != cnt:
            #Add a row for each intruder
            falseDist.append([])
            for j in range(len(uXlist[i])):
                falseDist[countFP].append([])
                for k in uXlist[i][j]:
                    #Add each string to the new rows
                    falseDist[countFP][j].append(avpd.getNorm((k- xBar)- PhiHat))
            countFP += 1
        
    modelDist_GT = avpd.removeFromListIf(modelDist, '<', decisionBoundary)
    veriDist_GT = []
    if verificationIndex != -1:
        veriDist_GT = avpd.removeFromListIf(veriDist, '<', decisionBoundary)
    uVeriDist_GT = avpd.removeFromListIf(uVeriDist, '<', decisionBoundary)
    falseDist_GT = []
    for i in range(len(falseDist)):
        falseDist_GT.append([])
        for j in range(len(falseDist[i])):
            falseDist_GT[i].append([])
            falseDist_GT[i][j] = avpd.removeFromListIf(falseDist[i][j], '<', decisionBoundary)

    decBound_GT = np.mean(modelDist_GT) + np.std(modelDist_GT)/std_divisor
    print("Decision Boundary 2:\t", decBound_GT, sep='')
    print("Model % =\t\t", avpd.flaggedPercentage(modelDist_GT, decBound_GT), sep='')
    veriPercentage = 0
    if(verificationIndex != -1):
        veriPercentage = avpd.flaggedPercentage(veriDist_GT, decBound_GT)
    uVeriPercentage = 0
    if(unkownVerificationIndex != -1):
        uVeriPercentage = avpd.flaggedPercentage(uVeriDist_GT, decBound_GT)
    print("Veri (", verificationIndex,") % =\t\t", veriPercentage, " / ",len(veriDist_GT), sep ='')
    print("U-Veri (", unkownVerificationIndex,") % =\t\t", uVeriPercentage, " / ",len(uVeriDist_GT), sep ='')

    val = ''
    while val!='q':
        val = input("Try cutoff %:")
        if(val=='q'):
            break
        try:
            val = float(val)
        except:
            val = veriPercentage * 1.1
            print("ERR: Using cutoff %\t", val, sep='')
                   
        falseNeg = 0
        falsePos = 0
        totalIntruders = 0

        if(uVeriPercentage > val):
            falseNeg = 1

        for i in falseDist_GT:
            for j in i:
                totalIntruders += 1
                if(avpd.flaggedPercentage(j, decBound_GT) < val):
                    falsePos += 1

        print('  False Negatives:\t', falseNeg,'/1', sep='', flush = True)
        print('  False Positives:\t', falsePos,'/',totalIntruders, '\n', sep='', flush=True)

        print(PhiHat)

    print()