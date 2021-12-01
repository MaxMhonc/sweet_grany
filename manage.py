import argparse

from sweet_grany_app.data_service import sql_sevice


def create_tables(arg):
    sql_sevice.create_all_tables(arg)


def recreate_tables(arg):
    sql_sevice.drop_all_tables(arg)
    sql_sevice.drop_all_tables(arg)


if __name__ == '__main__':
    actions = {
        'create': create_tables,
        'recreate': recreate_tables
    }
    parser = argparse.ArgumentParser(
        description='Main module to rule dbs'
    )
    parser.add_argument('action', choices=actions.keys())
    parser.add_argument('-db', '--db_type', default='sweet_granny')
    args = parser.parse_args()
    actions[args.action](args.db_type)
