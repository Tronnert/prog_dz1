import argparse
import os
import datetime


def add_handler(args):
    ...


def show_handler(args):
    ...


def remove_handler(args):
    ...


parser = argparse.ArgumentParser(prog='main')
subparsers = parser.add_subparsers(help='sub-command help', required=True)

parser_add = subparsers.add_parser('add', help='add help')
parser_add.add_argument('name', type=str, help='product name: str')
parser_add.add_argument('category', type=str, help='product category: str')
parser_add.add_argument('price', type=int, help='product price: int')
parser_add.set_defaults(func=add_handler)

parser_show = subparsers.add_parser('show', help='show help')
min_max_group = parser_show.add_mutually_exclusive_group()
min_max_group.add_argument('--asc', action='store_true', help='sorting products in ascending order')
min_max_group.add_argument('--des', action='store_true', help='sorting products in descending order')
parser_show.add_argument('-category', nargs='+', type=str, help='list of categories to show')
parser_show.add_argument('-date', nargs='+', type=str, help='list of dates to show')
parser_show.set_defaults(func=show_handler)

parser_remove = subparsers.add_parser('remove', help='remove help')
parser_remove.add_argument('id', type=int, help='product id: int')
parser_remove.set_defaults(func=remove_handler)

def main():
    os.system("cls||clear")

# print(parser.parse_args(['--foo', 'b', '--baz', 'Z']))