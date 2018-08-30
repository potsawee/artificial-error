"""
he'd he had         => "he'd": ['he', 'had'],
how'd how had       => "how'd": ['how', 'had'],
"""

def convert():
    # path1 = "map_all.txt"
    path1 = "/home/alta/CLC/LNRC/lib/corrs/map_clc.txt"
    path2 = "map_all_pydict2.txt"
    with open(path1) as file:
        lines = file.readlines()
    with open(path2, 'w') as file:
        for line in lines:
            if line == '\n':
                continue
            try:
                items = line.split(' ')
                file.write("\"{}\": ['{}', '{}'],\n".format(items[0], items[1], items[2].strip()))
            except:
                print(line, end="")
if __name__ == "__main__":
    convert()
