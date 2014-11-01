# coding: utf-8

ENCODING="shift-jis"

import sys, os
import re
import json

class JsonParser:
    def __init(self,):
        return
    """
    get value by key
    """
    def get_value_from_json(self, j, key):
        d = self.get_all_from_json(j)
        return d.get(key, default=None)
    def get_value_from_line(self, line, key):
        for codepoint,d in self.get_dict_from_line(line).items():
            res = d.get(key)
        return res
    def get_value_from_file(self, filename, key):
        res = {}
        for codepoint, d in self.get_all_from_file(filename).items():
            try:
                # note: duplicate codepoint will be overridden
                res.update( {codepoint: d[key]} )
            except KeyError:
                pass
        return res
    def get_value_from_dir(self, dirname, key):
        res = {}
        for codepoint, d in self.get_all_from_dir(dirname).items():
            try:
                # note: duplicate codepoint will be overridden
                res.update( {codepoint: d[key]} )
            except KeyError:
                pass
        return res
    """
    print value by key
    """
    def print_value_from_json(self, j, key):
        self.print_value(self.get_value_from_json(j, key))
    def print_value_from_line(self, line, key):
        self.print_value(self.get_value_from_line(line, key))
    def print_value_from_file(self, filename, key):
        for codepoint, v in self.get_value_from_file(filename, key).items():
            sys.stdout.write("codepoint: %s\n" %codepoint)
            self.print_value(v)
    def print_value_from_dir(self, dirname, key):
        for codepoint, v in self.get_value_from_dir(dirname, key).items():
            sys.stdout.write("codepoint: %s\n" %codepoint)
            self.print_value(v)

    """
    get all
    """
    def get_all_from_json(self, j):
        #sys.stderr.write("### j: %s\n" %j)
        return json.loads(j)
    def get_dict_from_line(self, line):
        #sys.stderr.write("### line: %s\n" %line)
        pat = re.compile(",(?={)")
        (codepoint, j) = re.split(pat, line)
        return {codepoint:
                self.get_all_from_json(j)}
    def get_all_from_file(self, filename):
        res = {}
        f = open(filename)
        try:
            for l in f.readlines():
                # note: duplicate codepoint will be overridden
                res.update( self.get_dict_from_line(l) )
        finally:
            f.close()
        return res
    def get_all_from_dir(self, dirname):
        res = {}
        for f in os.listdir(dirname):
            full_path = os.path.join(dirname, f)
            # note: duplicate codepoint will be overridden
            res.update( self.get_all_from_file(full_path) )
        return res
    """
    print all
    """
    def print_all_from_json(self, j):
        d = self.get_all_from_json(j)
        self.print_all(d)
        return
    def print_all_from_line(self, line):
        for codepoint, j in self.get_dict_from_line(line).items():
            self.print_all_from_json(j)
        return
    def print_all_from_file(self, filename):
        for codepoint, d in self.get_all_from_file(filename).items():
            sys.stdout.write("codepoint: %s\n" %codepoint)
            self.print_all(d)
        return
    def print_all_from_dir(self, dirname):
        for codepoint, d in self.get_all_from_dir(dirname).items():
            sys.stdout.write("codepoint: %s\n" %codepoint)
            self.print_all(d)
        return
    def print_all(self, d):
        for data_type,value in d.items():
            sys.stderr.write("## data_type: %s, value: %s\n" %(data_type, value))
            self.print_value(value)
    def print_value(self, value):
        for v in value.split(";"):
            if not v.strip():
                continue
            #sys.stderr.write("#### v: %s\n" %v)

            vs = re.split(re.compile("\s+"), v)
            sys.stdout.write("#### values: %s\n" %",".join(vs))

            #hex_value = codepoint.replace("U+", "")
            #sys.stdout.write("#### hex_value: %s\n" %hex_value)

            #sys.stdout.write( unichr(int(hex_value, 16)).encode(ENCODING) )

def main():
    jp = JsonParser()
    #d = "./dict/"
    #jp.print_all_from_dir(d)
    f = "./dict/5.txt"
    #jp.print_all_from_file(f)
    jp.print_value_from_file(f, "kHanyuPinlu")

if __name__ == '__main__':
    main()
