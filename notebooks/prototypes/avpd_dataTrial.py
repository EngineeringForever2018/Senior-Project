import avpd_help as avpd
import numpy as np
import sys

std_divisor = 10
if(len(sys.argv) > 1 and avpd.listContains(['N', 'GT', 'LT'], sys.argv[len(sys.argv)-1])==False):
    std_divisor = float(sys.argv[len(sys.argv)-1])


veriEuc = avpd.loadList('model_mean.txt')
veriStringEuc = avpd.loadList('veri_mean.txt')
falsePosiEuc = avpd.loadList('false_mean.txt')

true_TH = np.mean(veriEuc) + np.std(veriEuc)/std_divisor

if(len(sys.argv) > 1 == False or
   len(sys.argv) > 1 and (avpd.listContains(sys.argv, 'GT') or avpd.listContains(sys.argv, 'LT')) == False or
   len(sys.argv) > 1 and (avpd.listContains(sys.argv, 'N'))):
    print('\n***Source Outputs***')
    print("New Model Mean:", np.mean(veriEuc),'\n\tFlagged False:',avpd.countCriteria(veriEuc, '>', true_TH)/len(veriEuc))
    print("Veri Mean:", np.mean(veriStringEuc),'\n\tFlagged False',avpd.countCriteria(veriStringEuc, '>', true_TH)/len(veriStringEuc))
    print("Total FP Mean:", np.mean(falsePosiEuc),'\n\tFlagged False',avpd.countCriteria(falsePosiEuc, '>', true_TH)/len(falsePosiEuc))

if(len(sys.argv) > 1 and avpd.listContains(sys.argv, 'GT')):
    veriEuc_GT = avpd.removeFromListIf(veriEuc, '<', true_TH)
    veriStringEuc_GT = avpd.removeFromListIf(veriStringEuc, '<', true_TH)
    falsePosiEuc_GT = avpd.removeFromListIf(falsePosiEuc, '<', true_TH)
    true_GT = np.mean(veriEuc_GT) + np.std(veriEuc_GT)/std_divisor

    print('\n***Greater Than TH Outputs***')
    print("New Model Mean:", np.mean(veriEuc_GT),'\n\tFlagged False:',avpd.countCriteria(veriEuc_GT, '>', true_GT)/len(veriEuc_GT))
    print("Veri Mean:", np.mean(veriStringEuc_GT),'\n\tFlagged False',avpd.countCriteria(veriStringEuc_GT, '>', true_GT)/len(veriStringEuc_GT))
    print("Total FP Mean:", np.mean(falsePosiEuc_GT),'\n\tFlagged False',avpd.countCriteria(falsePosiEuc_GT, '>', true_GT)/len(falsePosiEuc_GT))

if(len(sys.argv) > 1 and avpd.listContains(sys.argv, 'LT')):
    veriEuc_LT = avpd.removeFromListIf(veriEuc, '>', true_TH)
    veriStringEuc_LT = avpd.removeFromListIf(veriStringEuc, '>', true_TH)
    falsePosiEuc_LT = avpd.removeFromListIf(falsePosiEuc, '>', true_TH)
    true_LT = np.mean(veriEuc_LT) + np.std(veriEuc_LT)/std_divisor

    print('\n***Less Than TH Outputs***')
    print("New Model Mean:", np.mean(veriEuc_LT),'\n\tFlagged False:',avpd.countCriteria(veriEuc_LT, '>', true_LT)/len(veriEuc_LT))
    print("Veri Mean:", np.mean(veriStringEuc_LT),'\n\tFlagged False',avpd.countCriteria(veriStringEuc_LT, '>', true_LT)/len(veriStringEuc_LT))
    print("Total FP Mean:", np.mean(falsePosiEuc_LT),'\n\tFlagged False',avpd.countCriteria(falsePosiEuc_LT, '>', true_LT)/len(falsePosiEuc_LT))

