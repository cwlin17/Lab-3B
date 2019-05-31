# NAME: Don Le, Carol Lin
# EMAIL: donle22599@g.ucla.edu, carol9gmail@yahoo.com
# ID: 804971410, 804984337

#!/usr/bin/python

import sys, csv

class SuperBlock:
    def __init__(self, param):
        self.totalNumBlocks = param[1]
        self.totalNumInodes = param[2]
        self.blockSize = param[3]
        self.inodeSize = param[4]
        self.blocksPerGroup = param[5]
        self.inodesPerGroup = param[6]
        self.firstNonresInode = param[7]

class Group:
    def __init__(self, param):
        self.groupNum = int(param[1])
        self.totalBlocksInGroup = int(param[2])
        self.totalInodesInGroup = int(param[3])
        self.numFreeBlocks = int(param[4])
        self.numFreeInodes = int(param[5])
        self.freeBlockBitmap = param[6]
        self.freeInodeBitmap = param[7]
        self.firstBlockInodes = param[8]

class FreeBlockEntries:
    def __init__(self, param):
        self.freeBlockNum = int(param[1])

class FreeInodeEntries:
    def __init__(self, param):
        self.freeInodeNum = int(param[1])

class Inode:
    def __init__(self, param):
        self.inodeNum = int(param[1])
        self.fileType = param[2]
        self.owner = param[4]
        self.group = param[5]
        self.linkCount = int(param[6])
        self.fileSize = int(param[10])

def fillObjects():
    with open(sys.argv[1], 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            firstCol = row[0]
            if (firstCol == "INODE"):
                print("Got an inode")
    
def main():
    # Checking for correct number of arguments
    if len(sys.argv) != 2:
        sys.stderr.write("Incorrect number of arguments.\n")
        exit(1)

    with open(sys.argv[1], 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            print(",".join(row))
    fillObjects()
            

##### Need to read csv file contents into data structure(s) #####
if __name__ == "__main__":
    main()
