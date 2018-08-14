"""
Convert pra to gedx
"""
import string
import sys
import pdb

punctuation = string.punctuation.replace('*','') # !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~

def convert(pra, gedx):
    with open(pra, 'r') as file:
        lines = file.readlines()
    with open(gedx, 'w') as file:
        c_count = 0
        i_count = 0
        for line in lines:
            if line == '\n':
                continue
            items = line.split()
            if items[0] == 'REF:':
                ref = items[1:]
                continue
            elif items[0] == 'HYP:':
                hyp = items[1:]
            else:
                continue

            # Debug the stats
            if (len(ref) != len(hyp)):
                # If an error (e.g. misalignment occurs)
                # The user can fix it this way
                # or remove this and simply ignore those sentences with errors
                print(pra)
                print(len(ref), len(hyp))
                print(ref)
                print(hyp)
                # debug
                # pdb.set_trace()

                # ignore
                continue


            # pdb.set_trace()
            for w_r, w_h in zip(ref, hyp):
                # if len(w_r) != 1:
                w_r = w_r.lower().strip(punctuation)
                # if len(w_h) != 1:
                w_h = w_h.lower().strip(punctuation)
                if w_r != '' and w_h != '':
                    if(w_r == w_h):
                        file.write("{}\t{}\tc\n".format(w_r, w_h))
                        c_count += 1
                    else:
                        file.write("{}\t{}\ti\n".format(w_r, w_h))
                        i_count += 1
            file.write('\n')

        total_count = c_count + i_count
        print("count = {}".format(total_count))
        print("c_count = {:8} ({:.1f}%)".format(c_count, c_count/total_count*100))
        print("i_count = {:8} ({:.1f}%)".format(i_count, i_count/total_count*100))

def main():
    # pra = '/home/alta/BLTSpeaking/ged-pm574/artificial-error/work/IELTS/2000_44/align/file.spell.ctm.pra'
    # gedx = '/home/alta/BLTSpeaking/ged-pm574/artificial-error/work/IELTS/2000_44/align/file.gedx'
    # pra = '/home/alta/BLTSpeaking/ged-pm574/artificial-error/work/CPE/1993_01/align/file.spell.ctm.pra'
    # gedx = '/home/alta/BLTSpeaking/ged-pm574/artificial-error/work/CPE/1993_01/align/file.gedx'
    if(len(sys.argv) != 3):
        print("Usage python3 pra2gedx.py pra gedx")
        return
    pra = sys.argv[1]
    gedx = sys.argv[2]
    convert(pra, gedx)

if __name__ == "__main__":
    main()
