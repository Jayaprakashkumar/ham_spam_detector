import os
import collections
import re
import numpy as np

def main():
    readFile()

def readFile():
    hamDict = {}
    spamDict = {}
    hamCounter =0
    spamCounter =0
    your_path = './data/train'
    files = os.listdir(your_path)

    for file in files:
        if "ham" in file:
            hamCounter = hamCounter + 1
            f=open(os.path.join(your_path,file),'r',encoding="utf8", errors="surrogateescape")
          
            hamTrainFile = []    
            word1 = re.split("[^a-zA-Z]", f.read())
            for word in word1:
                if len(word) > 0:
                    hamTrainFile.append(word.lower())

            for word in hamTrainFile:      
                if word in hamDict:
                    hamDict.update({word : hamDict[word] + 1})
                else:
                    hamDict[word] = 1
                        
            f.close()

        if "spam" in file:
            spamCounter = spamCounter + 1
            f=open(os.path.join(your_path,file),'r',encoding="utf8", errors="surrogateescape")

            spamTrainFile = []
            word1 = re.split("[^a-zA-Z]", f.read())
            for word in word1:
                if len(word) > 0:
                    spamTrainFile.append(word.lower())

            for word in spamTrainFile:
                if word in spamDict:
                    spamDict.update({word : spamDict[word] + 1})
                else:
                    spamDict[word] = 1
            f.close()

    bagsProbabilty(sortData(hamDict),sortData(spamDict),hamCounter, spamCounter)        


def bagsProbabilty(hamDic, spamDic, hamCounter, spamCounter):
    hamLen = 0
    spamLen = 0
    spamProb = {}
    hamProb = {}
    smoothing = 0.5
    uniqueWords= 0
    totalFiles = hamCounter + spamCounter

    # total words in ham and spam training set
    uniqueWords = uniqueWords + len(spamDic)
    for word in hamDic:
        if word not in spamDic:
            uniqueWords = uniqueWords + 1

    print("training set vocabulary", uniqueWords)
    

    # find total word frequence in ham dictionary
    for freq in hamDic:
        hamLen = hamLen + hamDic[freq]
        
    # find total word frequence in spam dictionary
    for freq in spamDic:
        spamLen = spamLen + spamDic[freq]

    print("Total word frq in ham :", hamLen)
    print("Total word frq in spam :", spamLen)

    # p(word | ham)
    for i in hamDic:
        hamProb.update({i : (hamDic[i] + smoothing)/(hamLen + (smoothing * uniqueWords))})

    # p(word | spam)
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
            spamDic.update({data : 0})
            spamProb.update({data : temp})
            dataStr = dataStr + str(spamDic[data]) + "  " + str(spamProb[data])
        moduleArray.append(dataStr)       


    for data in spamDic:
        dataStr = ""
        if data not in hamDic:
            temp = smoothing / (hamLen + (uniqueWords * smoothing))
            hamDic.update({data : 0})
            hamProb.update({data : temp})
            dataStr = dataStr + data+ "  " + str(hamDic[data]) + "  " + str(hamProb[data]) +"  "+str(spamDic[data])+ "  "+str(spamProb[data])
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
        spamScore = 0 
        hamScore = 0 
        spamScore = spamScore + np.log(spamCounter/totalFiles)
        hamScore = hamScore + np.log(hamCounter/totalFiles)
        fileWords = []
           
        if "txt" in file:

            # f=open(os.path.join(your_path,file), mode='r')
            f=open(os.path.join(your_path,file),'r',encoding="utf8", errors="surrogateescape")

            words = re.split("[^a-zA-Z]", f.read())
            for word in words:
                if len(word) > 0:
                    fileWords.append(word.lower())

            for word in fileWords:
                if word in hamProb:
                    hamScore = hamScore + np.log(hamProb[word])
            
                if word in spamProb:
                    spamScore = spamScore + np.log(spamProb[word])
                                    
            f.close()          
        
        fileStatus = ""
        flag = ""
        status = ""

        
        if hamScore > spamScore:
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

        result = file + "  " + flag+ "  " +str(hamScore) + "  " + str(spamScore) + "  "+ fileStatus + "  " + status
        testResult.append(result)

    outputFile = open("./data/output/result.txt", "w+")
    for i, data in enumerate(testResult):
        j = i + 1
        # print(str(j)+ "  " + data+"\n")
        outputFile.write(str(j)+ "  " + data+"\n")

    outputFile.close() 


    hamAccuracy =  ( correctHam/ testHamCount) * 100
    spamAccuracy = ( correctSpam/ testSpamCount) * 100

    
    print("predicted correct ham: ", correctHam)
    print("predicted correct spam: ", correctSpam)
    print("total ham in test file: ", testHamCount)
    print("total spam in test file: ", testSpamCount)

    print("ham Accuracy: ", hamAccuracy)
    print("spam Accuracy: ", spamAccuracy)

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

    
    hamArr = [["","__","___","__","__","__","__","",""],["|", " ", "   ", " ", "|"," ", "   ", " ", "|"], [ "|", " ",correctHam, " ", "|", "  ", testSpamCount - correctSpam, " ", "|"],["|","__","__","__","","__","__","_","|"],["|", " ", "   ", " ", "|"," ", "   ", " ", "|"], [ "|", "  ",testHamCount - correctHam, "  ", "|", " ",correctSpam, " ", "|"],["|","__","__","_","|","__","__","_","|"]]

    
    spamArr = [["","__","___","__","__","__","__","",""],["|", " ", "   ", " ", "|"," ", "   ", " ", "|"], [ "|", " ",correctSpam, " ", "|", "  ",testHamCount - correctHam, "  ", "|"],["|","__","__","__","","__","__","_","|"],["|", " ", "   ", " ", "|"," ", "   ", " ", "|"], [ "|", "  ",testSpamCount - correctSpam, " ", "|", " ",correctHam, " ", "|"],["|","__","__","_","|","__","__","_","|"]]
    # print(hamArr)

    print("Ham confusion Matrix")
    print("--------------------")
    for row in hamArr:
        for elem in row:
            print(elem, end=' ')
        print()
    print("\n")

    print("Spam confusion Matrix")
    print("-------------------=-")
    for row in spamArr:
        for elem in row:
            print(elem, end=' ')
        print()

def sortData(dic):
    sortDic = {}
    for key in sorted(dic):
        sortDic.update({key : dic[key]})
    return sortDic 



main()