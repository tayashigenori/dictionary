# coding: utf-8

import sys
import re
import json

def main():
    s = '{"kSemanticVariant": "U+5F0C &#x5F0C;U+58F9 &#x58F9;", "kSpecializedSemanticVariant": "U+58F9 &#x58F9;"}'
    for data_type,value in json.loads(s).items():
        sys.stderr.write("####data_type: %s, value: %s\n" %(data_type, value))
        #codepoint = value.split(";")[0]
        for v in value.split(";"):
            if not v.strip():
                continue
            sys.stderr.write("####v: %s\n" %v)
            pat = re.compile("\s+")
            codepoint = re.split(pat, v)[0]
            sys.stderr.write("####codepoint: %s\n" %codepoint)
            hex_value = codepoint[2:6]
            sys.stderr.write("####hex_value: %s\n" %hex_value)
            print unichr(int(hex_value, 16)).encode('shift-jis')

if __name__ == '__main__':
    main()
