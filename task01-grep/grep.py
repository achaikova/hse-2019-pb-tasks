#!/usr/bin/env python3
from typing import List, IO
from pathlib import Path
import sys
import re
import argparse


def print_out_result(result: List[str]):
    for x in result:
        print(x)


def grep_input(filename: IO[str], pattern: str, is_amount: bool) -> List[str]:
    result = []
    for line in filename:
        line = line.rstrip('\n')
        if re.search(pattern, line):
            result.append(line)
    if is_amount:
        return [str(len(result))]
    return result


def grep_files(paths: List[str], pattern: str, is_amount: bool):
    number_of_files = len(paths)
    if number_of_files == 0:
        result = grep_input(sys.stdin, pattern, is_amount)
        print_out_result(result)
    else:
        for path in paths:
            p = Path(path)
            if p.is_dir():
                print(f'Is a directory: {path}')
            elif p.is_file():
                with open(path, 'r') as file:
                    result = grep_input(file, pattern, is_amount)
                    if number_of_files > 1:
                        result = [f'{path}:' + str(x) for x in result]
                    print_out_result(result)
            else:
                print(f'File not found')


def main(args_str: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('pattern', type=str, help='a pattern to search for')
    parser.add_argument('files', metavar='FILES', nargs='*',
                        help='the files(s) to search')
    parser.add_argument('-c', '--is_amount', action='store_true',
                        help='print out the amount of found lines')
    parser.add_argument('-E', '--is_regex', action='store_true',
                        help='search for a regular expression')
    args = parser.parse_args(args_str)
    pattern = args.pattern if args.is_regex else re.escape(args.pattern)
    grep_files(args.files, pattern, args.is_amount)


if __name__ == '__main__':
    main(sys.argv[1:])
