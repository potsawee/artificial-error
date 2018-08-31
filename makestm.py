#!/usr/bin/python3
"""
Convert from inc/spell/corr to stm
E.g.
(1) AU*111*0265*0381*2000*42-1-1 From the chart we can see the difference between the levels of participation in education and science between developing countries and industrialised countries from 1980 to 1990 .
(stm) ID 1 aggregate 0.000 80.000 ..........

Args:
    orig: inc/spell/corr file in the /home/alta/CLC/exams/LNRC/*/*.(inc/spell/corr)
    stm: output file name

Output:
    stm format the specified location

"""

import sys
from collections import OrderedDict

def convert(orig, stm):
    with open(orig, 'r') as file:
        lines = file.readlines()
    dict = OrderedDict()

    for line in lines:
        items = line.split()
        if(len(items) <= 1):
            items.append('*emp*')
            # continue
        id = items[0]
        # sentence = ' '.join(items[1:])
        if not id[-1].isdigit():
            id = id[:-1]
        if id in dict:
            dict[id].extend(items[1:])
        else:
            dict[id] = items[1:]
        # file.write("{} 1 aggregate 0.000 80.000 {}\n".format(id, sentence))
    with open(stm, 'w') as file:
        for id, words in dict.items():
            sentence = ' '.join(words)

            # ; causes the mis-alignment problem --- @potsawee 14 Aug 2018
            sentence = sentence.replace(" ;", " ,")
            sentence = sentence.replace("(", "")
            sentence = sentence.replace(")", "")
            if sentence == "":
                sentence = "*emp*"

            file.write("{} 1 aggregate 0.000 80.000 {}\n".format(id, sentence))

def main():
    if(len(sys.argv) != 3):
        print("Usage python3 makestm.py orig stm")
    orig = sys.argv[1]
    stm = sys.argv[2]
    # orig = "/home/alta/CLC/LNRC/exams/IELTS/2000_44.corr"
    # stm = "/home/alta/BLTSpeaking/ged-pm574/artificial-error/work/try.stm"
    convert(orig, stm)
    # print("convert to stm done!")

if __name__ == "__main__":
    main()
