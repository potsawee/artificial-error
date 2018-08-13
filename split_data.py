import sys
import random

def main():
    if(len(sys.argv) != 4):
        print("Usage: python3 split_data.py orig tgt name")

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
            file.write(".\tc\n")
            for line in sentence:
                file.write(line)
            file.write('\n')
    # Dev set
    with open(path_dev, 'w') as file:
        for sentence in sentences[2500:5000]:
            file.write(".\tc\n")
            for line in sentence:
                file.write(line)
            file.write('\n')
    # Train set
    with open(path_train, 'w') as file:
        for sentence in sentences[5000:]:
            file.write(".\tc\n")
            for line in sentence:
                file.write(line)
            file.write('\n')


if __name__ == "__main__":
    main()
