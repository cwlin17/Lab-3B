
# NAME: Don Le, Carol Lin
# EMAIL: donle22599@g.ucla.edu, carol9gmail@yahoo.com
# ID: 804971410, 804984337

#!/usr/bin/python

import sys, csv

superBlock = None
groupList = []
freeBlockList = []
freeInodeList = []
inodeList = []
directoryList = []
indirectList = []
refBlockList = [] #2 dimensional array to store referenced blocks
freeBlockArray = []
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
        numAdd = len(param[12:28])
        self.blocks = param[12:28]
        for i in range(0, numAdd):
            self.blocks[i] = int(self.blocks[i])



class Directory:
    def __init__(self, param):
        self.parentInode = int(param[1])
        self.offset = int(param[2])
        self.referencedFileInodeNum = int(param[3])
        self.name = param[6]

class IndirectBlockReferences:
    def __init__(self, param):
        self.inodeNum = int(param[1]) #of owning file
        self.indirectionLevel = int(param[2])
        self.logicalBlockOffset = int(param[3])
        self.blockNum = int(param[4])
        self.referencedBlockNum = int(param[5])

class blockRef:
    def __init__(self,inodeNum, blockNum, offset, indirectionLevel):
        self.inodeNum = inodeNum
        self.blockNum = blockNum
#        self.numOfRef = 0;
        self.offset = offset
        self.indirectionLevel = indirectionLevel


def findInodeInconsistencies():
    global superBlock
    global refBlockList
    for inode in inodeList:
        #first check for invalid blocks
        for i in range(0, len(inode.blocks)):
            indirectionLevel = " "
            offset = i
            if (i == 12):
                indirectionLevel = " INDIRECT "
            elif (i == 13):
                indirectionLevel = " DOUBLE INDIRECT "
                offset = 256 + 12;
            elif (i == 14):
                indirectionLevel = " TRIPLE INDIRECT "
                offset = 12 + 256*256 + 256;
            if (inode.blocks[i] < 0 or inode.blocks[i] > superBlock.totalNumBlocks):
                print("INVALID{}BLOCK {} IN INODE {} AT OFFSET {}".format(indirectionLevel,inode.blocks[i], inode.inodeNum, offset))
            #Now check which are pointing to reserved blocks
            elif (inode.blocks[i] >= 1 and inode.blocks[i] < 8): #check blocks
                print("RESERVED{}BLOCK {} IN INODE {} AT OFFSET {}".format(indirectionLevel,inode.blocks[i], inode.inodeNum, offset))
            else: #put block into block list to check later
                blockNum = inode.blocks[i]
                if (i < 12):
                    tempBlock = blockRef(inode.inodeNum, inode.blocks[i], offset, 0)
                    refBlockList[blockNum].append(tempBlock)
                elif (i == 12):
                    tempBlock = blockRef(inode.inodeNum, inode.blocks[i], offset, 1)
                    refBlockList[blockNum].append(tempBlock)
                elif (i == 13):
                    tempBlock = blockRef(inode.inodeNum, inode.blocks[i], offset, 2)
                    refBlockList[blockNum].append(tempBlock)
                elif (i == 14):
                    tempBlock = blockRef(inode.inodeNum, inode.blocks[i], offset, 3)
                    refBlockList[blockNum].append(tempBlock)
#                print(tempBlock.blockNum)
#                print(refBlockList[blockNum][0].blockNum)
    #Do all the same checks but for indirects
    for indirect in indirectList:
        indirectionLevel = "INDIRECT" #For indirection level 1
        if (indirect.indirectionLevel == 2):
            indirectionLevel = "DOUBLE INDIRECT"
        elif (indirect.indirectionLevel == 3):
            indirectionLevel = "TRIPLE INDIRECT"
        if(indirect.referencedBlockNum >= 1 and indirect.referencedBlockNum < 8):
            print("RESERVED{}BLOCK {} IN INODE {} AT OFFSET {}".format(indirectionLevel,indirect.referencedBlockNum,indirect.inodeNum,indirect.logicalBlockOffset))
        elif(indirect.referencedBlockNum < 0 or indirect.referencedBlockNum > superBlock.totalNumBlocks):
            print("INVALID{}BLOCK {} IN INODE {} AT OFFSET {}".format(indirectionLevel,indirect.referencedBlockNum,indirect.inodeNum,indirect.logicalBlockOffset))
        else:
            blockNum = indirect.referencedBlockNum
            if (indirect.indirectionLevel == 1):
                tempBlock = blockRef(indirect.inodeNum, indirect.referencedBlockNum, indirect.logicalBlockOffset, 1);
                refBlockList[blockNum].append(tempBlock)
            elif (indirect.indirectionLevel == 2):
                tempBlock = blockRef(indirect.inodeNum, indirect.referencedBlockNum, indirect.logicalBlockOffset, 2);
                refBlockList[blockNum].append(tempBlock)
            elif (indirect.indirectionLevel == 3):
                tempBlock = blockRef(indirect.inodeNum, indirect.referencedBlockNum, indirect.logicalBlockOffset, 3);
                refBlockList[blockNum].append(tempBlock)
