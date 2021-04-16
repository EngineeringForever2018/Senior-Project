import spacy
import numpy as np
from numpy import linalg as LA

nlp = spacy.load("en_core_web_sm")

posVector = [
    "ADJ",
    "ADP",
    "ADV",
    "AUX",
    "CCONJ",
    "DET",
    "INTJ",
    "NOUN",
    "NUM",
    "PART",
    "PRON",
    "PROPN",
    "PUNCT",
    "SCONJ",
    "SPACE",
    "SYM",
    "VERB",
    "X",
]
Phi_size = len(posVector) * len(posVector)


# TERM was removed from posVector because well... it's always going to end with a punctuation that's kind of a given
# ideally, i want to allow users to submit entire paragraphs for this to work, so it'll work on a paragraph basis
# but also let it work on smaller scale defined by us later on which means i need:


class tSentence:  # for transcribed sentence. May be used for general purpose isntead of just sentences to avoid issues w/ proper noun punctuation and whatnot

    data = []
    size = 0

    def __init__(self, string):
        doc = nlp(str(string))
        for i in doc:
            self.data.append(tWord(i.text, i.pos_))
            self.size += 1

    def printPOS(self):
        for i in range(self.size):
            print(self.data[i].pos, end=" ")
        print("done")
        return True


class tWord:
    def __init__(self, word):
        self.word = word
        self.pos = str(nlp(word)[0].pos)

    def __init__(self, word, part):
        self.word = str(word)
        self.pos = str(part)

    def __repr__(self):
        return str("<" + str(self.word) + ", " + str(self.pos) + ">")

    def __str__(self):
        return str("<" + str(self.word) + ", " + str(self.pos) + ">")


# Finds ||x|| of a vector
def getNorm(vector):
    sum = 0.0
    for i in vector:
        sum += i * i
    return np.sqrt(sum)


# States what bigram based on a given index. Mostly used for debugging purposes, has little to no implementation use.
def getBigram(index):
    first = index // len(posVector)
    second = index % len(posVector)
    print(posVector[index // len(posVector)], end=" ")
    if posVector[index % len(posVector)] == "TERM":
        print("***", posVector[index % len(posVector)], "***")
    else:
        print(posVector[index % len(posVector)])
    return True


# Pass string, return bigram vector X (name in function is wrong)
def make_X(posArr):
    Phi = np.zeros(Phi_size)

    k = 0

    for i in range(len(posArr) - 1):
        if i == 0:
            l = posVector.index(str(posArr[i]))
            k = posVector.index(str(posArr[i + 1]))
            Phi[l * len(posVector) + k] += 1
        else:
            l = posVector.index(str(posArr[i + 1]))
            Phi[k * len(posVector) + l] += 1
            k = l
    return Phi


# takes list of X and compiles it into an average, xBar (the name is wrong)
def make_xBar(X_list):
    xBar = np.zeros(Phi_size)
    for i in X_list:
        xBar = xBar + i
    xBar = xBar / len(X_list)

    return xBar


# Makes a list of Phi, imagine it's stored vertically
def make_PhiList(X, xBar):
    PhiList = []
    for i in X:
        PhiList.append(i - xBar)
    return PhiList


# Want a better place to hold them while still allowing A to exist so:
def storePhi(Phi_list, Phi):
    # where Phi list is the array of Phi unformatted. A is too formatted to use cleanly at this point
    Phi_list.append(Phi)
    return True


# but i also kind of need A for actual computations
def make_A(Phi_list):
    A = np.zeros((Phi_size, len(Phi_list)))
    for i in range(len(Phi_list)):
        for j in range(len(Phi_list[i])):
            A[j][i] = Phi_list[i][j]
    return A


# AAT is the default = [324xL]x[Lx324] = [324x324]
# ATA would          = [Lx324]x[324xL] = [LxL]
def make_covarianceMatrix(A):
    SigmaX = np.matmul(A, A.transpose())
    SigmaX = SigmaX / A[0].size
    return SigmaX


# Returns eigenvector and eigenvector coefficients (v and lambda)
def make_Eigen(cov):
    lamb, v = LA.eig(cov)  # assuming cov is AAT covariance matrix
    v = v.real
    lamb = lamb.real
    return lamb, v


# Takes V created by make_Eigen() and stores it in a list for easier manipulation later.
def store_v(V):
    # i believe v is stored similarly to A and Phi, so vertically
    vList = []
    for i in range(len(V[0])):
        temp = np.zeros(len(V[0]))
        for j in range(len(V)):
            temp[j] = float(V[j][i])
        vList.append(temp)

    return vList


# Normalizes V such that ||V_i||==1, allows us to easily calculate Omega
def normalize_vList(vList):
    for i in vList:
        sum = 0.0
        for j in range(len(i)):
            sum += i[j] * i[j]
        sum = np.sqrt(sum)
        # print(sum)

        for j in range(len(i)):
            i[j] /= sum

    return True


# Creates omega using V and Phi, used for calculating Phi Hat down the line
def make_omegaList(Phi_list, vList):
    Omega_list = []
    for i in range(len(Phi_list)):
        Omega_list.append(np.matmul(Phi_list[i].transpose(), vList[i]))
    return Omega_list


# Returns how many eigenvectors are to be used to represent at least T% of the data
def get_kThresh(lamb, T):
    denom = np.sum(lamb)
    k = 0
    sum = 0.0
    for k in range(len(lamb)):
        sum += lamb[k]
        if sum / denom > T:
            return k + 1
    return k + 1


# Creates sample of what the data should look like based on k samples holding T% of the data.
def get_PhiHat(k, omegaList, vList):
    PhiHat = np.zeros(len(vList[0]))
    for i in range(k):
        PhiHat += omegaList[i] * vList[i]
    return PhiHat


# Returns the euclidean distance of a given string from the current model.
def test_String(string, xBar, PhiHat):
    test = make_X(string)
    test = test - xBar

    return getNorm(test - PhiHat)


# Takes the string and vital parts and updates everything with the new string added to the data set. Returns all passed values except string
def integrate_String(string, xList, xBar, Phi_list, A, lamb, vList, omegaList):
    newX = make_X(string)
    xList.append(newX)
    xBar = make_xBar(xList)

    Phi_list.append(newX - xBar)
    A = make_A(Phi_list)

    lamb, v = make_Eigen(make_covarianceMatrix(A))
    vList = store_v(v)
    normalize_vList(vList)

    omegaList = make_omegaList(Phi_list, vList)

    return (xList, xBar, Phi_list, A, lamb, vList, omegaList)


def case3_BDT(x, x_list, Sigma, omega_i):
    mu = np.zeros(len(x_list[0]))
    for i in range(len(x_list)):
        mu += x_list[i]
    mu /= len(x_list)

    return LA.inv(Sigma)
