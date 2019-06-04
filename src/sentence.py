import os
import operator
import re
import collections

ppDictionary = {}

def nextpos(postag, probability, recurlevel):
  if "$$" in postag:
    mylist = []
    mylist.append(["$", float(1)])
    return mylist

  if recurlevel > 15:
    mylist = []
    return mylist

  currDictionary = {}
  tempDictionary = {}
  temp2Dictionary = {}
  temp3Dictionary = {}
  
  for x, y in ppDictionary.items():
    mylist = re.split('\s+', x)
    if postag == mylist[0]:
      d = {x: y}
      tempDictionary.update(d)
      
  count = float(0)
  
  for x, y in tempDictionary.items():
      if y.isdigit():
        count += float(int(y))

  for x, y in tempDictionary.items():
    if y.isdigit():
      d = {x: float(int(y))/float(count)}
      temp2Dictionary.update(d)
    
  temp2Dictionary = collections.OrderedDict(sorted(temp2Dictionary.items(), key=operator.itemgetter(1), reverse=True))
  temp2Dictionary = dict(temp2Dictionary.items()[:2])
#  print "LEVEL: " + str(recurlevel)
  mylist = []
  for x, y in temp2Dictionary.items():
    nextstring = re.split('\s+', x)
    if recurlevel < 2:
        print nextstring[1]
    wordlist = nextpos(nextstring[1], y, recurlevel+1)
    for i in range(len(wordlist)):
#      print wordlist[i][1]
      posstring = nextstring[0] + " " + wordlist[i][0]
      mylist.append([posstring, float(wordlist[i][1])*probability])
#  print mylist
  return mylist


def main():
  global ppDictionary
  currDictionary = {}
  tempDictionary = {}
  temp2Dictionary = {}
  temp3Dictionary = {}
  file = open("../data/ppFreq", "r")
  for x in file:
    mylist = re.split(r'\s+', x)
    string = mylist[0] + " " + mylist[1]
    d = {string: mylist[2]}
    ppDictionary.update(d)
  file.close()
  
  for x, y in ppDictionary.items():
    if x.startswith('^'):
      d = {x: y}
      tempDictionary.update(d)

  count = 0
  for x, y in tempDictionary.items():
    count += int(y)

#  print count

  for x, y in tempDictionary.items():
    d = {x: float(int(y)/float(count))}
    temp2Dictionary.update(d)
  
  temp2Dictionary = collections.OrderedDict(sorted(temp2Dictionary.items(), key=operator.itemgetter(1), reverse=True))
  temp2Dictionary = dict(temp2Dictionary.items()[:50])

  mylist = []
  for x, y in temp2Dictionary.items():
    print x +" " + str(y)
    nextstring = re.split('\s+', x)
    wordlist = list(nextpos(nextstring[1], y, 0))
    for i in range(len(wordlist)):
      posstring = wordlist[i][0]
      mylist.append([posstring, wordlist[i][1]])
    print mylist
      
  for i in range(len(mylist)):
    print mylist[i][0]
    temp3Dictionary.update({mylist[i][0]: mylist[i][1]})
      
  temp3Dictionary = collections.OrderedDict(sorted(temp3Dictionary.items(), key=operator.itemgetter(1), reverse=True))
  file = open("../data/posSentences.txt", "w")
  for x, y in temp3Dictionary.items():
    file.write(x+"   "+str(y)+"\n")
    print x
    print y
  file.close()

if __name__ == '__main__':
    main()