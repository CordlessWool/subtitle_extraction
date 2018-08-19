#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import sys

src = sys.argv[1]
dest = sys.argv[2]

print(src)
print(dest)

replace = ["_", "-", " "]

regex_files = r'[\w\W. -]*(mkv|mp4){1}$'
matches = 0

exclude = ["kung_fu_killer_2_(2008).mkv", "kung_fu_killer_(2008).mkv"]

def extract_subs(srcname, destname, dest):
    global matches

    matches+=1
    print(srcname)
    print(dest)
    print(destname)
    os.system('./extract_sub.sh "{0}" "{1}" "{2}"'.format(srcname, destname, dest))

def deep_compare(first, second):

    quantity_of_signs = 3
    f_len = len(first)
    s_len = len(second)

    if f_len < quantity_of_signs or s_len < quantity_of_signs:
        return 0

    min_len = (f_len > s_len) and s_len or f_len
    max_len = (f_len < s_len) and s_len or f_len

    x = 0
    while x < min_len and first[x] == second[x]:
        x+=1

    same = x
    pos = x
    x = -1

    while x == -1 and pos < min_len - quantity_of_signs:
        f_x = first.find(second[pos:pos + quantity_of_signs], same)
        s_x = second.find(first[pos:pos + quantity_of_signs], same)

        pos += quantity_of_signs

        x = (f_x < s_x) and f_x or s_x  #get smaller value

    if pos >= min_len - quantity_of_signs:
        return same/max_len

    match = deep_compare(first[pos::], second[pos::])
    match = same/pos + match

    return match



def compare_names(first, second, min_match):

    global replace
    global exclude
    regex = r'^([\w\+\'"#&.,-]*)[\(]?([0-9]{4})?[\)]?_?d?i?s?c?[0-9]?[.][\w. -]*(mkv|mp4){1}$'


    fir = ''.join(first)
    sec = (second + ".")[:-1]

    for sign in replace:
        fir = fir.replace(sign, "")
        sec = sec.replace(sign, "")

    fir_obj = re.match(regex, fir, re.IGNORECASE | re.UNICODE)
    sec_obj = re.match(regex, sec, re.IGNORECASE | re.UNICODE)

    if fir_obj is None or sec_obj is None or len(fir_obj.groups()) < 2 or len(sec_obj.groups()) < 2:
       # print("failed: " + first + " " + second)
        return

    fir_name = fir_obj.group(1).lower()
    sec_name = sec_obj.group(1).lower()

    if len(fir_name) == 0 or len(sec_name) == 0:
        return

    fir_year = fir_obj.group(2)
    sec_year = sec_obj.group(2)

    #fir_ext = fir_obj.group(3)
    #fir_ext = sec_obj.group(3)

    if fir_name == sec_name:
        if fir_year and sec_year:
            if fir_year == sec_year:
                return True
        else:
            return True
    elif first not in exclude and second not in exclude:
        match = deep_compare(fir_name, sec_name)
        if match >= min_match and fir_year == sec_year:
            print("Matching: " + first + " " + second)
            print("success")
            return True

    return False


for (src_dirpath, src_dirname, src_filenames) in os.walk(src):
    for src_filename in src_filenames:
        match = re.match(regex_files, src_filename)
        if match:
            for(dest_dirpath, dest_dirname, dest_filenames) in os.walk(dest):
                for dest_filename in dest_filenames:
                    match = re.match(regex_files, dest_filename)
                    if match and compare_names(src_filename, dest_filename, 0.7):
                        extract_subs(src_dirpath+src_filename, dest_filename, dest_dirpath)


print(matches)