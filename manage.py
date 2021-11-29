import argparse


def create_tables(arg):
    print(f'*** tables <{arg}> created ***')


def recreate_tables(arg):
    print(f'*** tables <{arg}> recreated ***')


if __name__ == '__main__':
    actions = {
        'create': create_tables,
        'recreate': recreate_tables
    }
    parser = argparse.ArgumentParser(
        description='Main module to rule dbs'
    )
    parser.add_argument('action', choices=actions.keys())
    parser.add_argument('-db', '--db_type', default='all')
    args = parser.parse_args()
    actions[args.action](args.db_type)
