#!/usr/bin/env python3
import sys

def read_input(file):
    for line in file:
        return line.split()

def main(separator='\t'):
    # fileTopWords = '/home/cse587/sortedReducerWCoutput12345'
    listOfTopWords = ['people','new','time','york','year','show','love','life','even','story']

    # from collections import OrderedDict
    # d = {}
    #     # {'banana': 3, 'apple': 4, 'pear': 1, 'orange': 2}
    # d.get('banana')
    # d.has_key('banana')
    # OrderedDict(sorted(d.items(), key=lambda t: t[1], reverse=True))
    # with open(fileTopWords,'r') as fileReading:
    #     listOfTopWords = listOfTopWords.append(fileReading.readline())
        # x = fileReading.read()
    data = read_input(sys.stdin)
    # print (type(data))
    # tokens = data.split(' ')
    m = len(data)
    dictonaryOfPairs = {}
    for i in range(m):
        j=i+1
        if data[i]!='':
            if data[i] in listOfTopWords:
                while(j<m):
                    if data[i]!=data[j]:
                        if data[i] > data[j]:
                            print ((data[j], data[i]), separator, 1)
                        elif data[i] < data[j]:
                            print((data[i], data[j]), separator, 1)
                        # if dictonaryOfPairs.get((data[j],data[i]) == None):
                        #     dictonaryOfPairs[(data[i], data[j])] = 1
                    # elif data[i]!=data[j]:
                    #     dictonaryOfPairs[(data[j], data[i])] = dictonaryOfPairs[(data[j], data[i])] + 1
                    #     print ((data[j], data[i]), separator, 1)
                    j=j+1

if __name__ == "__main__":
