#!/usr/bin/python3
import sys
from sequencemodel import UnigramModel
from sequencemodel import BigramModel
from sequencemodel import UnigramCount
from data_processing import *
from string import punctuation
from tqdm import tqdm

# quick implementation for corrupting a file

# mapping = {
#     "'s": 'is',
#     "n't": 'not',
#     "'re": 'are',
#     "'m": 'am',
#     "'ve": 'have',
#     "'ll": 'will',
#     "'d": 'had'
# }

def corrupt(gedx_path, input_path, output_path, model_type):
    # ----------- ged.tsv ------------ #
    with open(input_path, 'r') as file:
        lines = file.readlines()

    # gedx_path = "/home/alta/BLTSpeaking/ged-pm574/artificial-error/lib/gedx-tsv/dtal-291018/dtal.gedx.ins.tsv"
    print("Loading... {}".format(gedx_path))
    # ----- Model selection ----- #
    # Unigram
    if model_type == 'unigram':
        model = UnigramModel()

    # Bigram
    elif model_type == 'bigram':
        start_tag = "<s>"
        token = start_tag
        model = BigramModel()
    # -------------------------- #
    model.readin(gedx_path)
    model.construct_model()
    print("Model built!")

    # ------- Balancing distributions for words across CLC/Speech  ------ #
    # @potsawee - 28 August 2018
    # only support unigram model!
    if model_type == 'unigram':

        target_stat = UnigramCount()
        target_stat.readfile(input_path)
        # if P(w1 -> w2) * count_target(w1) > count_target(w2)
        # reduce P(w1 -> w2) to  count_target(w2) / count_target(w1)
        # re-adjust the pmf[w1] i.e. increase P(w1 -> w1) so that the sum is 1.0

        count_not_in_model = 0
        count_err_too_high = 0
        count_err_okay = 0

        for w1 in target_stat.words_count:
            if w1 not in model.words_dict:
                count_not_in_model += 1
                continue

            transition_prob_changed = False

            for w2 in model.words_dict[w1]:
                # INSERTION / DELETION => do not change the transition prob!
                if len(w2.split()) > 1 or '*' in w2:
                    pass
                # SUBSTITUTION
                else:
                    if w2 in target_stat.words_count:
                        target_w2_count = target_stat.words_count[w2]
                    else:
                        target_w2_count = 0
                    if model.transition_probs[(w1,w2)] * target_stat.words_count[w1] > 0.1 * target_w2_count:
                        model.transition_probs[(w1,w2)] = 0.1 * target_w2_count / target_stat.words_count[w1]
                        transition_prob_changed = True
            if transition_prob_changed:
                new_pmf = []
                for w2 in model.words_dict[w1]:
                    new_pmf.append(model.transition_probs[(w1,w2)])
                new_pmf = [1-sum(new_pmf)] + new_pmf
                model.pmf[w1] = new_pmf
                count_err_too_high += 1
            else:
                count_err_okay += 1

            # TODO: Fix how the corpus is corrupted here!
            ### w0 -> w1
            ### w1 -> w2
            # if w1 not in model.words_dict:
            #     count_not_in_model += 1
            #     continue
            # transition_prob_changed = False
            # for w2 in model.words_dict[w1]:
            #     # INSERTION / DELETION => do not change the transition prob!
            #     if len(w2.split()) > 1 or '*' in w2:
            #         pass
            #     # SUBSTITUTION
            #     else:
            #         if w2 in target_stat.words_count:
            #             target_w2_count = target_stat.words_count[w2]
            #         else:
            #             target_w2_count = 0
            #         sum_prob_w_r = 0
            #         expected_err = 0
            #         for w_r in model.rev_words_dict[w2]:
            #             sum_prob_w_r += model.transition_probs[(w_r, w2)]
            #             if w_r not in target_stat.words_count:
            #                 tgt_word_count_w_r = 0
            #             else:
            #                 tgt_word_count_w_r = target_stat.words_count[w_r]
            #             expected_err += model.transition_probs[(w_r,w2)] * tgt_word_count_w_r

        print("Error exploding problem checked!")
        print("Count word not in the model:   ", count_not_in_model)
        print("Count word prob being too high:", count_err_too_high)
        print("Count word prob being okay:    ", count_err_okay)
        print("Total word count in target:    ", len(target_stat.words_count))
    # ------------------------------------------------------------------ #

    sentences = []
    sentence = [] # start with a word, end with a full stop
                  # [('the', 'c'), ('cat', 'c'), ...]

    deletion = "<DEL>"
    sub_count = 0
    ins_count = 0
    del_count = 0
    good_count = 0

    print("Propagating the errors...")
    for idx in tqdm(range(len(lines))):
        line = lines[idx]
        # ------------- Unigram ------------- #
        if model_type == 'unigram':
            if line == '\n':
                sentences.append(sentence)
                sentence = []
                continue

            # token = line.strip()
            token = line.split()[0]
            others = line.split()[1:]

            # No error boosting
            emitted = model.emit(token)
            # With error boosting
            # emitted = model.emit(token, gain=1.2)
        # ----------------------------------- #

        # ------------- Bigram -------------- #
        elif model_type == 'bigram':
            if line == '\n':
                sentences.append(sentence)
                sentence = []
                token = start_tag
                continue

            prev_token = token
            # token = line.strip()
            token = line.split()[0]
            others = line.split()[1:]

            bigram = (prev_token,token)

            emitted = model.emit(bigram)
        # ----------------------------------- #


        # insertion
        if(len(emitted.split()) >= 2):
            x = emitted.split()
            if(x[0] == token):
                items = [x[0]] + others + ['c']
                sentence.append(items)
                items = [x[1]] + ['_', '_'] + ['i']
                sentence.append(items)
            else:
                items = [x[0]] + ['_', '_'] + ['i']
                sentence.append(items)
                items = [x[1]] + others + ['c']
                sentence.append(items)
            ins_count += 1

        # deletion
        elif '*' in emitted:
            items = [deletion] + others + ['i']
            sentence.append(items)
            del_count += 1

        # Substitution or No-error
        else:
            # Substitution
            if token != emitted:
                items = [emitted] + others + ['i']
                sentence.append(items)
                sub_count += 1

            # No-error
            else:
                items = [token] + others + ['c']
                sentence.append(items)
                good_count +=1

    print("good_count:", good_count)
    print("sub_count:", sub_count)
    print("ins_count:", ins_count)
    print("del_count:", del_count)

    with open(output_path, 'w') as file:
        for sentence in sentences:
            idx = 0
            while(idx < len(sentence)):
                word = sentence[idx]
                if word[0] != deletion:
                    file.write("{}\n".format('\t'.join(word)))
                else:
                    while sentence[idx][0] == deletion:
                        idx += 1
                        if idx == len(sentence):
                            break
                    if(idx < len(sentence)):
                        word = sentence[idx]
                        # file.write("{}\ti\n".format(word[0]))
                        file.write("{}\ti\n".format('\t'.join(word[:-1])))
                    else:
                        pass
                idx += 1
            file.write("\n")

    print("{} done".format(output_path))
    print("------ Summary ------")
    print("num_words = {}".format(good_count+sub_count+ins_count+del_count))
    print("%error = {:.2f}".format((sub_count+ins_count+del_count)/good_count*100))
    print("%sub = {:.2f}".format(sub_count/good_count*100))
    print("%ins = {:.2f}".format(ins_count/good_count*100))
    print("%del = {:.2f}".format(del_count/good_count*100))



def main():
    if(len(sys.argv) != 5):
        print("Usage: python3 corrupt.py gedx input output [unigram/bigram]")
        return

    gedx_path = sys.argv[1]
    input_path = sys.argv[2]
    output_path = sys.argv[3]
    model_type = sys.argv[4].lower()

    if model_type not in ['unigram', 'bigram']:
        print("model type error")
        return

    corrupt(gedx_path, input_path, output_path, model_type)

if __name__ == '__main__':
    main()
