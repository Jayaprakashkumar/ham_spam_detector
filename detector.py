import os
import collections


def main():
    print("Hello")
    readFile()

def readFile():
    print("Hello1")
    HamDict = {}
    SpamDict = {}
    hamCounter =0
    spamCounter =0
    your_path = '../data/train'
    files = os.listdir(your_path)

    for file in files:
        print(file)
        if "ham" in file:
            print("yes")
            f=open(os.path.join(your_path,file),'r')
            for line in f:
                for word in line.split():
                    print(word)


            f.close()


        if "spam" in file:
            print("yes")
            f=open(os.path.join(your_path,file),'r')
            for line in f:
                for word in line.split():
                    print(word)


            f.close()

# if _name_ == "_main_":
main()