# coding: utf-8

from operator import itemgetter, attrgetter
import sys, os
import re

def save_frequency_list(res, filename):
    f = open(filename, "w+")
    try:
        for l in res:
            f.write("%s" %l[0])
            f.write(",%s" %l[1])
            f.write(",%s\n" %l[2])
    finally:
        f.close()
    return

def get_frequency_list(filename):
    res = []
    f = open(filename)
    for line in f.readlines():
        sep = re.compile(",")
        parts = re.split(sep, line.rstrip())
        res.append( [parts[0], parts[1], int(parts[2])] )
    return res

def main():
    for stroke in range(1, 65):
        #stroke = 5
        input_filename = os.path.join("./freq/", "%s.txt" %(stroke))
        output_filename = os.path.join("./freq/", "%s.txt" %(stroke))
        res = get_frequency_list(input_filename)
        res_sorted = sorted(res, key=itemgetter(2), reverse=True)
        #print res_sorted
        save_frequency_list(res_sorted, output_filename)

if __name__ == '__main__':
    main()
