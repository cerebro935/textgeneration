import os
import re
import random
import operator
import collections
import math
import multiprocessing

structureDictionary = {}
wpDictionary = {}
wwDictionary = {}
wwwDictionary = {}
wDictionary = {}

def findword(postag, wordlist):
  if not wordlist:
    prevword = '^'
  else:
    prevword = str(wordlist[-1])
  global wpDictionary
  global wwDictionary
  global wDictionary
  tempDictionary = {}
  temp2Dictionary = {}
  temp3Dictionary = {}
  temp4Dictionary = {}
  temp5Dictionary = {}
  temp6Dictionary = {}
  
  for x, y in wpDictionary.items():
    mylist = re.split(r'\s+', x)
    if postag == mylist[1] and mylist[0] not in wordlist:
      d = {mylist[0]: y}
      tempDictionary.update(d)
      
  for x, y in wwwDictionary.items():
    mylist = re.split(r'\s+', x)
    if len(mylist)==3 and len(wordlist) > 2:
      if mylist[0] == wordlist[-2] and mylist[1]==wordlist[-1]:
        if mylist[2] not in wordlist:
          d = {mylist[2]: y}
          temp5Dictionary.update(d)
  
  for x, y in wwDictionary.items():
    if x.startswith(prevword):
      mylist = re.split(r'\s+', x)
      if mylist[0] not in wordlist:
        d = {mylist[1]: y}
        temp2Dictionary.update(d)

  
  count = 0    
  for x, y in tempDictionary.items():
    if y.isdigit():
      count += int(y)
    
  for x, y in tempDictionary.items():
    if y.isdigit():
      d = {x: float(int(y)/float(count))}
      temp3Dictionary.update(d)
  
  count = 0
  for x, y in temp2Dictionary.items():
    if y.isdigit():
      count += int(y)
  
  for x, y in temp2Dictionary.items():
    if y.isdigit():
      d = {x: float(int(y)/float(count))}
      temp4Dictionary.update(d)
      
  count = 0
  for x, y in temp5Dictionary.items():
    if y.isdigit():
      count += int(y)
      
  for x, y in temp5Dictionary.items():
    if y.isdigit():
      d = {x: float(int(y)/float(count))}
      temp6Dictionary.update(d)

  for x, y in temp3Dictionary.items():
    if x not in temp6Dictionary:
      if x in temp4Dictionary:
        temp6Dictionary.update({x: 1+temp4Dictionary[x]})
      else:
        temp6Dictionary.update({x: y})
    else:
      if x in temp4Dictionary:
        temp6Dictionary[x] += 3
      else:
        temp6Dictionary[x] += 2
        
  temp4Dictionary = collections.OrderedDict(sorted(temp6Dictionary.items(), key=operator.itemgetter(1), reverse=True))
  temp4Dictionary = dict(temp4Dictionary.items()[:5])
  mylist = []
  for x, y in temp4Dictionary.items():
    mylist.append([x, float(y)])
    
  return mylist 
  
def fill(randline):
  mylist = re.split(r'\s+', randline)
  wordlist = []
  for j in mylist:
    if j == '.' or '$' in j:
      wordlist.append('.')
      break
    stringlist = list(findword(j, wordlist))
    string = ""
    if not stringlist:
      string = "NA"
    else:
      string, wordprob = random.choice(stringlist)
    wordlist.append(string)
  sentencestring = ""
  for x in wordlist:
    sentencestring += x+" "
  print sentencestring +"\n\n"
  file= open("../data/generatedSentences.txt", "a")
  file.write(sentencestring +"\n")
  file.close()

def main():
  global structureDictionary
  global wpDictionary
  global wwDictionary
  global wDictionary
  global wwwDictionary
  
  file = open("../data/posSentences.txt", "r")
  for x in file:
    mylist = re.split(r'\s+', x)
    string = ""
    prob = ""
    for y in range(len(mylist)):
      if y == len(mylist)-2:
        prob = float(mylist[y])
      else:
        string += mylist[y]+" "
    d = {string.lower(): prob}
    structureDictionary.update(d)
  file.close()
  structureDictionary = collections.OrderedDict(sorted(structureDictionary.items(), key=operator.itemgetter(1), reverse=True))
  
  file = open("../data/wpFreq", "r")
  for x in file:
    mylist = re.split(r'\s+', x)
    string = mylist[0] + " " + mylist[1]
    d = {string.lower(): mylist[2]}
    wpDictionary.update(d)
  file.close()
  
  file = open("../data/wFreq", "r")
  for x in file:
    mylist = re.split(r'\s+', x)
    string = mylist[0]
    d = {string: mylist[1]}
    wDictionary.update(d)
  file.close()
  
  file = open("../data/wwFreq", "r")
  for x in file:
    mylist = re.split(r'\s+', x)
    string = mylist[0] + " " + mylist[1]
    d = {string.lower(): mylist[2]}
    wwDictionary.update(d)
  file.close()
  
  file = open("../data/wwwFreq", "r")
  for x in file:
    mylist = re.split(r'\s+', x)
    string = mylist[0] + " " + mylist[1]+" "+mylist[2]
    d = {string.lower(): mylist[3]}
    wwwDictionary.update(d)
  file.close()
  
  i = 0
  structurelist= []
  while i < 100:
    string, prob = random.choice(list(structureDictionary.items()))
    mylist = re.split(r'\s+', string)
    if 5 < len(mylist):
	    structurelist.append(string)
	    i += 1
  pool = multiprocessing.Pool()
  pool.map(fill, structurelist)
  pool.close()
  
if __name__ == '__main__':
  main()
