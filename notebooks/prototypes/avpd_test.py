#Hayden Donovan
#University of Nevada-Reno
#CS426 Team 25 (Gage Christensen, Daniel Enriquez, Noah Wong, Jared Lam)
#AVPD
#3/18/2021

import avpd_help as avpd
import numpy as np
from os import listdir
from os.path import isfile, join

import sys

TRANSFER_DATA = 1.0

corpus_loc = 'H:/Downloads/2539/download/CORPUS_TXT/'
user1 = ['0001a.txt', '0001b.txt', '0001c.txt', '0001d.txt', '0001e.txt']
u1_str = []

falseDirList = [f for f in listdir(corpus_loc) if isfile(join(corpus_loc, f))]

for i in user1:
    falseDirList.remove(i)

xList, xBar, Phi_list, A, SigmaX, lamb, vList, omegaList, k, PhiHat = avpd.create_AVPD_data()

if len(sys.argv) < 2:
    print("Creating student1 data")
    for i in range(len(user1)-1):
        with open(corpus_loc+user1[i], 'r') as file:
            data = file.read()
            data = avpd.fileToSentenceList(data)
            u1_str.extend(data)
            file.close()

    xList, xBar, Phi_list, A, SigmaX, lamb, vList, omegaList, k, PhiHat = avpd.init_AVPD_data(u1_str, TRANSFER_DATA)
    avpd.saveStudentInfo('Student1', xList, Phi_list, A, SigmaX, lamb, vList, omegaList, PhiHat)

else:
    print("Loading student1 data")
    xList, xBar, Phi_list, A, SigmaX, lamb, vList, omegaList, k, PhiHat = avpd.loadStudentInfo("Student1", TRANSFER_DATA)

#===============================================================


veriEuc = []
for i in xList:
    veriEuc.append(avpd.getNorm((i-xBar)-PhiHat))
true_TH = np.mean(veriEuc) + np.std(veriEuc)/10

print("Model Mean: ", np.mean(veriEuc), '\n\tFlagged False:', avpd.countCriteria(veriEuc, '>', true_TH)/len(veriEuc))


veriString = []
veriStringEuc = []
with open(corpus_loc+'0001e.txt', 'r') as file:
    data = file.read()
    veriString = avpd.fileToSentenceList(data)
    file.close()
for i in veriString:
    veriStringEuc.append(avpd.test_String(i, xBar, PhiHat))

print("Veri Mean: ", np.mean(veriStringEuc), '\n\tFlagged False:', avpd.countCriteria(veriStringEuc, '>', true_TH)/len(veriStringEuc))

falsePosiEuc = []
total_cnt = 0
for i in range(15):

    falseDist = []
    falsePosi = []
    with open(corpus_loc+falseDirList[i], 'r') as file:
        data = file.read()
        falsePosi = avpd.fileToSentenceList(data)
        file.close()
    for j in falsePosi:
        temp = avpd.test_String(j, xBar, PhiHat)
        falsePosiEuc.append(temp)
        falseDist.append(temp)

    print(i,'Mean:', np.mean(falseDist), '\n\tFlagged False:', avpd.countCriteria(falseDist, '>', true_TH)/len(falseDist))

print()
print("\nFP Mean: ", np.mean(falsePosiEuc), '\n\tTotal Flagged:', avpd.countCriteria(falsePosiEuc, '>', true_TH)/len(falsePosiEuc))

avpd.saveList(veriEuc, 'model_mean.txt')
avpd.saveList(veriStringEuc, 'veri_mean.txt')
avpd.saveList(falsePosiEuc, 'false_mean.txt')

veriEuc = avpd.removeFromListIf(veriEuc, '<', true_TH)
veriStringEuc = avpd.removeFromListIf(veriStringEuc, '<', true_TH)
falsePosiEuc = avpd.removeFromListIf(falsePosiEuc, '<', true_TH)

print()
true_TH = np.mean(veriEuc) + np.std(veriEuc)/10
print("New Model Mean:", np.mean(veriEuc),'\n\tFlagged False:',avpd.countCriteria(veriEuc, '>', true_TH)/len(veriEuc))
print("Veri Mean:", np.mean(veriStringEuc),'\n\tFlagged False',avpd.countCriteria(veriStringEuc, '>', true_TH)/len(veriStringEuc))
print("Total FP Mean:", np.mean(falsePosiEuc),'\n\tFlagged False',avpd.countCriteria(falsePosiEuc, '>', true_TH)/len(falsePosiEuc))

