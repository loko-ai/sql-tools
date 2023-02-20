from collections import Counter

from loguru import logger
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Unicode, text
from sqlalchemy.dialects.mysql import insert
from sqlalchemy_utils import database_exists, create_database



class SQLConnection:

    def __init__(self):
        self.connections = dict()

    def __getitem__(self, url):

        if url not in self.connections:
            logger.debug(f'Connecting to url: {url}')
            engine = create_engine(url, pool_recycle=1800)
            if not database_exists(engine.url):
                db_name = str(engine.url).split('/')[-1]
                logger.debug(f'Create DB: {db_name}')
                create_database(engine.url)
            self.connections[url] = SQLDAO(engine=engine)
        return self.connections[url]


class SQLDAO:

    def __init__(self, engine):

        self.engine = engine

    def _stream(f):
        def rename_columns(cols):
            for k, v in Counter(cols).items():
                if v > 1:
                    for i in range(v):
                        idx = cols.index(k)
                        cols[idx] = f'{k}-{i}'
            return cols

        def res(self, *args, **kwargs):
            result_set = f(self, *args, **kwargs)
            if result_set.cursor:
                cols = rename_columns(list(result_set.keys()))
                for row in result_set:
                    yield dict(zip(cols, row))
            else:
                yield '"Query executed"'

        return res

    @property
    def metadata(self):
        self._metadata = MetaData()
        self._metadata.reflect(bind=self.engine)
        return self._metadata


    def tables(self):
        return self.metadata.tables


    def save(self, table, obj):

        metadata = self.metadata


        if table not in self.tables():

            t = Table(table, metadata, Column('_id', Integer, primary_key=True),
                      *(Column(wordCol, Unicode(255)) for wordCol in obj[0] if wordCol!='_id'))
            metadata.create_all(self.engine)


        with self.engine.connect() as connection:

            t = metadata.tables[table]
            stmt = insert(t).values(obj)
            connection.execute(stmt)
            connection.commit()

    @_stream
    def query(self, q):

        with self.engine.connect() as connection:
            for qrow in q.split(';'):
                qrow = qrow.strip()
                if qrow:
                    logger.debug(f'QUERY: {qrow}')
                    result = connection.execute(text(qrow))
                    connection.commit()
            return result

if __name__ == '__main__':

    connections = SQLConnection()
    
    user = 'root'
    password = 'root_password'
    host = '0.0.0.0'
    db = 'mydb'

    ### mysql ###
    port = '3306'
    url = f'mysql+pymysql://{user}:{password}@{host}:{port}/{db}'
    ### postgres ###
    port = '5432'
    url = f'postgresql://{user}:{password}@{host}:{port}/{db}'

    ### sqlite ###
    url = f'sqlite:////home/cecilia/loko/projects/sql-tools/resources/sqlite/{db}.db'

    ### mariadb ###
    # port = '3307'
    # # user = 'user'
    # # password = 'password'
    # url = f'mariadb+mariadbconnector://{user}:{password}@{host}:{port}/{db}'

    dao = connections[url]
    table = 'shop'

    dao.save(table, [dict(article=1, dealer='A', price=3.45), dict(article=1, dealer='B', price=3.99),
                      dict(article=2, dealer='A', price=10.99), dict(article=3, dealer='B', price=1.45),
                      dict(article=3, dealer='C', price=1.69), dict(article=3, dealer='D', price=1.25),
                      dict(article=4, dealer='D', price=19.95), dict(article=1, dealer='A', price=None)])

    res = dao.query('SELECT * FROM shop')
    print(list(res))

