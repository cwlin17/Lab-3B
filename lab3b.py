# NAME: Don Le, Carol Lin
# EMAIL: donle22599@g.ucla.edu, carol9gmail@yahoo.com
# ID: 804971410, 804984337

#!/usr/bin/python

import sys, csv

class SuperBlock:
    def __init__(self, param):
        self.totalNumBlocks = int(param[1])
        self.totalNumInodes = int(param[2])
        self.blockSize = int(param[3])
        self.inodeSize = int(param[4])
        self.blocksPerGroup = int(param[5])
        self.inodesPerGroup = int(param[6])
        self.firstNonresInode = int(param[7])

class Group:
    def __init__(self, param):
        self.groupNum = int(param[1])
        self.totalBlocksInGroup = int(param[2])
        self.totalInodesInGroup = int(param[3])
        self.numFreeBlocks = int(param[4])
        self.numFreeInodes = int(param[5])
        self.freeBlockBitmap = int(param[6])
        self.freeInodeBitmap = int(param[7])
        self.firstBlockInodes = int(param[8])

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
        self.owner = int(param[4])
        self.group = int(param[5])
        self.linkCount = int(param[6])
        self.fileSize = int(param[10])

class Directory:
    def __init__(self, param):
        self.parentInode = int(param[1])
        self.offset = int(param[2])
        self.referencedFileInodeNum = int(param[3])

class IndirectBlockReferences:
    def __init__(self, param):
        self.inodeNumOfOwningFile = int(param[1])
        self.indirectionLevel = int(param[2])
        self.logicalBlockOffset = int(param[3])
        self.indirectBlockNum = int(param[4])
        self.referencedBlockNum = int(param[5])

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
