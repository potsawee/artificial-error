#!/usr/bin/python3
'''
Print the substitution, insertion, deletion statistics
of a gedx file
'''

import sys

def gedx_info(path):
    good_count = 0
    sub_count = 0
    ins_count = 0
    del_count = 0
    with open(path, 'r') as file:
        for line in file:
            if line == '\n':
                continue

            items = line.split()
            orig = items[0]
            emit = items[1]

            if orig == emit:
                good_count += 1
            elif '*' in orig:
                ins_count += 1
            elif '*' in emit:
                del_count += 1
            else: # orig != emit and not '*'
                if emit == '<unk>':
                    good_count += 1
                else:
                    sub_count += 1

    print("------ gedx info ------")
    print("num_words = {}".format(good_count+sub_count+ins_count+del_count))
    print("%error = {:.2f}".format((sub_count+ins_count+del_count)/good_count*100))
    print("%sub = {:.2f}".format(sub_count/good_count*100))
    print("%ins = {:.2f}".format(ins_count/good_count*100))
    print("%del = {:.2f}".format(del_count/good_count*100))

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 gedx-info.py gedx_path")
        return

    gedx_path = sys.argv[1]
    gedx_info(gedx_path)

if __name__ == '__main__':
    main()
