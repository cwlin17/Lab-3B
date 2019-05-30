# NAME: Don Le, Carol Lin
# EMAIL: donle22599@g.ucla.edu, carol9gmail@yahoo.com
# ID: 804971410, 804984337

#!/usr/bin/python

import sys, csv

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
