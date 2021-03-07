import re
import string
f = open('E:/Downloads/testdoc.txt').read()  # f is for file

words = re.findall(r'\w+', f)
# print(words)
wordcount = len(words)
print("The amount of words are: ")
print(wordcount)

periodSearch = re.findall(r'\.', f)
periodCount = len(periodSearch)
print("The amount of periods are: ")
print(periodCount)

commaSearch = re.findall(r',', f)
commaCount = len(commaSearch)
print("The amount of commas are: ")
print(commaCount)

quoteSearch = re.findall(r'\"', f)
quoteCount = len(quoteSearch) / 2
print("The amount of quotes are: ")
print(quoteCount)

totalChars = len(re.sub(r'[^a-zA-Z0-9]', '', f))
print("The amount of characters are: ")
print(totalChars)


mostUsedWords = open('E:/Downloads/mostusedwords.txt').read()  # mostUsedWords is a file
checkAgainst = re.findall(r'\b[a-z]{3,15}\b', mostUsedWords)
# check against are the words to make sure it's not a common word, such as 'the'
frequency = {}
matchPattern = re.findall(r'\b[a-z]{3,15}\b', f)
for word in matchPattern:
    if word not in checkAgainst:
        count = frequency.get(word, 0)
        frequency[word] = count + 1

"""
# If you uncomment the following code it prints out the most commonly used words
frequencyList = frequency.keys()
for words in frequencyList:
    print(words)
    print(frequency[words])
"""
print(frequency)
temp = max(frequency, key=frequency.get)
print("Most frequently used word is: ")
print(temp)


averageWordLength = totalChars / wordcount
print("The Average Word Length is:")
print(averageWordLength)

pToWRatio = wordcount / periodCount
print("The Period count ratio is:")
print(pToWRatio)
