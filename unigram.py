import sys
import numpy as np
from operator import itemgetter
import pdb

class UnigramModel(object):
    def __init__(self):
        self.words_count = {}       # words_count[have] = 100
        self.pairs_count = {}       # pairs_count[(have,had)] = 20
        self.words_dict = {}        # words_dict[have] = [has, had, ****, ...]  ... not contain itself
        self.transition_probs = {}  # transition_probs[(have,had)] = P(have->had) = 0.2
        self.pmf = {}               # pmf[have] = [P(have->have), P(have->each word in word dict)] ... sum this must be 1
        self.filepath = None

    # Building a Unigram Model
    def readin(self, filepath):
        self.filepath = filepath

    def construct_model(self):
        self.count_unigrams()
        self.build_transition_probs()

    def count_unigrams(self):
        with open(self.filepath, 'r') as file:
            # reference word - correct
            r = None
            # hypothesis word - incorrect
            h = None
            # label
            l = None
            for idx, line in enumerate(file):
                if line == '\n':
                    continue

                items = line.split('\t')

                try:
                    r = items[0].lower()
                    h = items[1].lower()
                    l = items[-1].strip()
                except:
                    print(idx, line)

                if r not in self.words_count:
                    self.words_count[r] = 1
                else:
                    self.words_count[r] += 1

                if l == 'i':
                    if (r,h) not in self.pairs_count:
                        self.pairs_count[(r,h)] = 1
                    else:
                        self.pairs_count[(r,h)] += 1

                    if r not in self.words_dict:
                        self.words_dict[r] = [h]
                    else:
                        if h not in self.words_dict[r]:
                            self.words_dict[r].append(h)

    def build_transition_probs(self):
        for w1, v in self.words_dict.items():
            sum_prob = 0
            self.pmf[w1] = []
            for w2 in v:
                prob = self.prob(w1,w2)
                sum_prob += prob
                self.transition_probs[(w1,w2)] = prob
                self.pmf[w1].append(prob)
            self.transition_probs[(w1,w1)] = 1-sum_prob
            self.pmf[w1] = [1-sum_prob] + self.pmf[w1]

    def prob(self, r, h):
        return self.pairs_count[(r,h)] / self.words_count[r]

    # Propagate error
    def emit(self, word):
        """
        Emit a word according to the probability distribution
        of the unigram model
        e.g. P(cat->cats) = 0.2
        """
        if word not in self.pmf:
            return word
        else:
            x = np.random.choice([word]+self.words_dict[word], size=1, p=self.pmf[word])
        return x[0]

    # Print methods - debugging etc.
    def print_unigrams(self, num=100):
        i = 0
        print("---------------------------------------------")
        print("Correct => Incorrect")
        print("---------------------------------------------")
        for key, value in sorted(self.pairs_count.items(), key = itemgetter(1), reverse = True):
            r = key[0]
            h = key[1]
            print("{:10} =>    {:10} : {:4.1f}% {}/{}".format(r,h,100*value/self.words_count[r],value,self.words_count[r]))
            i += 1
            if(i >= num):
                break

    def print_prob(self, r, h):
        print("{:10} =>    {:10} : {:4.1f}".format(r,h,100*self.prob(r,h)))

    def print_error(self, word):
        for err in self.words_dict[word]:
            self.print_prob(word, err)

    @staticmethod
    def handle_insertion(input, output):
        lines = []
        with open(input, 'r') as file:
            in_lines = file.readlines()
        for i, line in enumerate(in_lines):
            if line == '\n':
                lines.append(line)
                continue

            items = line.split()

            # Handle insertion problem
            if '*' in items[0]:
                # (1) embed the insertion to the previous word
                if lines[-1] != '\n':
                    prev = lines[-1].split()
                    lines[-1] = "{}\t{} {}\ti\n".format(prev[0], prev[1], items[1])
                # (2) if the insertion occurs at the beginning
                # embed to the next word
                else:
                    if in_lines[i+1] != '\n':
                        next = in_lines[i+1].split()
                        in_lines[i+1] = "{}\t{} {}\ti\n".format(next[0], items[1], next[1])
                continue

            # not endline not insertion
            lines.append(line)
        with open(output, 'w') as file:
            for line in lines:
                file.write(line)


# Testing the class
def test1():
    path = "/home/alta/BLTSpeaking/ged-pm574/artificial-error/gedx-tsv/master.gedx.ins.tsv"
    uni = UnigramModel()
    uni.readin(path)
    uni.construct_model()
    uni.print_unigrams()
    pdb.set_trace()
    pass

def ins():
    input = "/home/alta/BLTSpeaking/ged-pm574/artificial-error/lib/gedx-tsv/work-14082018/master.gedx.tsv"
    output = "/home/alta/BLTSpeaking/ged-pm574/artificial-error/lib/gedx-tsv/work-14082018/master.gedx.ins.tsv"
    UnigramModel.handle_insertion(input, output)

def main():
    if(len(sys.argv) < 2):
        return
    arg1 = sys.argv[1]
    if arg1 == 'test1':
        test1()
    elif arg1 == 'ins':
        ins()
if __name__ == "__main__":
    main()
