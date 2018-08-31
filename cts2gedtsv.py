#!/usr/bin/python3
import sys
from sequencemodel import UnigramModel
from sequencemodel import BigramModel
from sequencemodel import UnigramCount
from data_processing import *
from tqdm import tqdm

# CTS = Conversational Telephone Speech
# There are about 3 million words

def cts2gedtsv(cts, gedtsv, model_type):
    """

    This script is for processing the 'Switchboard' CTS corpus.

    original: the CTS corpus e.g. /home/nst/yq236/tools/kaldi-trunk-git/egs/swbd/s5c/data/train/text

    sw02001-A_001980-002131 um-hum
    sw02001-A_002736-002893 and is
    sw02001-A_003390-004012 right right is there is there um an- is there a like a code of dress where you work do they ask


    work12:    transcription + text processing
                1. one word per line format
                2. remove special tokens
                3. split multiple words
                4. parital word e.g. spee-
    work3:    more complicated text processing
                ### 1. US spelling => UK spelling !!! DTAL has both spelling
                2. Tokenisation e.g. don't => do n't // it's => it 's
    ged.tsv:  corrput the corpus using statistics from the model
    """

    myoutput = [gedtsv+'.work12.ged.tsv',
                gedtsv+'.work3.ged.tsv', gedtsv+'.ged.tsv']

    # ------------ Work 12 ------------ #
    with open(cts, 'r') as file:
        lines = file.readlines()
    with open(myoutput[0], 'w') as file:
        for line in lines:
            items = line.split()
            for token in items[1:]:

                if is_special_token_cts(token):
                    continue

                if '-' in token:
                    if token[0] != '-' and token[-1] != '-':
                        for word in token.split('-'):
                            if not is_hesitation(word):
                                file.write("{}\n".format(word.lower()))
                else:
                    if not is_hesitation(token):
                        file.write("{}\n".format(token.lower()))
                    else:
                        pass
            # file.write(".\n\n")
            file.write("\n")
    print("{} done".format(myoutput[0]))
    # -------------------------------- #

    # ------------ Work 3 ------------ #
    with open(myoutput[0], 'r') as file:
        lines = file.readlines()

    with open(myoutput[1], 'w') as file:
        for line in lines:

            # Empty lines
            if line == '\n':
                file.write(line)
                continue

            word = line.strip()

            # US to UK spelling
            # word = us_to_uk_spelling(word) #version4

            # tokenisation
            # if "'" in word:
            #     words = split_word(word)
            #     for word in words:
            #         file.write("{}\n".format(word))
            #     continue
            if "'" in word:
                if word in glm_mapping_kmk:
                    words = glm_mapping_kmk[word]
                    print("{}   =>  {}".format(word, words))
                    for word in words:
                        file.write("{}\n".format(word))
                    continue
                else:
                    pass
            file.write("{}\n".format(word))

    print("{} done".format(myoutput[1]))
    # -------------------------------- #

    # ----------- ged.tsv ------------ #

    with open(myoutput[1], 'r') as file:
        lines = file.readlines()

    gedx_path = "/home/alta/BLTSpeaking/ged-pm574/artificial-error/lib/gedx-tsv/work-24082018/master.gedx.ins.tsv"
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

    # ---------- Read the statistics of the AMI corpus --------- #
    # @potsawee - 28 August 2018
    # only support unigram model!
    if model_type == 'unigram':

        target_stat = UnigramCount()
        target_stat.readfile(myoutput[1])
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
    # --------------------------------------------------- #

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

            token = line.strip()

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
            token = line.strip()
            bigram = (prev_token,token)

            emitted = model.emit(bigram)
        # ----------------------------------- #

        # insertion
        if(len(emitted.split()) >= 2):
            x = emitted.split()
            if(x[0] == token):
                sentence.append((x[0], 'c'))
                sentence.append((x[1], 'i'))
            else:
                sentence.append((x[0], 'i'))
                sentence.append((x[1], 'c'))
            ins_count += 1

        # deletion
        elif '*' in emitted:
            sentence.append((deletion, 'i'))
            del_count += 1

        # Substitution or No-error
        else:
            # Substitution
            if token != emitted:
                sentence.append((emitted, 'i'))
                sub_count += 1

            # No-error
            else:
                sentence.append((token, 'c'))
                good_count +=1

    print("good_count:", good_count)
    print("sub_count:", sub_count)
    print("ins_count:", ins_count)
    print("del_count:", del_count)

    with open(myoutput[2], 'w') as file:
        for sentence in sentences:
            idx = 0
            while(idx < len(sentence)):
                word = sentence[idx]
                if word[0] != deletion:
                    file.write("{}\t{}\n".format(word[0], word[1]))
                else:
                    while sentence[idx][0] == deletion:
                        idx += 1
                        if idx == len(sentence):
                            break
                    if(idx < len(sentence)):
                        word = sentence[idx]
                        file.write("{}\ti\n".format(word[0]))
                    else:
                        pass
                idx += 1
            file.write("\n")

    print("{} done".format(myoutput[2]))
    print("------ Summary ------")
    print("num_words = {}".format(good_count+sub_count+ins_count+del_count))
    print("%error = {:.2f}".format((sub_count+ins_count+del_count)/good_count*100))
    print("%sub = {:.2f}".format(sub_count/good_count*100))
    print("%ins = {:.2f}".format(ins_count/good_count*100))
    print("%del = {:.2f}".format(del_count/good_count*100))

def main():
    if(len(sys.argv) != 2):
        print("Usage: python3 cts2gedtsv.py [unigram/bigram]")
        return

    model_type = sys.argv[1].lower()

    if model_type not in ['unigram', 'bigram']:
        print("model type error")
        return

    path1 = "/home/nst/yq236/tools/kaldi-trunk-git/egs/swbd/s5c/data/train/text"
    path2= "/home/alta/BLTSpeaking/ged-pm574/artificial-error/lib/cts-work/cts7-2"
    cts2gedtsv(path1, path2, model_type)


if __name__ == "__main__":
    main()
