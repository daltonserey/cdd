#!/usr/bin/env python
# coding: utf-8
# (c) 2011-2014 Dalton Serey, UFCG

from __future__ import print_function
from __future__ import unicode_literals

import sys
import os
import datetime

from jsonfile import *
from directories import *

config = JsonFile(os.path.expanduser('~/.cdd/config.json'))
directories = Directories(config['directories'])

LRED = '\033[1;31m'
LGREEN = '\033[1;32m'
GREEN="\033[9;32m"
WHITE="\033[1;37m"
LCYAN = '\033[1;36m'
RESET = '\033[0m'

DEBUG = False

def cprint(color, msg, file=sys.stdout):
    print(color + msg + RESET, file=file)


def add_directory(directory, directories):
    if directory in directories:
        if DEBUG:
            cprint(LCYAN, "%s (already in database)" % directory, file=sys.stderr)
        return

    directories.add(directory)
    cprint(LCYAN, "%s (+)" % directory, file=sys.stderr)
    print("type cd -d to remove", file=sys.stderr)


def delete_directory(directory, directories):
    dir2remove = os.path.basename(sys.argv[2]) if len(sys.argv) < 2 else directory
    directories.remove(dir2remove)
    print(os.getcwd())


def format_report(pattern, match, alternatives):
    i_match = next(i for i in xrange(len(alternatives)) if alternatives[i] == match)
    match = match.replace("/Users/dalton", "~")
    for i in xrange(len(alternatives)):
        alternatives[i] = alternatives[i].replace("/Users/dalton", "~")
        basename = os.path.basename(alternatives[i])
        if alternatives[i] == match:
            color_basename = basename.replace(pattern, LCYAN + pattern + WHITE)
            alternatives[i] = WHITE + alternatives[i].replace(basename, color_basename) + RESET
        #else:
        #    color_basename = basename.replace(pattern, WHITE + pattern + RESET)
        #    alternatives[i] = alternatives[i].replace(basename, color_basename)

    return "\n".join(alternatives)


def matching_from(pattern, directories, from_dir):
    def is_match(pattern, directory):
        return pattern.lower() in directory.lower()

    alternatives = [d[0] for d in directories if is_match(pattern, os.path.basename(d[0]))]
    if not alternatives:
        return [None, []]

    if from_dir not in alternatives:
        select = alternatives[0]

    else: # from_dir in alternatives:
        index = alternatives.index(from_dir)
        alternatives[index]
        select = alternatives[(index + 1) % len(alternatives)]

    return [select, alternatives]


def print_matches(pattern, directories, from_dir):
    match, alternatives = matching_from(pattern, directories.data, from_dir)
    if match is None:
       print(pattern)
       return

    # print match
    print(match)

    # print report with alternatives
    output = format_report(pattern, match, alternatives)
    print(output, file=sys.stderr)

    # register pending update
    config['pending_update'] = {
        "timestamp": (datetime.datetime.now() - datetime.datetime(1970,1,1)).total_seconds(),
        "match": match,
        "from_dir": from_dir
    }


def resolve_pending_update(directories):
    def to_timestamp(dt):
        return (dt - datetime.datetime(1970,1,1)).total_seconds()

    def is_hit(timestamp):
        return True
        now = to_timestamp(datetime.datetime.now())
        dt = datetime.datetime.fromtimestamp(timestamp)
        return now > dt + 1

    update = config['pending_update']
    if is_hit(float(update['timestamp'])):
        directory = update['match']
        directories.hit(directory)
        config.save()
    

def main():
    current_dir = os.getcwd()

    if 'pending_update' in config.data:
        resolve_pending_update(directories)

    if sys.argv[1] == '-a':
        add_directory(current_dir, directories)

    elif sys.argv[1] == '-d':
        dir2remove = sys.argv[2] if len(sys.argv) > 2 else current_dir
        delete_directory(dir2remove, directories)

    else:
        pattern = sys.argv[1]
        print_matches(pattern, directories, current_dir)

    config.save()


if __name__ == '__main__':
    main()
