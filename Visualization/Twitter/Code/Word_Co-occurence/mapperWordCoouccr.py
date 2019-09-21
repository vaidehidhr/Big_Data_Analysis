#!/usr/bin/env python3
import sys

def read_input(file):
    for line in file:
        return line.split()

def main(separator='\t'):
    listOfTopWords = ['movie','new','action','flim','live','horror','comedy','f','see','love']

    data = read_input(sys.stdin)
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
                    j=j+1

if __name__ == "__main__":
