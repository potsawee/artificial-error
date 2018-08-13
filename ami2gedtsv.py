import sys
from unigram import UnigramModel
from data_processing import *
from string import punctuation
mypunc = punctuation.replace('.','').replace("'",'')


model = UnigramModel()
model.readin("/home/alta/BLTSpeaking/ged-pm574/artificial-error/lib/gedx-tsv/BULATS.gedx.ins.tsv")
model.construct_model()


def ami2gedtsv(ami, gedtsv):
    """
    original: the AMI corpus e.g. /home/dawna/meetings/ami/convert/lib/mlfs/train+sil.mlf
    work1:    transcription => tsv format & hesitation => <hesitation>
    work2:    text processing
                1. mispronunciation
                2. short form e.g. 'kay => okay
                3. multiple word e.g. one-handed => one handed
                4. parital word e.g. spee-
                5. just \
                6. remove special tokens
    work3:    more complicated text processing
                1. US spelling => UK spelling
                2. Tokenisation e.g. don't => do n't // it's => it 's
    ged.tsv:  corrput the corpus using statistics from the model
    """

    myoutput = [gedtsv+'.work1.ged.tsv', gedtsv+'.work2.ged.tsv',
                gedtsv+'.work3.ged.tsv', gedtsv+'.ged.tsv']

    # ------------ Work 1 ------------ #
    with open(ami, 'r') as file:
        lines = file.readlines()
    with open(myoutput[0], 'w') as file:
        for line in lines[1:]:
            if line[:3] == '"*/':
                continue
            if line == '.\n':
                file.write('.\n\n')
                continue

            token = line.strip()
            if is_hesitation(token):
                print(token, '=>', '<hesitation>')
                file.write("<hesitation>\n")
                continue

            file.write(line.lower())
    print("{} done".format(myoutput[0]))
    # -------------------------------- #

    # ------------ Work 2 ------------ #
    with open(myoutput[0], 'r') as file:
        lines = file.readlines()

    with open(myoutput[1], 'w') as file:
        for line in lines:

            # Empty lines
            if line == '\n':
                file.write(line)
                continue

            word = line.strip()

            # Mispronunciation => Not a partial word
            if '_mispron' in word:
                word = word.replace('_mispron','')

            # Short form (\' ...) token e.g. \'kay
            if "\\'" in word:
                print("convert sf {} => {}".format(word,convert_short_form(word)))
                word = convert_short_form(word)

            # Partial word
            if word[-1] == '-':
                continue

            # Multiple words
            if '-' in word:
                if(len(word.split('-'))>1):
                    for w in word.split('-'):
                        file.write("{}\n".format(w))
                    continue

            # just \
            if word == "\\":
                continue

            # <hesitation>, <disfluency>, etc...
            if is_special_token(word):
                continue

            file.write("{}\n".format(word))

    print("{} done".format(myoutput[1]))
    # -------------------------------- #
    # ------------ Work 3 ------------ #
    with open(myoutput[1], 'r') as file:
        lines = file.readlines()

    with open(myoutput[2], 'w') as file:
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

    # -------------------------------- #
    return
    # ----------- ged.tsv ------------ #
    #
    # with open(myoutput[2], 'r') as file:
    #     lines = file.readlines()
    #
    # err_count = 0
    # good_count = 0
    # insertion_count = 0
    # deletion_count = 0
    #
    # with open(myoutput[2], 'w') as file:
    #     is_deletion = False
    #     for line in lines:
    #
    #         if line == '\n':
    #             continue
    #
    #         token = line.strip()
    #
    #         emitted = model.emit(token)
    #
    #         # insertion
    #         if(len(emitted.split()) >= 2):
    #             is_deletion = False
    #             x = emitted.split()
    #             if(x[0] == token):
    #                 file.write("{}\tc\n{}\ti\n".format(x[0],x[1]))
    #             else:
    #                 file.write("{}\ti\n{}\tc\n".format(x[0],x[1]))
    #
    #             insertion_count += 1
    #             # continue
    #
    #         # deletion
    #         elif '*' in emitted:
    #             is_deletion = True
    #             # continue
    #             deletion_count += 1
    #
    #         # Ok or Substitution
    #         else:
    #             if token != emitted or is_deletion == True:
    #                 file.write("{}\ti\n".format(emitted))
    #                 err_count += 1
    #             else:
    #                 file.write("{}\tc\n".format(token))
    #                 good_count +=1
    #             is_deletion = False
    #
    # print("err_count:", err_count)
    # print("good_count:", good_count)



def main():
    path1 = "/home/alta/BLTSpeaking/ged-pm574/artificial-error/lib/ami-train+sil.mlf"
    path2= "/home/alta/BLTSpeaking/ged-pm574/artificial-error/lib/ami-monday"
    ami2gedtsv(path1,path2)

def test1():
    """
    Found:
    <other> <hesitation> <disfluency> <laugh>
    <gap> <cough> <vocal> <sigh> <singing> <sound> <noise>
    """
    path= "/home/alta/BLTSpeaking/ged-pm574/artificial-error/lib/ami.ged"
    with open(path, 'r') as f:
        mylist = []
        for line in f:
            if '<' in line or '>' in line:
                if line.strip() not in mylist:
                    mylist.append(line.strip())
    for line in mylist:
        print(line)

def test2():
    path= "/home/alta/BLTSpeaking/ged-pm574/artificial-error/lib/ami.2.ged.tsv"
    mylist = []
    with open(path, 'r') as file:
        for line in file:
            for c in line.strip():
                if c in mypunc:
                    if line.strip() not in mylist:
                        mylist.append(line.strip())
    for item in mylist:
        print(item)
if __name__ == "__main__":
    if(len(sys.argv) == 1):
        main()
    else:
        # test1()
        test2()
