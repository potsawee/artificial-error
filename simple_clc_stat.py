#!/usr/bin/python3
'''
Print the error statistics of the CLC from .gedx.tsv file
e.g. http://mi.eng.cam.ac.uk/raven/esol/ind_reports/pm574/UROP3/clc_stat.pdf

Args:
    - gedx_path: path to gedx_path
    - [1/unigram/bigram]
        - 1 = simple stat (word count, percentage error)
        - unigram = unigram transition
        - bigram = bigram transition
Output:
    - Print the statistics to the terminal
'''

import sys
from sequencemodel import *

def stat1(path):
    """
    Word count, Percentage errors etc
    """

    # path = '/home/alta/BLTSpeaking/ged-pm574/artificial-error/lib/gedx-tsv/work-14082018/master.gedx.tsv'

    sub_count = 0
    ins_count = 0
    del_count = 0
    good_count = 0

    with open(path) as file:
        for line in file:
            if line == '\n':
                continue

            items = line.split()
            r = items[0] # ref (correct)
            h = items[1] # hyp (correct/incorrect)
            l = items[-1] # label

            if r == h:
                good_count += 1
            elif '*' in r:
                ins_count += 1
            elif '*' in h:
                del_count += 1
            else:
                sub_count += 1

    print("good_count:", good_count)
    print("sub_count:", sub_count)
    print("ins_count:", ins_count)
    print("del_count:", del_count)
    print("------ Summary ------")
    print("num_words = {}".format(good_count+sub_count+ins_count+del_count))
    print("%error = {:.2f}".format((sub_count+ins_count+del_count)/good_count*100))
    print("%sub = {:.2f}".format(sub_count/good_count*100))
    print("%ins = {:.2f}".format(ins_count/good_count*100))
    print("%del = {:.2f}".format(del_count/good_count*100))

def stat2(gedx_path):
    """
    Unigram transition statistics
    """
    # gedx_path = "/home/alta/BLTSpeaking/ged-pm574/artificial-error/lib/gedx-tsv/work-14082018/master.gedx.ins.tsv"
    print("Loading... {}".format(gedx_path))
    model = UnigramModel()
    model.readin(gedx_path)
    model.construct_model()
    print("Model built!")

    i = 0
    print("--------------------------------------------------------------------")
    print("{:15} => {:15} : count".format('correct', 'incorrect'))
    print("--------------------------------------------------------------------")
    for pair, count in sorted(model.pairs_count.items(), key=lambda x:x[1])[::-1]:
        print("{:15} => {:15} : {}".format(pair[0], pair[1], count))
        i += 1
        if i == 500:
            return

def stat3(gedx_path):
    """
    Bigram transition statistics
    """
    # gedx_path = "/home/alta/BLTSpeaking/ged-pm574/artificial-error/lib/gedx-tsv/work-14082018/master.gedx.ins.tsv"
    print("Loading... {}".format(gedx_path))
    model = BigramModel()
    model.readin(gedx_path)
    model.construct_model()
    print("Model built!")

    i = 0
    print("--------------------------------------------------------------------")
    print("{:15}{:15} => {:15}: count".format('correct', 'incorrect', 'given_prev'))
    print("e.g count(sing->sings | I)")
    print("count #sing => #sings given that the previous word is I")
    print("--------------------------------------------------------------------")
    for pair, count in sorted(model.pairs_count.items(), key=lambda x:x[1])[::-1]:
        bigram, word = pair
        print("{:15} => {:15} | {:15} : {}".format(bigram[1], word, bigram[0], count))
        i += 1
        if i == 500:
            return

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 simple_clc_stat.py gedx_path [1/unigram/bigram]")
        return

    gedx_path = sys.argv[1]
    option = sys.argv[2]

    if option == '1':
        stat1(gedx_path)
    elif option == 'unigram':
        stat2(gedx_path)
    elif option == 'bigram':
        stat3(gedx_path)
    else:
        print("option invalid")

if __name__ == "__main__":
    main()
