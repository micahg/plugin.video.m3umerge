"""Test Module."""

import sys
import os
from argparse import ArgumentParser

from resources.lib.m3u import M3U, M3UError
from resources.lib.utils import log


def parse_arguments():
    print('parsing arguments')
    parser = ArgumentParser()
    parser.add_argument('-p', '--playlist', action='store', help='specify playlist file')
    args = parser.parse_args()
    return args, parser


def main():
    args, parser = parse_arguments()

    if args.playlist is None:
        print('Playlist is required for now\n\n')
        parser.print_help()
        sys.exit(1)

    if os.path.isfile(args.playlist):
        file = open(file=args.playlist, mode='r', encoding='utf-8')
    else:
        log(f'Cannot handle playlist "{args.playlist}"')
        sys.exit(1)

    m3u = M3U(file)
    try:
        channels = m3u.parse()
        for channel in channels:
            log(channel)
    except M3UError as err:
        log(f'Failed to parse {args.playlist}: "{err.get_message()}')



if __name__ == '__main__':
    main()
