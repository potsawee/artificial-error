import sys
from unigram import UnigramModel
from data_processing import *

# CTS = Conversational Telephone Speech
# There are about 3 million words

def cts2gedtsv(ami, gedtsv):
    """
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
                1. US spelling => UK spelling
                2. Tokenisation e.g. don't => do n't // it's => it 's
    ged.tsv:  corrput the corpus using statistics from the model
    """

    myoutput = [gedtsv+'.work12.ged.tsv',
                gedtsv+'.work3.ged.tsv', gedtsv+'.ged.tsv']

    # ------------ Work 12 ------------ #
    with open(ami, 'r') as file:
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
            file.write(".\n\n")
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
            word = us_to_uk_spelling(word)

            # tokenisation
            if "'" in word:
                words = split_word(word)
                for word in words:
                    file.write("{}\n".format(word))
                continue

            file.write("{}\n".format(word))

    print("{} done".format(myoutput[1]))
    # -------------------------------- #

    # ----------- ged.tsv ------------ #

    with open(myoutput[1], 'r') as file:
        lines = file.readlines()

    gedx_path = "/home/alta/BLTSpeaking/ged-pm574/artificial-error/lib/gedx-tsv/work-14082018/master.gedx.ins.tsv"
    print("Loading... {}".format(gedx_path))
    model = UnigramModel()
    model.readin(gedx_path)
    model.construct_model()
    print("Model built!")

    sentences = []
    sentence = [] # start with a word, end with a full stop
                  # [('the', 'c'), ('cat', 'c'), ...]

    deletion = "<DEL>"
    sub_count = 0
    ins_count = 0
    del_count = 0
    good_count = 0

    print("len(lines) =", len(lines))
    print("{}|100%".format(' '*int(len(lines)/50000)))

    for j, line in enumerate(lines):

        # counting
        if j % 50000 == 0:
            print('#', end='')
            sys.stdout.flush()

        if line == '\n':
            sentences.append(sentence)
            sentence = []
            continue

        token = line.strip()
        emitted = model.emit(token)

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


    print("\n")
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
                    idx += 1
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
    path1 = "/home/nst/yq236/tools/kaldi-trunk-git/egs/swbd/s5c/data/train/text"
    path2= "/home/alta/BLTSpeaking/ged-pm574/artificial-error/lib/cts-work/cts1-log"
    cts2gedtsv(path1,path2)


if __name__ == "__main__":
    if(len(sys.argv) == 1):
        main()
