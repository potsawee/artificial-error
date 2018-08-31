#!/usr/bin/python3
'''
Split .ged.tsv file into training/dev/test sets
    - Test set     = 2500 sentences
    - Dev set      = 2500 sentences
    - Training set = the rest of the data
    - seed number "myseed = 10"

Args:
    orig: path to the original .ged.tsv file
    tgt: path to the target directory
    name: name of the output files

Output:
    1. tgt/name.train.ged.tsv
    2. tgt/name.dev.ged.tsv
    3. tgt/name.test.ged.tsv
'''

import sys
import random

def main():
    if(len(sys.argv) != 4):
        print("Usage: python3 split_data.py orig tgt name")
        return

    # orig = '/home/alta/BLTSpeaking/ged-pm574/artificial-error/lib/ami-monday2.ged.tsv'
    # path_train = '/home/alta/BLTSpeaking/ged-pm574/artificial-error/lib/tsv/ami-monday2.train.ged.tsv'
    # path_dev = '/home/alta/BLTSpeaking/ged-pm574/artificial-error/lib/tsv/ami-monday2.dev.ged.tsv'
    # path_test = '/home/alta/BLTSpeaking/ged-pm574/artificial-error/lib/tsv/ami-monday2.test.ged.tsv'
    orig = sys.argv[1]
    tgt = sys.argv[2]
    name = sys.argv[3]
    path_train = tgt + name + '.train.ged.tsv'
    path_dev = tgt + name + '.dev.ged.tsv'
    path_test = tgt + name + '.test.ged.tsv'


    with open(orig, 'r') as file:
        lines = file.readlines()

    sentences = []
    sentence = []
    for line in lines:
        if line != '\n':
            sentence.append(line)
        else:
            sentences.append(sentence)
            sentence = []

    myseed = 10
    random.seed(myseed)
    random.shuffle(sentences)

    # print(len(sentences))
    # print(sentences[:3])

    # Test set
    with open(path_test, 'w') as file:
        for sentence in sentences[:2500]:
            if len(sentence) < 1:
                continue
            # file.write(".\tc\n")
            file.write("</s>\tc\n")
            for line in sentence:
                file.write(line)
            # file.write(".\tc\n\n")
            file.write("</s>\tc\n\n")

    # Dev set
    with open(path_dev, 'w') as file:
        for sentence in sentences[2500:5000]:
            if len(sentence) < 1:
                continue
            # file.write(".\tc\n")
            file.write("</s>\tc\n")
            for line in sentence:
                file.write(line)
            # file.write(".\tc\n\n")
            file.write("</s>\tc\n\n")

    # Train set
    with open(path_train, 'w') as file:
        for sentence in sentences[5000:]:
            if len(sentence) < 1:
                continue
            # file.write(".\tc\n")
            file.write("</s>\tc\n")
            for line in sentence:
                file.write(line)
            # file.write(".\tc\n\n")
            file.write("</s>\tc\n\n")


if __name__ == "__main__":
    main()
