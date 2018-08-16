import sys
from unigram import *
from bigram import *
def stat1():
    """
    Word count, Percentage errors etc
    """

    path = '/home/alta/BLTSpeaking/ged-pm574/artificial-error/lib/gedx-tsv/work-14082018/master.gedx.tsv'

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

def stat2():
    """
    Unigram transition statistics
    """
    gedx_path = "/home/alta/BLTSpeaking/ged-pm574/artificial-error/lib/gedx-tsv/work-14082018/master.gedx.ins.tsv"
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

def stat3():
    """
    Bigram transition statistics
    """
    gedx_path = "/home/alta/BLTSpeaking/ged-pm574/artificial-error/lib/gedx-tsv/work-14082018/master.gedx.ins.tsv"
    gedx_path = "/home/alta/BLTSpeaking/ged-pm574/artificial-error/lib/gedx-tsv/work-14082018/master.gedx.ins.tsv"
    print("Loading... {}".format(gedx_path))
    model = BigramModel()
    model.readin(gedx_path)
    model.construct_model()
    print("Model built!")

    i = 0
    print("--------------------------------------------------------------------")
    print("{:24} => {:24} : count".format('correct_bigram', 'incorrect_bigram'))
    print("--------------------------------------------------------------------")
    for bigram_pair, count in sorted(model.bigram_pairs_count.items(), key=lambda x:x[1])[::-1]:
        print("{:12}{:12} => {:12}{:12} : {}".format(bigram_pair[0][0], bigram_pair[0][1], bigram_pair[1][0], bigram_pair[1][1], count))
        i += 1
        if i == 500:
            return

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 simple_clc_stat.py option")
        return
    option = sys.argv[1]
    if option == '1':
        stat1()
    elif option == 'unigram':
        stat2()
    elif option == 'bigram':
        stat3()
    else:
        print("option invalid")

if __name__ == "__main__":
    main()
