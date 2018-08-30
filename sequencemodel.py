import sys
import numpy as np
from operator import itemgetter
import pdb
from tqdm import tqdm

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
            lines = file.readlines()

        # reference word - correct
        r = None
        # hypothesis word - incorrect
        h = None
        # label
        l = None
        for idx in tqdm(range(len(lines))):
            line = lines[idx]

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
            # this sum_prob is the probability that the word changes
            # so if it is more than one, something went wrong => do not build the pmf
            if sum_prob > 1.0:
                self.transition_probs[(w1,w1)] = 0
                del self.pmf[w1]
            else:
                self.transition_probs[(w1,w1)] = 1-sum_prob
                self.pmf[w1] = [1-sum_prob] + self.pmf[w1]

    def prob(self, r, h):
        return self.pairs_count[(r,h)] / self.words_count[r]

    # Propagate error
    def emit(self, word, gain=None):
        """
        Emit a word according to the probability distribution
        of the unigram model
        e.g. P(cat->cats) = 0.2

        => gain: pmf'(!same) = min[gain x pmf(!same), 1]
                 pmf'(same)  = 1 - pmf'(!same)
        """
        if word not in self.pmf:
            return word
        else:
            if gain == None:
                # try:
                x = np.random.choice([word]+self.words_dict[word], size=1, p=self.pmf[word])
                # except ValueError:
                #     print("PMF-ERROR: {} - sum(pmf) = {}, pmf = {}".format(word, sum(self.pmf[word]),self.pmf[word]))
                #     return word
            else:
                new_pmf = []
                boosted = [gain * p for p in self.pmf[word][1:]]
                if sum(boosted) < 1.0:
                    new_pmf.append(1.0-sum(boosted))
                    new_pmf += boosted

                else: # gain is too large
                    factor = 1.0 / sum(self.pmf[word][1:])
                    new_pmf.append(0.0)
                    new_pmf += [factor * p for p in self.pmf[word][1:]]

                x = np.random.choice([word]+self.words_dict[word], size=1, p=new_pmf)

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

class BigramModel(object):
    def __init__(self):
        self.bigrams_count = {}       # bigrams_count[(I,sing)] = 100
        self.pairs_count = {}         # pairs_count[((I,sing), sings)] = 5
        self.bigrams_dict = {}        # bigrams_dict[(I,sing)] = [sings, song, ****, ...]  ... not contain itself
        self.transition_probs = {}    # transition_probs[((I,sing),sings)] = P(sing->sings | I) = 0.05
        self.pmf = {}                 # pmf[(I,sing)] = [P((I,sing)->sing), P((I,sing)->each bigram in bigrams dict)] ... sum this must be 1
        self.filepath = None

    # Building a Bigram Model
    def readin(self, filepath):
        self.filepath = filepath

    def construct_model(self):
        self.count_bigrams()
        self.build_transition_probs()

    def count_bigrams(self):
        with open(self.filepath, 'r') as file:
            lines = file.readlines()

        start_tag = "<s>"
        # 0-th => previous
        # 1-st => current

        # reference bigram - correct
        r0 = None
        r1 = start_tag # so that the first iteration, this value gets passed to r0
        # hypothesis word - incorrect
        h1 = None
        # label
        l1 = None

        for idx in tqdm(range(len(lines))):
            line = lines[idx]

            if line == '\n':
                # more than one empty line
                # if lines[idx+1] == '\n':
                    # pass
                # end of sentence
                # else:
                r1 = start_tag
                continue

            items = line.split('\t')
            r0 = r1
            try:
                r1 = items[0].lower()
                h1 = items[1].lower()
                l1 = items[-1].strip()
            except:
                print(idx, line)

            bigram_r = (r0,r1)

            if bigram_r not in self.bigrams_count:
                self.bigrams_count[bigram_r] = 1
            else:
                self.bigrams_count[bigram_r] += 1

            if l1 == 'i':
                if (bigram_r,h1) not in self.pairs_count:
                    self.pairs_count[(bigram_r,h1)] = 1
                else:
                    self.pairs_count[(bigram_r,h1)] += 1

                if bigram_r not in self.bigrams_dict:
                    self.bigrams_dict[bigram_r] = [h1]
                else:
                    if h1 not in self.bigrams_dict[bigram_r]:
                        self.bigrams_dict[bigram_r].append(h1)

    def build_transition_probs(self):
        for bigram, words in self.bigrams_dict.items():
            sum_prob = 0
            self.pmf[bigram] = []
            for word in words:
                prob = self.prob(bigram,word)
                sum_prob += prob
                self.transition_probs[(bigram,word)] = prob
                self.pmf[bigram].append(prob)
            # this sum_prob is the probability that the (current) word changes
            # so if it is more than one, something went wrong => do not build the pmf
            if sum_prob > 1.0:
                self.transition_probs[(bigram,bigram[1])] = 0
                del self.pmf[bigram]
            else:
                self.transition_probs[(bigram,bigram[1])] = 1-sum_prob
                self.pmf[bigram] = [1-sum_prob] + self.pmf[bigram]

    def prob(self, bigram, h):
        return self.pairs_count[(bigram,h)] / self.bigrams_count[bigram]

    # Propagate error
    def emit(self, bigram, gain=None):
        """
        Emit a word according to the probability distribution
        of the bigram model
        e.g. P(sing->sings | I) = 0.05
        """
        if bigram not in self.pmf:
            return bigram[1]
        else:
            if gain == None:
                # try:
                x = np.random.choice([bigram[1]]+self.bigrams_dict[bigram], size=1, p=self.pmf[bigram])
                # except ValueError:
                #     print("PMF-ERROR: {} - sum(pmf) = {}, pmf = {}".format(bigram, sum(self.pmf[bigram]),self.pmf[bigram]))
                #     return bigram
            else:
                new_pmf = []
                boosted = [gain * p for p in self.pmf[bigram][1:]]
                if sum(boosted) < 1.0:
                    new_pmf.append(1.0-sum(boosted))
                    new_pmf += boosted

                else: # gain is too large
                    factor = 1.0 / sum(self.pmf[bigram][1:])
                    new_pmf.append(0.0)
                    new_pmf += [factor * p for p in self.pmf[bigram][1:]]

                x = np.random.choice([bigram]+self.bigrams_dict[bigram], size=1, p=new_pmf)

        return x[0]

class UnigramCount(object):
    def __init__(self):
        self.words_count = {} # words_count[staff] = 5000
    def readfile(self, filepath):
        with open(filepath, 'r') as file:
            lines = file.readlines()

        for idx in tqdm(range(len(lines))):
            line = lines[idx]
            if line == '\n':
                continue

            word = line.strip()
            if word not in self.words_count:
                self.words_count[word] = 1
            else:
                self.words_count[word] += 1


def handle_insertion(input, output):
    '''
    to convert from .gedx.tsv to .gedx.ins.tsv
    this is mainly to do with combine insertion to the word nearby
    Args:
        - input:  .gedx.tsv
        - output: .gedx.ins.tsv
    '''
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

def ins():
    input = "/home/alta/BLTSpeaking/ged-pm574/artificial-error/work-24082018/master.gedx.tsv"
    output = "/home/alta/BLTSpeaking/ged-pm574/artificial-error/work-24082018/master.gedx.ins.tsv"
    handle_insertion(input, output)

def main():
    if(len(sys.argv) < 2):
        return
    arg1 = sys.argv[1]
    if arg1 == 'ins':
        print("handling insertion...")
        ins()

if __name__ == "__main__":
    main()
