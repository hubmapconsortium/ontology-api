#!/usr/bin/env python

import argparse, os, re, unicodedata, itertools, sys, string


class RawTextArgumentDefaultsHelpFormatter(
    argparse.ArgumentDefaultsHelpFormatter,
    argparse.RawTextHelpFormatter
):
    pass


# https://docs.python.org/3/howto/argparse.html
parser = argparse.ArgumentParser(
    description='Post process tsv files produced py PheKnowLator',
    formatter_class=RawTextArgumentDefaultsHelpFormatter)
parser.add_argument('filename', type=str,
                    help='file to fix')
parser.add_argument("-c", "--check", action="store_true",
                    help='check that all records have the same number of fields')
parser.add_argument("-f", "--fix", type=str,
                    help='for records with fewer fields, append lines till the field count is correct')
args = parser.parse_args()


def print_string_as_chars(s: str) -> None:
    print(s)
    lst = [ord(c) for c in s]
    print(lst)


def count_of_char_in_str(ch: int, s: str) -> int:
    lst = [ord(c) for c in s]
    return lst.count(ch)


def check(ifilename: str) -> None:
    file_r = open(ifilename, 'r')

    # Process the header to determine the number of fields in a record...
    line = file_r.readline()
    tabs_in_record = line.count('\t')
    print(f"Fields in record: {tabs_in_record}")

    line_no = 1
    bad_no = 0
    eof = False
    while not eof:
        line_no += 1
        line = file_r.readline()
        # print_string_as_chars(line)

        # if line is empty end of file is reached
        if not line:
            break
        tabs_in_line = line.count('\t')
        # print(f"tabs_in_line: {tabs_in_line}; tabs_in_record: {tabs_in_record}")

        while not eof and tabs_in_line < tabs_in_record:
            print(f"< Line number {line_no} has {tabs_in_line} fields but wanted {tabs_in_record}, last character {ord(line[-1])}")
            bad_no += 1
            line_no += 1
            next_line = file_r.readline()
            if not next_line:
                eof = True
                break
            line = line + ' ' + next_line
            tabs_in_line = line.count('\t')
        if tabs_in_line > tabs_in_record:
            print(f"> Line number {line_no} has {tabs_in_line} fields but wanted {tabs_in_record}, last character {ord(line[-1])}")
            bad_no += 1

    print(f"Lines in file: {line_no}, bad records: {bad_no}")
    file_r.close()


def fix_records_to_have_same_number_of_fields(ifilename: str, ofilename: str) -> None:
    file_w = open(ofilename, 'w')
    file_r = open(ifilename, 'r')

    # Process the header to determine the number of fields in a record...
    line = file_r.readline()
    tabs_in_record = line.count('\t')
    print(f"Fields in record: {tabs_in_record}")
    file_w.write(line)

    appended = 0
    line_no = 1
    eof = False
    while not eof:
        line_no += 1
        line = file_r.readline()

        # if line is empty end of file is reached
        if not line:
            break
        tabs_in_line = line.count('\t')

        while not eof and tabs_in_line < tabs_in_record:
            print(f"< Line number {line_no} has {tabs_in_line} fields but wanted {tabs_in_record}, last character {ord(line[-1])}")
            # This should be a new line character, so remove it
            line = line[:-1]
            line_no += 1
            next_line = file_r.readline()
            if not next_line:
                eof = True
                break
            appended += 1
            line = line + ' ' + next_line
            tabs_in_line = line.count('\t')
        if tabs_in_line > tabs_in_record:
            print(f"> Line number {line_no} has {tabs_in_line} fields but wanted {tabs_in_record}, last character {ord(line[-1])}")

        file_w.write(line)

    print(f"Lines in file: {line_no}, lines appended: {appended}")
    file_w.close()
    file_r.close()


print(f"Processing input file {args.filename}")

if args.fix is not None:
    print("Fixing file...")
    fix_records_to_have_same_number_of_fields(args.filename, args.fix)
if args.check is True:
    print("Checking file...")
    check(args.filename)

print('Done!')
