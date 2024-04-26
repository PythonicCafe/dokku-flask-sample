import os

import psycopg2

DATABASE_URL = os.environ["DATABASE_URL"]

connection = psycopg2.connect(dsn=DATABASE_URL)


def execute_query(sql, args=None):
    """Execute a query with or without arguments (do not return any data)"""
    with connection.cursor() as cursor:
        if args is None:
            cursor.execute(sql)
        else:
            cursor.execute(sql, args)
    connection.commit()


def query_data(sql, args=None):
    """Query the database and yields dicts"""
    with connection.cursor() as cursor:
        if args is None:
            cursor.execute(sql)
        else:
            cursor.execute(sql, args)
        header = [item[0] for item in cursor.description]
        for row in cursor.fetchall():
            yield dict(zip(header, row))
