"""
Step 1 BBN:
    - Transcripts come from either LDC or BBN/WordWave => This script works with BBN
    - Processing from the raw Fisher CTS data
    - No word removal is done here

    Input e.g. /home/alta/CTS/Fisher/transcripts/fsh_qt_eng_tr_031016/bbn:
    HI MY NAME IS SCOOTER (fsh_60590-A-0001)
    NICE TO MEET YOU TOO WHERE ARE YOU LOCATED OH OKAY SO THIS THING STRETCHES OUT PRETTY FAR I'M IN NEW JERSEY (fsh_60590-A-0002)
    I'M NOT I'M NOT THAT FAR FROM YOU AT ALL ALL (fsh_60590-A-0003)
    RIGHT YOU GO FIRST (fsh_60590-A-0004)

    Output:
    fsh_60590 hi my name is scooter
    fsh_60590 nice to meet you too where are you located oh okay so this thing stretches out pretty far i'm in new jersey
    fsh_60590 i'm not i'm not that far from you at all all
    fsh_60590 right you go first
"""

import sys
import os
# import pdb

def main():
    if(len(sys.argv) != 2):
        print("Usage: python3 step1bbn.py input")
        return

    input = sys.argv[1]

    with open(input, 'r') as file:
        lines = file.readlines()

    for line in lines:
        if line == '\n':
            continue

        items = line.lower().split()

        if(len(items) <= 1):
            print("File: {}\nLine: {}".format(input, line))
            continue

        sentence = ' '.join(items[:-1])
        id = items[-1].strip('()').split('-')[0]
        print("{} {}".format(id, sentence))



if __name__ == "__main__":
    main()
