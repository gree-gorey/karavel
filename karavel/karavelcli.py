import os
import sys
import argparse

from functions import *


def parser():
    parser = argparse.ArgumentParser()
    template_p = argparse.ArgumentParser(add_help=False)
    template_p.add_argument(
        dest='chart', metavar='CHART', type=str,
        help='path to the directory containing chart')
    template_p.add_argument(
        '-o', '--output', dest='output', help='output format: yaml, json')
    template_p.add_argument(
        '-f', '--values', dest='values', action='append',
        default=['values.yaml'], help='path to the values file')
    template_p.set_defaults(func=template_chart)

    subparsers = parser.add_subparsers(
        title='list of subcommands', dest='service_command',
        metavar='subcommand')
    subparsers.add_parser(
        'template', help='genaretes template', parents=[template_p])

    dep_p = argparse.ArgumentParser(add_help=False)
    dep_p.add_argument(
        dest='chart', metavar='CHART', type=str, nargs=1,
        help='path to the directory containing chart')
    dep_p.set_defaults(func=ensure)
    subparsers.add_parser(
        'ensure', help='ensure helm dependencies', parents=[dep_p])

    return parser


if __name__ == '__main__':
    path = os.environ['KARAVEL_PATH']
    sys.path.append(path)
    parser = parser()
    args = parser.parse_args()
    args.func(args)
