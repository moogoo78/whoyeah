#!/usr/bin/env python
# -.- coding: utf-8 -.-
# 
#

# for file open
from __future__ import with_statement # This isn't required in Python 2.6
import sys, os, string, re
if os.name == "nt":
    from ctypes import *
    windll.Kernel32.GetStdHandle.restype = c_ulong
    std_out_handle = windll.Kernel32.GetStdHandle(c_ulong(0xfffffff5))

### config ###
# set exclude files and dirs
IGNORE_FILES = ['TAGS', 'tags']
IGNORE_DIRS = ['.git', '.svn']

TEXTCHARS = ''.join(map(chr, [7,8,9,10,12,13,27] + range(0x20, 0x100)))
ALLBYTES = ''.join(map(chr, range(256)))

# main 
def main(str_pattern, target_dir):
    num_files = 0
    num_match_files = 0
    num_matches = 0
    file_list = []

    if options.quiet_dir:
        IGNORE_DIRS.extend(options.quiet_dir.split(' '))

    # find .wyignore file
    if os.path.isfile(".wyignore"):
        with open(".wyignore") as fopen:
            for ignore_dir in fopen:
                d = ignore_dir.strip(' \t\n\r')
                IGNORE_DIRS.append(d)

    print 'wy search, ignoring... ' +  "[" + ", ".join(IGNORE_DIRS) + "]"

    for path, dirs, files in os.walk(target_dir, topdown=True):
        for f in files:
            found = 0
            ignore = False
            # if path have ignore directorys, skip to next
            for dirt in IGNORE_DIRS:
                if path.find(dirt) > 0: 
                    ignore = True
                    break
            if not ignore and os.path.isfile(os.path.join(path, f)):
                found = find_in_file(f, path, str_pattern)
                if found > 0 :
                    num_match_files += 1
                    file_list.append(os.path.join(path, f))
                num_files += 1
                num_matches += found

    print 'Summary:'
    print '--------'
    num_replace = 0
    for fn in file_list:
        print fn
        # replace string!!
        if options.str_replace:
            num_replace += 1
            s = open(fn).read()
            s = s.replace(str_pattern, options.str_replace)
            fw = open(fn, 'w')
            fw.write(s)
            fw.close()
    print '--------'
    print '  match', set_color(num_matches, 94), 'times, in', set_color(num_match_files, 94), 'files.'
    print '  total find', set_color(num_files, 94), 'files'
    if num_replace > 0:
        print '<<< string replaced by: ' + options.str_replace + '!!! >>>'

def find_in_file(f, path, str_pattern):
    full_path = os.path.join(path, f)
    re_flag = False
    found = 0
    ln = 0 # line number
                
    with open(full_path) as fopen:
        if is_binary(full_path) != 1 and f not in IGNORE_FILES:
            found = 0
            # find in each line
            for line in fopen:
                match = []
                ln += 1
                if options.ignore_case:
                    re_flag = re.IGNORECASE
                for m in re.finditer(str_pattern, str(line), re_flag):
                    match.append(m.group(0))
                if len(match) > 0:
                    if found == 0:
                        print set_color(full_path, 91)
                    for keyword in match:
                        line = replace_by_color(line, keyword, 95)
                        found += 1
                    print set_color(ln, 93) + ': ' + line[:-1]

        return found


def replace_by_color(string, keyword, color_code):
#    if os.name == "nt":
#        windll.Kernel32.SetConsoleTextAttribute(std_out_handle, 14)
#        print (str(keyword))
#        windll.Kernel32.SetConsoleTextAttribute(std_out_handle, 7)
#    else: 
        return string.replace(str(keyword), set_color(str(keyword),95) )

def set_color(keyword, color_code):
    if os.getenv('TERM',None) in ['rxvt','xterm']:
        #return keyword.replace(str(keyword), '\033[0;'+str(color_code)+'m'+str(keyword)+'\033[m')
        return '\033[0;' + str(color_code) + 'm' + str(keyword) + '\033[m'
#    elif os.name == "nt":
#        windll.Kernel32.SetConsoleTextAttribute(std_out_handle, 10)
#        print str(keyword)
#        windll.Kernel32.SetConsoleTextAttribute(std_out_handle, 7) # 7 is light grey, 15 is white
    else:
        return str(keyword)

def is_binary(filename):
    fopen = open(filename, 'rb')
    is_binary = _is_binary_file(fopen)
    fopen.close()
    return is_binary


def _is_binary_file(fopen):
    bytes = fopen.read(1024)
    return is_binary_string(bytes)


def is_binary_string(bytes):
    nontext = bytes.translate(ALLBYTES, TEXTCHARS)
    return bool(nontext)


if __name__ == '__main__':
    # parse options
    from optparse import OptionParser
    usage = "usage: %prog [options] PATTERN"
    parser = OptionParser(usage=usage)
    parser.add_option('-i', '--ignore_case',
                      action='store_true', dest='ignore_case', default=False,
                      help='ignore case sensitive')
    parser.add_option('-t', '--target', dest='target_dir', default='.',
                      help='set search target', metavar='TARGET')
    parser.add_option("-q", '--quiet', dest='quiet_dir', default='',
                      help='ignore file or directory to be search',
                      metavar='BIGFILE')
    parser.add_option('-s', '--replace', dest='str_replace', help='replace by new string', metavar='NEW_STRING')

    (options, args) = parser.parse_args()

    if not args:
        parser.print_help()
    else:
        str_pattern = args[0]
        main(str_pattern, options.target_dir)
