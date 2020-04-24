import os
import collections
import re
import math

def main():
    readFile()

def readFile():
    HamDict = {}
    SpamDict = {}
    hamCounter =0
    spamCounter =0
    your_path = './data/train'
    files = os.listdir(your_path)

    for file in files:
        # print(file)
        if "ham" in file:
            hamCounter = hamCounter + 1
            f=open(os.path.join(your_path,file),'r')
            for line in f:
                line = re.sub('[^a-z\s]+',' ',line, flags=re.IGNORECASE)
                line = re.sub('(\s+)',' ',line)
                line = re.split(' ',line)
                # print(line)
                for word in line:
                    if len(word) > 0:
                        if word.lower() in HamDict:
                            HamDict.update({word.lower() : HamDict[word.lower()] + 1})
                        else:
                            HamDict[word.lower()] = 1
                         
            f.close()
            # print(HamDict)

        if "spam" in file:
            # print("yes")
            spamCounter = spamCounter + 1
            f=open(os.path.join(your_path,file),'r')
            for line in f:
                line = re.sub('[^a-z\s]+',' ',line, flags=re.IGNORECASE)
                line = re.sub('(\s+)',' ',line)
                line = re.split(' ',line)
                # print(line)
                for word in line:
                    if len(word) > 0:
                        if word.lower() in SpamDict:
                            SpamDict.update({word.lower() : SpamDict[word.lower()] + 1})
                        else:
                            SpamDict[word.lower()] = 1
            f.close()
            # print(SpamDict)
    bagsProbabilty(HamDict,SpamDict,hamCounter, spamCounter)        


def bagsProbabilty(hamDic, spamDic, hamCounter, spamCounter):
    hamLen = 0
    spamLen = 0
    spamProb = {}
    hamProb = {}
    smoothing = 0.5
    uniqueWords= 0
    totalFiles = hamCounter + spamCounter


    # total words in ham and spam training set
    for word in hamDic:
        if word not in spamDic:
            uniqueWords = uniqueWords + 1

    uniqueWords = uniqueWords + len(spamDic)
    # print("uniqueword :", uniqueWords)   
    # print("hamDic: ", len(hamDic))
    # print("spamDic: ", len(spamDic))
    for length in hamDic:
        hamLen = hamLen + hamDic[length]
        
    for length in spamDic:
        spamLen = spamLen + spamDic[length]

    for i in hamDic:
        hamProb.update({i : (hamDic[i] + smoothing)/(hamLen + (smoothing * uniqueWords))})

    for i in spamDic:
        spamProb.update({i : (spamDic[i] + smoothing)/(spamLen + (smoothing * uniqueWords))})
       
    moduleFile = open("./data/output/module.txt", "w+")
    moduleArray = []

    for data in hamDic:
        dataStr = ""
        dataStr = dataStr + data +"  "+str(hamDic[data])+ "  "+str(hamProb[data])+ "  "

        if(data in spamDic):
            dataStr = dataStr + str(spamDic[data]) + "  " + str(spamProb[data]) 
        else:
            temp = smoothing / (spamLen + (uniqueWords * smoothing))
            dataStr = dataStr + "0" + "  " + str(temp)
        moduleArray.append(dataStr)       

    for data in spamDic:
        dataStr = ""
        if data not in hamDic:
            temp = smoothing / (hamLen + (uniqueWords * smoothing))
            dataStr = dataStr + data +"  "+str(spamDic[data])+ "  "+str(spamProb[data])+ "  " + "0" + "  " + str(temp)
            moduleArray.append(dataStr) 
    
    # print("total data set: ",len(moduleArray) )
    for i, data in enumerate(moduleArray):
        j = i + 1
        result = str(j) + "  " + data
        moduleFile.write(result+"\n")

    moduleFile.close()
    # print("hamPRob: ", hamProb)
    # print("spamProb: ", spamProb)
    testModule(hamProb, spamProb, hamCounter, spamCounter, totalFiles, spamLen, hamLen, uniqueWords)

    
def testModule(hamProb, spamProb, hamCounter, spamCounter, totalFiles, spamLen, hamLen, uniqueWords):
    your_path = './data/test'
    files = os.listdir(your_path)
    testResult = []
    testFileCounter = 0

    for file in files:
        testFileCounter = testFileCounter + 1
        # print(file)
        spamFileProb = 0 
        hamFileProb = 0 
        # print("spamLen", spamLen)
        spamFileProb = spamFileProb + math.log10(spamCounter/totalFiles)
        hamFileProb = hamFileProb + math.log10(hamCounter/totalFiles)
        # print("spamFileProb", spamFileProb)
        # print("hamFileProb", hamFileProb)

        if "txt" in file:
            # print("yes")
            # hamCounter = hamCounter + 1
            f=open(os.path.join(your_path,file),'r')
            for line in f:
                line = re.sub('[^a-z\s]+',' ',line, flags=re.IGNORECASE)
                line = re.sub('(\s+)',' ',line)
                line = re.split(' ',line)
                # print(line)
                for word in line:
                    if word in hamProb:
                        # print(word," is ", y)
                        hamFileProb = hamFileProb + math.log10(hamProb[word])
                    else:
                        hamX = 0.5 / (hamLen + (uniqueWords * 0.5))
                        hamFileProb = hamFileProb + math.log10(hamX)

                    if word in spamProb:
                        # print(word, "is ", math.log10(spamProb[word]))
                        spamFileProb = spamFileProb + math.log10(spamProb[word])
                    else:
                        spamX = 0.5 / (spamLen + (uniqueWords * 0.5))
                        # print(word, "is ", math.log10(spamX))
                        spamFileProb = spamFileProb + math.log10(spamX)

                # print(result)        
                                 
            f.close()    
        # print("hamfilePRob:", hamFileProb)
        # print("spamFileProb:", spamFileProb)    
        fileStatus = ""
        flag = ""
        if hamFileProb > spamFileProb:
            fileStatus = "ham"
            flag = "right"
        else:
            fileStatus = "spam"
            flag = "wrong"

        result = file + "  " + fileStatus + "  " +str(round(hamFileProb, 5)) + "  " + str(round(spamFileProb,5)) + "  "+ "ham" + "  " + flag
        testResult.append(result)

    outputFile = open("./data/output/result.txt", "w+")
    for i, data in enumerate(testResult):
        j = i + 1
        # print(str(j)+ "  " + data)
        outputFile.write(str(j)+ "  " + data+"\n")

    outputFile.close()    

main()