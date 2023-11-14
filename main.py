import argparse
import os
import re
import datetime
from database import create_session, Product
from sqlalchemy.orm import Session
from functools import partial


def custom_split(s: str):
    return list(map(lambda x: "".join(x).strip(), re.findall(r'''\"(.*?)\"|(\S+)''', s)))


def add_handler(args, session: Session):
    if args.price < 0:
        print("price must be positive")
        return True
    product = Product(name=args.name, 
                      category=args.category, 
                      date=args.date,
                      price=args.price)
    session.add(product)
    session.commit()
    session.refresh(product)
    print(f"added product {product.name} with id {product.id}")
    return True


def show_handler(args, session: Session):
    query = session.query(Product)
    if args.category != None:
        query = query.filter(Product.category.in_(args.category))
    if args.date != None:
        query = query.filter(Product.date.in_(args.date))
    result = query.all()
    if result == []:
        print("no products with current filters")
    else:
        for product in result:
            print(*[product.id, 
                    product.name, 
                    product.category, 
                    product.date, 
                    product.price], 
                    sep="\t")
    return True


def remove_handler(args, session: Session):
    product = session.get(Product, args.id)
    if product != None:
        session.delete(product)
        session.commit()
    else:
        print("there is no product with this id")
    return True


def quit_handler(args):
    return False


def date(x):
    return datetime.datetime.strptime(x, '%Y-%m-%d').strftime('%Y-%m-%d')


def create_parser(session):
    parser = argparse.ArgumentParser(prog='main', exit_on_error=False)
    subparsers = parser.add_subparsers(help='sub-command help', required=True)

    parser_add = subparsers.add_parser('add', help='add product')
    parser_add.add_argument('name', type=str, help='''product name: str (str with whitespace like what: "a b")''')
    parser_add.add_argument('category', type=str, help='product category: str')
    parser_add.add_argument('date', type=date, 
                            help='''product date: date (in '%%Y-%%m-%%d' format)''')
    parser_add.add_argument('price', type=int, help='product price: int')
    parser_add.set_defaults(func=partial(add_handler, session=session))

    parser_show = subparsers.add_parser('show', help='show products')
    min_max_group = parser_show.add_mutually_exclusive_group()
    min_max_group.add_argument('--asc', action='store_true', help='sorting products in ascending order')
    min_max_group.add_argument('--des', action='store_true', help='sorting products in descending order')
    parser_show.add_argument('-category', nargs='+', type=str, help='list of categories to show')
    parser_show.add_argument('-date', nargs='+', type=date, 
                             help='''list of dates to show (in '%%Y-%%m-%%d' format)''')
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
    os.system("cls||clear")
    try:
        args = parser.parse_args(custom_split(args_string))
    except SystemExit:
        help_flag = True
    while help_flag or args.func(args):
        help_flag = False
        args_string = input("Type your commands, -help to see help\n")
        os.system("cls||clear")
        try:
            args = parser.parse_args(custom_split(args_string))
        except SystemExit:
            help_flag = True
    
    

if __name__ == "__main__":
    main()