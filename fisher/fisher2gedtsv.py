import sys
from sequencemodel import UnigramModel
from data_processing import *
from tqdm import tqdm

def fisher2gedtsv(fisher, gedtsv):
    """

    This script is for processing the 'Fisher' CTS corpus.

    original: the Fisher corpus e.g. /home/alta/CTS/Fisher/transcripts
    converted: /home/alta/BLTSpeaking/ged-pm574/artificial-error/lib/fisher/work15082018/fisher-all.txt

    fsh_60059 this is george doddington
    fsh_60059 my name is katie
    fsh_60059 hi katie
    fsh_60059 okay

    work12:    transcription + text processing
                1. one word per line format
                2. remove special tokens - () {} []
                3. split multiple words
                4. parital word e.g. spee-
                5. keep mispronunciation
    work3:    more complicated text processing
                ### 1. US spelling => UK spelling !!! DTAL has both spelling
                2. Tokenisation e.g. don't => do n't // it's => it 's
    ged.tsv:  corrput the corpus using statistics from the model
    """

    myoutput = [gedtsv+'.work12.ged.tsv',
                gedtsv+'.work3.ged.tsv', gedtsv+'.ged.tsv']

    # ------------ Work 12 ------------ #
    with open(fisher, 'r') as file:
        lines = file.readlines()
    with open(myoutput[0], 'w') as file:

        print("processing {}".format(myoutput[0]))

        for idx in tqdm(range(len(lines))):
            line = lines[idx]

            items = line.split()
            for token in items[1:]:

                if '?' in token:
                    token = token.replace('?','')
                token = token.strip(',')

                if '(' in token or ')' in token:
                    if token == "((" or token == "))":
                        continue
                    elif "((" in token:
                        token = token.replace("((","")
                        token = token.strip()
                    elif "))" in token:
                        token = token.replace("))","")
                        token = token.strip()


                if '{' in token or '}' in token or '[' in token or ']' in token:
                    continue


                if token[0] == '-':
                    token = keep_pw_fisher(token)
                    if token == "<partial>":
                        continue
                if token[-1] == '-':
                    continue


                if '-' in token: #multiple-words
                    for word in token.split('-'):
                        if not is_hesitation(word):
                            file.write("{}\n".format(word.lower()))

                else:
                    if not is_hesitation(token):
                        file.write("{}\n".format(token.lower()))
                    else:
                        pass
            file.write("\n")
    print("\n{} done".format(myoutput[0]))
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
            # word = us_to_uk_spelling(word)

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

    print("Propagating the errors...")
    for idx in tqdm(range(len(lines))):
        line = lines[idx]

        if line == '\n':
            sentences.append(sentence)
            sentence = []
            continue

        token = line.strip()

        # No error boosting
        emitted = model.emit(token)
        # With error boosting
        # emitted = model.emit(token, gain=1.2)

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
    path1 = "/home/alta/BLTSpeaking/ged-pm574/artificial-error/lib/fisher/work15082018/fisher-all.txt"
    path2 = "/home/alta/BLTSpeaking/ged-pm574/artificial-error/lib/fisher/fisher6"
    fisher2gedtsv(path1,path2)


if __name__ == "__main__":
    if(len(sys.argv) == 1):
        main()
