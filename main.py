import argparse
import os
import datetime
from database import create_session, Product
from sqlalchemy.orm import Session
from functools import partial


def add_handler(args, session: Session):
    name = "".join(args.name)
    category = "".join(args.category)
    price = args.price
    session.add(Product(name=name, category=category, price=price))
    session.commit()
    return True


def show_handler(args, session: Session):
    return True


def remove_handler(args, session: Session):
    return True


def quit_handler(args):
    return False


def create_parser(session):
    parser = argparse.ArgumentParser(prog='main', exit_on_error=False)
    subparsers = parser.add_subparsers(help='sub-command help', required=True)

    parser_add = subparsers.add_parser('add', help='add product')
    parser_add.add_argument('name', nargs='+', type=str, help='product name: str')
    parser_add.add_argument('category', nargs='+', type=str, help='product category: str')
    parser_add.add_argument('price', type=int, help='product price: int')
    parser_add.set_defaults(func=partial(add_handler, session=session))

    parser_show = subparsers.add_parser('show', help='show products')
    min_max_group = parser_show.add_mutually_exclusive_group()
    min_max_group.add_argument('--asc', action='store_true', help='sorting products in ascending order')
    min_max_group.add_argument('--des', action='store_true', help='sorting products in descending order')
    parser_show.add_argument('-category', nargs='+', type=str, help='list of categories to show')
    parser_show.add_argument('-date', nargs='+', type=str, help='list of dates to show')
    parser_show.set_defaults(func=partial(show_handler, session=session))

    parser_remove = subparsers.add_parser('remove', help='remove product by id')
    parser_remove.add_argument('id', type=int, help='product id: int')
    parser_remove.set_defaults(func=partial(remove_handler, session=session))

    parser_quit = subparsers.add_parser('quit', help='quit app')
    parser_quit.set_defaults(func=quit_handler)
    return parser


def main():
    os.system("cls||clear")
    session = create_session()
    parser = create_parser(session)
    args_string = input("Type your commands, --help to see help\n")
    help_flag = False
    try:
        args = parser.parse_args(args_string.split())
    except SystemExit:

    print("111111")
    while help_flag or args.func(args):
        os.system("cls||clear")
        args_string = input("Type your commands, -help to see help\n")
        args = parser.parse_args(args_string.split())
    
    

if __name__ == "__main__":
    main()
# print(parser.parse_args(['--foo', 'b', '--baz', 'Z']))