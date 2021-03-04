import re

from pkg_resources import resource_stream
mostUsedWords = resource_stream('notebooks.resources', 'mostusedwords.txt').read().decode('ascii')


class ParsedDoc:
    def __init__(self, body: str):
        # self._words = re.findall(r'\w+', body)
        # self._wordCount = len(self._words)
        self._periodCount = len(re.findall(r'.', body))
        self._commaCount = len(re.findall(r',', body))
        self._quoteCount = len(re.findall(r'"', body)) / 2
        # self._totalChars = len(re.sub(r'[^a-zA-Z0-9]', '', body))
        
        # self._frequency = {}
        # matchPattern = re.findall(r'\b[a-z]{3,15}\b', body)
        # checkAgainst = re.findall(r'\b[a-z]{3,15}\b', mostUsedWords)
        # for word in matchPattern:
        #     if word not in checkAgainst:
        #         count = self._frequency.get(word, 0)
        #         self._frequency[word] = count + 1
        
        # self._averageWordLength = self._totalChars / self._wordCount
        # if self._periodCount != 0:
        #     self._pToWRatio = self._wordCount / self._periodCount
        # else:
        #     self._pToWRatio = 0.
        #
    def getWords(self):
        return self._words
    
    def getWordCount(self):
        return self._wordCount
    
    def getPeriodCount(self):
        return self._periodCount
    
    def getCommaCount(self):
        return self._commaCount
    
    def getQuoteCount(self):
        return self._quoteCount
    
    def getTotalChars(self):
        return self._totalChars
    
    def getAverageWordLength(self):
        return self._averageWordLength
    
    def getPToWRatio(self):
        return self._pToWRatio
    
    def getFrequencyOf(self, word: str):
        return self._frequency[word]
