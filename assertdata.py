import sys

def main():
    # path = '/home/alta/BLTSpeaking/ged-pm574/artificial-error/lib/tsv/ami1.train.ged.tsv'
    if len(sys.argv) > 1:
        path = sys.argv[1]
    zero = 0
    one = 0
    two = 0
    three = 0
    four = 0
    fivemore = 0
    with open(path) as file:
        for line in file:
            n = len(line.split())
            if n == 0:
                zero += 1
            elif n == 1:
                one += 1
            elif n == 2:
                two += 1
            elif n == 3:
                three += 1
            elif n == 4:
                four += 1
            else:
                fivemore += 1
    print("zero: ", zero)
    print("one: ", one)
    print("two: ", two)
    print("three: ", three)
    print("four: ", four)
    print("five+: ", fivemore)


if __name__ == "__main__":
    main()
