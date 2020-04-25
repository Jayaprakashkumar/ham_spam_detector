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
        if "ham" in file:
            hamCounter = hamCounter + 1
            f=open(os.path.join(your_path,file),'r',encoding="utf8", errors="surrogateescape")
            for line in f:
                line = re.sub('[^a-z\s]+',' ',line, flags=re.IGNORECASE)
                line = re.sub('(\s+)',' ',line)
                line = re.split(' ',line)
                for word in line:
                    if len(word) > 0:
                        if word.lower() in HamDict:
                            HamDict.update({word.lower() : HamDict[word.lower()] + 1})
                        else:
                            HamDict[word.lower()] = 1
                         
            f.close()

        if "spam" in file:
            spamCounter = spamCounter + 1
            f=open(os.path.join(your_path,file),'r',encoding="utf8", errors="surrogateescape")
            for line in f:
                line = re.sub('[^a-z\s]+',' ',line, flags=re.IGNORECASE)
                line = re.sub('(\s+)',' ',line)
                line = re.split(' ',line)
                for word in line:
                    if len(word) > 0:
                        if word.lower() in SpamDict:
                            SpamDict.update({word.lower() : SpamDict[word.lower()] + 1})
                        else:
                            SpamDict[word.lower()] = 1
            f.close()
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
            dataStr = dataStr + data+ "  " + "0" + "  " + str(temp) +"  "+str(spamDic[data])+ "  "+str(spamProb[data])
            moduleArray.append(dataStr) 
    
    for i, data in enumerate(moduleArray):
        j = i + 1
        result = str(j) + "  " + data
        moduleFile.write(result+"\n")

    moduleFile.close()
    testModule(hamProb, spamProb, hamCounter, spamCounter, totalFiles, spamLen, hamLen, uniqueWords)

    
def testModule(hamProb, spamProb, hamCounter, spamCounter, totalFiles, spamLen, hamLen, uniqueWords):
    your_path = './data/test'
    files = os.listdir(your_path)
    testResult = []
    testFileCounter = 0
    testHamCount = 0
    testSpamCount = 0
    correctHam = 0
    correctSpam = 0
    

    for file in files:
        testFileCounter = testFileCounter + 1
        spamFileProb = 0 
        hamFileProb = 0 
        spamFileProb = spamFileProb + math.log10(spamCounter/totalFiles)
        hamFileProb = hamFileProb + math.log10(hamCounter/totalFiles)
           
        if "txt" in file:

            # f=open(os.path.join(your_path,file),'r')
            f=open(os.path.join(your_path,file),'r',encoding="utf8", errors="surrogateescape")
            for line in f:
                line = re.sub('[^a-z\s]+',' ',line, flags=re.IGNORECASE)
                line = re.sub('(\s+)',' ',line)
                line = re.split(' ',line)
                for word in line:
                    if word in hamProb:
                        hamFileProb = hamFileProb + math.log10(hamProb[word])
                    # else:
                    #     hamX = 0.5 / (hamLen + (uniqueWords * 0.5))
                    #     hamFileProb = hamFileProb + math.log10(hamX)

                    if word in spamProb:
                        spamFileProb = spamFileProb + math.log10(spamProb[word])
                    # else:
                    #     spamX = 0.5 / (spamLen + (uniqueWords * 0.5))
                    #     spamFileProb = spamFileProb + math.log10(spamX)

                # print(result)        
                                 
            f.close()    
      
        fileStatus = ""
        flag = ""
        status = ""

        
        if hamFileProb > spamFileProb:
            flag = "ham"
        else:
            flag = "spam"

        if "ham" in file:
            testHamCount = testHamCount + 1
            fileStatus = "ham"
            if flag == "ham":
                correctHam = correctHam + 1
        else:
            testSpamCount = testSpamCount + 1 
            fileStatus = "spam"
            if flag == "spam":
                correctSpam = correctSpam + 1

        if fileStatus == flag :
            status = "right"
        else:
            status = "wrong"

        result = file + "  " + flag+ "  " +str(round(hamFileProb, 5)) + "  " + str(round(spamFileProb,5)) + "  "+ fileStatus + "  " + status
        testResult.append(result)

    outputFile = open("./data/output/result.txt", "w+")
    for i, data in enumerate(testResult):
        j = i + 1
        print(str(j)+ "  " + data+"\n")
        outputFile.write(str(j)+ "  " + data+"\n")

    outputFile.close() 

    hamAccuracy =  ( correctHam/ testHamCount) * 100
    spamAccuracy = ( correctSpam/ testSpamCount) * 100

    
    print("correctHam: ", correctHam)
    print("correctSpam: ", correctSpam)
    print("testHamCount: ", testHamCount)
    print("testSpamCount: ", testSpamCount)

    print("hamAccuracy: ", hamAccuracy)
    print("spamAccuracy: ", spamAccuracy)


    hamPercision = correctHam / (correctHam + (testSpamCount - correctSpam))
    hamRecall = correctHam / (correctHam + (testHamCount - correctHam))

    print("hamPercision: ", hamPercision)
    print("hamRecall: ", hamRecall)

    spamPercision = correctSpam / (correctSpam + (testHamCount - correctHam))
    spamRecall = correctSpam / (correctSpam + (testSpamCount - correctSpam))

    print("spamPercision: ", spamPercision)
    print("spamRecall: ", spamRecall)

    # consider beta = 1
    hamFmeasure =  2 * (hamPercision * hamRecall) / (hamPercision + hamRecall)
    spamFmeasure =  2 * (spamPercision * spamRecall) / (spamPercision + spamRecall)
    print("hamFmeasure: ", hamFmeasure)
    print("spamFmeasure: ", spamFmeasure)


main()