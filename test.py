"""Test Module."""

import sys
from argparse import ArgumentParser

from resources.lib.m3u import M3U, M3UError


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

    m3u = M3U(args.playlist)
    try:
        m3u.parse()
    except M3UError as err:
        print(f'Failed to parse {args.playlist}: "{err.get_message()}')


if __name__ == '__main__':
    main()
