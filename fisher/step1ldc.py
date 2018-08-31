#!/usr/bin/python3
"""
Step 1 LDC:
    - Transcripts come from either LDC or BBN/WordWave => This script works with LDC
    - Processing from the raw Fisher CTS data
    - No word removal is done here

    Input e.g. /home/alta/CTS/Fisher/transcripts/fsh_qt_eng_tr_030416/transcr/fsh_60081.txt:
    0.75 1.14 A: hello

    1.38 1.86 B: hi

    11.06 16.28 A: i'd be impressed if you could get to your doctor in seven days with only cold symptoms (( )) we're on a ~hmo right now and

    16.39 16.96 A: (( ))

    17.35 18.01 B: oh

    Output:
    fsh_60081 hello
    fsh_60081 hi
    fsh_60081 i'd be impressed if you could get to your doctor in seven days with only cold symptoms (( )) we're on a ~hmo right now and
    fsh_60081 (( ))
    fsh_60081 oh
"""

import sys
import os
# import pdb

def main():
    if(len(sys.argv) != 2):
        print("Usage: python3 step1ldc.py input")
        return

    input = sys.argv[1]

    fileid = os.path.basename(input).split(".")[0]

    with open(input, 'r') as file:
        lines = file.readlines()

    for line in lines:
        if line == '\n':
            continue

        items = line.split()
        if(len(items) <= 3):
            continue

        sentence = ' '.join(items[3:])
        print("{} {}".format(fileid, sentence))



if __name__ == "__main__":
    main()
