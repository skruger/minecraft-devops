#!/usr/bin/env python3

import argparse
import os
import sys
import subprocess
import tempfile


def get_argparser():
    parser = argparse.ArgumentParser()

    cmd = parser.add_subparsers()

    trim = cmd.add_parser('trim_chunks')
    trim.add_argument('--world', default='world')
    trim.add_argument('--region', default=None)
    trim.add_argument('--chunk-query')
    trim.set_defaults(func=trim_chunks)
    return parser


def trim_chunks(options):
    jars = os.environ.get('SCRIPTS', 'scripts')
    selected_chunks = tempfile.mktemp('.csv', 'selectedchunks')
    cmd = [
        'java',
        '-jar', f'{jars}/mcaselector.jar',
        '--mode', 'select', '--query', options.chunk_query,

        '--world', options.world,
        '--output', selected_chunks,
    ]
    if options.region:
        cmd.extend(['--region', options.region])

    print(cmd)
    completed_select = subprocess.run(cmd)
    if completed_select.returncode != 0:
        return

    cmd = [
        'java',
        '-jar', f'{jars}/mcaselector.jar',
        '--mode', 'delete', '--query', options.chunk_query,

        '--world', options.world,
        '--selection', selected_chunks,
    ]
    if options.region:
        cmd.extend(['--region', options.region])

    print(cmd)
    completed_delete = subprocess.run(cmd)



if __name__ == '__main__':
    parser = get_argparser()
    options = parser.parse_args(sys.argv[1:])
    func = getattr(options, 'func', lambda x: print(parser.format_help()))
    func(options)
