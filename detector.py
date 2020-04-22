import os
import collections
import re

def main():
    print("Hello")
    readFile()

def readFile():
    print("Hello1")
    HamDict = {}
    SpamDict = {}
    hamCounter =0
    spamCounter =0
    your_path = './data/train'
    files = os.listdir(your_path)

    for file in files:
        # print(file)
        if "ham" in file:
            # print("yes")
            f=open(os.path.join(your_path,file),'r')
            for line in f:
                line = re.sub('[^a-z\s]+',' ',line, flags=re.IGNORECASE)
                line = re.sub('(\s+)',' ',line)
                line = re.split(' ',line)
                # print(line)
                for word in line:
                    if len(word) > 0:
                        if word in HamDict:
                            HamDict.update({word : HamDict[word] + 1})
                        else:
                            HamDict[word] = 1
                         
            f.close()
            print(HamDict)

        if "spam" in file:
            # print("yes")
            f=open(os.path.join(your_path,file),'r')
            for line in f:
                line = re.sub('[^a-z\s]+',' ',line, flags=re.IGNORECASE)
                line = re.sub('(\s+)',' ',line)
                line = re.split(' ',line)
                # print(line)
                for word in line:
                    if len(word) > 0:
                        if word in SpamDict:
                            SpamDict.update({word : SpamDict[word] + 1})
                        else:
                            SpamDict[word] = 1
                         

            f.close()

# if _name_ == "_main_":
main()