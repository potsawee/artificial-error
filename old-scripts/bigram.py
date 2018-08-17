import sys
import numpy as np
from operator import itemgetter
import pdb
from tqdm import tqdm

class BigramModel(object):
    def __init__(self):
        self.bigrams_count = {}             # bigrams_count[(I,sing)] = 100
        self.bigram_pairs_count = {}        # bigram_pairs_count[ ( (I,sing) , (I,sings) ) ] = 5
        self.bigrams_dict = {}              # bigrams_dict[(I,sing)] = [(I,sings), (I,****), (I,sang), ...]  ... not contain itself
        self.transition_probs = {}          # transition_probs[((I,sing),(I,sings))] = P((I,sing)->(I,sings)) = 0.05
        self.pmf = {}                       # pmf[(I,sing)] = [P((I,sing)->(I,sing)), P((I,sing)->each bigram in bigrams dict)] ... sum this must be 1
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

        # reference bigram - correct (r0,r1)
        bigram_r = None
        # hypothesis bigram - incorrect (h0,h1)
        bigram_h = None
        # label
        l0 = None
        l1 = None

        for idx in tqdm(range(len(lines)-1)):
            line0 = lines[idx]
            line1 = lines[idx+1]

            if line0 == '\n' or line1 == '\n':
                continue

            items0 = line0.split('\t')
            try:
                r0 = items0[0].lower()
                h0 = items0[1].lower()
                l0 = items0[-1].strip()
            except:
                print(idx, line0)

            items1 = line1.split('\t')
            try:
                r1 = items1[0].lower()
                h1 = items1[1].lower()
                l1 = items1[-1].strip()
            except:
                print(idx+1, line1)

            bigram_r = (r0,r1)
            bigram_h = (h0,h1)

            if bigram_r not in self.bigrams_count:
                self.bigrams_count[bigram_r] = 1
            else:
                self.bigrams_count[bigram_r] += 1

            if l0 == 'i' or l1 == 'i':
                if (bigram_r,bigram_h) not in self.bigram_pairs_count:
                    self.bigram_pairs_count[(bigram_r,bigram_h)] = 1
                else:
                    self.bigram_pairs_count[(bigram_r,bigram_h)] += 1

                if bigram_r not in self.bigrams_dict:
                    self.bigrams_dict[bigram_r] = [bigram_h]
                else:
                    if bigram_h not in self.bigrams_dict[bigram_r]:
                        self.bigrams_dict[bigram_r].append(bigram_h)

    def build_transition_probs(self):
        for bigram1, v in self.bigrams_dict.items():
            sum_prob = 0
            self.pmf[bigram1] = []
            for bigram2 in v:
                prob = self.prob(bigram1,bigram2)
                sum_prob += prob
                self.transition_probs[(bigram1,bigram2)] = prob
                self.pmf[bigram1].append(prob)
            # this sum_prob is the probability that the bigram changes
            # so if it is more than one, something went wrong => do not build the pmf
            if sum_prob > 1.0:
                self.transition_probs[(bigram1,bigram1)] = 0
                del self.pmf[bigram1]
            else:
                self.transition_probs[(bigram1,bigram1)] = 1-sum_prob
                self.pmf[bigram1] = [1-sum_prob] + self.pmf[bigram1]

    def prob(self, bigram_r, bigram_h):
        return self.bigram_pairs_count[(bigram_r,bigram_h)] / self.bigrams_count[bigram_r]

    # Propagate error
    def emit(self, bigram, gain=None):
        """
        Emit a bigram according to the probability distribution
        of the bigram model
        e.g. P((I,sing)->(I,sings)) = 0.05

        => gain: pmf'(!same) = min[gain x pmf(!same), 1]
                 pmf'(same)  = 1 - pmf'(!same)
        """
        if bigram not in self.pmf:
            return bigram
        else:
            if gain == None:
                # try:
                bigrams_list = [bigram]+self.bigrams_dict[bigram]
                x = np.random.choice(range(len(bigrams_list)), size=1, p=self.pmf[bigram])
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

                bigrams_list = [bigram]+self.bigrams_dict[bigram]
                x = np.random.choice(range(len(bigrams_list)), size=1, p=new_pmf)

        return bigrams_list[x[0]]
