import logging
import os
import sqlite3

from gamestore.models import Game

logger = logging.getLogger(__name__)

DB_FILE = 'gamestore.sqlite'


def dict_factory(cursor, row):
    d = {}
    for i, col in enumerate(cursor.description):
        d[col[0]] = row[i]
    return d



class Cursor:
    def __init__(self):
        self.conn = None
        self.cursor = None
    def __enter__(self):
        self.conn = sqlite3.connect(DB_FILE)
        self.cursor = self.conn.cursor()
        self.cursor.row_factory = dict_factory
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        if not exc_val:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.conn.close()


class DatabaseTable:
    def __init__(self, table_name, object_model, id_field, create_sql, select_sql, insert_sql, update_sql, delete_sql):
        self.table_name = table_name
        self.object_model = object_model
        self.id_field = id_field
        self.create_sql = create_sql
        self.select_sql = select_sql
        self.insert_sql = insert_sql
        self.update_sql = update_sql
        self.delete_sql = delete_sql
        with Cursor() as c:
            c.execute("select name from sqlite_master where type='table'")
            table_names = (r['name'] for r in c.fetchall())
            if self.table_name not in table_names:
                c.execute(self.create_sql)
    def __setitem__(self, key, value):
        data = value.model_dump()
        with Cursor() as c:
            if key in self.keys():
                logger.debug('Updating item %s', key)
                c.execute(self.update_sql, data)
            else:
                logger.debug('Inseting item %s', key)
                c.execute(self.insert_sql, data)
    def __getitem__(self, key):
        with Cursor() as c:
            logger.debug('Getting item')
            c.execute(self.select_sql, {self.id_field:key})
            return self.object_model(**c.fetchone())
    def __delitem__(self, key):
        with Cursor() as c:
            logger.debug('Deleting item')
            c.execute(self.delete_sql, {self.id_field: key})

    def keys(self):
        with Cursor() as c:
            logger.debug('Getting keys')
            c.execute(f"SELECT {self.id_field} FROM {self.table_name}")
            ids = [r[self.id_field] for r in c.fetchall()]
        return ids

    def get(self, key, default=None):
        if key in self.keys():
            logger.debug('Identifier found, returning object.')
            return self.__getitem__(key)
        else:
            logger.debug('Unknown id returnind default.')
            return default


game_table = DatabaseTable(
    table_name='game',
    id_field='id',
    object_model=Game,
    create_sql="""
        create table game (
            id            int primary key     not null,
            title         text                not null,
            platform      text                not null,
            price         float               not null,
            release_year  int                 not null
        )
    """,
    select_sql="SELECT * FROM game WHERE id = :id",
    insert_sql="""
        insert into
            game (id, title, platform, price, release_year)
        values
            (:id, :title, :platform, :price, :release_year)
    """,
    update_sql="""
        update 
            game
        set
            id =:id, title =:title, platform =:platform, price =:price, release_year =:release_year
        where
            id =:id
    """,
    delete_sql="delete from game where id = :id"
)