#            print(blockNum)
        #Now check for unreferenced blocks that are not on free list or referenced by a file
    
    #Also check if an allocated block is on a freelist
    global freeBlockArray
    for i in range (8, superBlock.totalNumBlocks):
        if len(refBlockList[i]) == 0 and (i not in freeBlockArray):
            print("UNREFERENCED BLOCK {}".format(i))
        elif len(refBlockList[i]) !=0 and (i in freeBlockArray):
            print("ALLOCATED BLOCK {} ON FREELIST".format(i))
        if (len(refBlockList[i]) > 1):
            for j in range (0, len(refBlockList[i])):
                indirectionLevel = " "
                if (refBlockList[i][j].indirectionLevel == 1):
                    indirectionLevel = " INDIRECT "
                elif (refBlockList[i][j].indirectionLevel == 2):
                    indirectionLevel = " DOUBLE INDIRECT "
                elif (refBlockList[i][j].indirectionLevel == 3):
                    indirectionLevel = " TRIPLE INDIRECT "
                print("DUPLICATE{}BLOCK {} IN INODE {} AT OFFSET {}".format(indirectionLevel, refBlockList[i][j].blockNum, refBlockList[i][j].inodeNum, refBlockList[i][j].offset)) 

        
        
def main():
    # Checking for correct number of arguments
    if len(sys.argv) != 2:
        sys.stderr.write("Incorrect number of arguments.\n")
        exit(1)

    # Checking if file exists
    try:
        open(sys.argv[1], 'r')
    except:
        sys.stderr.write("Unable to open file.\n")
        exit(1)

    with open(sys.argv[1], 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            firstCol = row[0]
            if (firstCol == "SUPERBLOCK"):
                global superBlock
                superBlock = SuperBlock(row)
            elif (firstCol == "GROUP"):
                global groupList
                temp = Group(row)
                groupList.append(temp)
            elif (firstCol == "BFREE"):
                global freeBlockList
                global freeBlockArray
                temp = FreeBlockEntries(row)
                freeBlockList.append(temp)
                freeBlockArray.append(int(row[1]))
            elif (firstCol == "IFREE"):
                global freeInodeList
                temp = FreeInodeEntries(row)
                freeInodeList.append(temp)
            elif (firstCol == "DIRENT"):
                global directoryList
                temp = Directory(row)
                directoryList.append(temp)
            elif (firstCol == "INODE"):
                global inodeList
                tempInode = Inode(row)
                inodeList.append(tempInode)
            elif (firstCol == "INDIRECT"):
                global indirectList
                temp = IndirectBlockReferences(row)
                indirectList.append(temp)
    global refBlockList
    refBlockList = [[] for y in range(superBlock.totalNumBlocks)] #initialize

    findInodeInconsistencies()

    ####### Inode Allocation Audits #######
    accountedNodes = [1, 3, 4, 5, 6, 7, 8, 9, 10]
    allocInodes = []
    # Check every allocated inode and see if it's also on free list
    for inode in inodeList:
        accountedNodes.append(inode.inodeNum)
        allocInodes.append(inode.inodeNum)
        if (inode.fileType != 0):
            for freeNode in freeInodeList:
                if (freeNode.freeInodeNum == inode.inodeNum):
                    print("ALLOCATED INODE " + str(inode.inodeNum) + " ON FREELIST")

    # Put all free inodes on accountedNodes list
    for freeNode in freeInodeList:
        accountedNodes.append(freeNode.freeInodeNum)

    # If inode isn't on accountedNodes list, then it's an unallocated
    # inode that's not on the free list
    for i in range(1, superBlock.totalNumInodes + 1):
        if i not in accountedNodes:
            print("UNALLOCATED INODE " + str(i) + " NOT ON FREELIST") 

    ####### Directory Consistency Audits #######
    for inode in inodeList:
        reference = inode.linkCount
        number = inode.inodeNum
        count = 0
        for directory in directoryList:
            fileInode = directory.referencedFileInodeNum
            if (number == fileInode):
                count += 1
        if (count != reference):
            print("INODE " + str(number) + " HAS " + str(count) + " LINKS BUT LINKCOUNT IS " + str(reference))

    child2Parent = {}
    parents = {}

    # Checking each directory entry
    for directory in directoryList:
        fileInode = directory.referencedFileInodeNum
        parent = directory.parentInode
        # Invalid inode
        if (fileInode < 1 or fileInode > superBlock.totalNumInodes):
            print("DIRECTORY INODE " + str(parent) + " NAME " + directory.name + " INVALID INODE " + str(fileInode))
        # Checks allocInodes list to see if inode is allocated
        elif (fileInode not in allocInodes):
            print("DIRECTORY INODE " + str(parent) + " NAME " + directory.name + " UNALLOCATED INODE " + str(fileInode))
        # Checking that the link (.) is to itself
        if (directory.name == "'.'" and parent != fileInode):
            print("DIRECTORY INODE " + str(parent) + " NAME " + directory.name + " LINK TO INODE " + str(fileInode) + " SHOULD BE " + str(parent))
        # Adding each referenced file and parent pair to a dictionary
        if (directory.name != "'.'" and directory.name != "'..'"):
            child2Parent[fileInode] = parent
        if (directory.name == "'..'"):
            parents[parent] = fileInode

    # Checking for correctness of 2 links
    for parent in parents:
        if (parent == 2 and parents[parent] != 2):
            print("DIRECTORY INODE " + str(parent) + " NAME '..' LINK TO INODE " + str(parents[parent]) + " SHOULD BE " + str(parent))
        elif (parent == 2):
            continue
        elif (parents[parent] != child2Parent[parent]):
            print("DIRECTORY INODE " + str(parent) + " NAME '..' LINK TO INODE " + str(parents[parent]) + " SHOULD BE " + str(child2Parent[parent]))

if __name__ == "__main__": 
    main()
