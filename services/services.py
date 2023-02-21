import re

import sanic
from loguru import logger
from loko_extensions.business.decorators import extract_value_args
from sanic import Sanic, Blueprint
from sanic.exceptions import NotFound
from sanic_openapi import swagger_blueprint
from sanic_openapi.openapi2 import doc

from dao.sql_dao import SQLConnection
from utils.exceptions_utils import NotFoundError

name = "sql-tools"
app = Sanic(name)
swagger_blueprint.url_prefix = "/api"

bp = Blueprint("default")
app.config["API_TITLE"] = name
app.blueprint(swagger_blueprint)
app.blueprint(bp)



connections = SQLConnection()


def _get_dao(f):
    def tmp(value, args):

        logger.debug(f'ARGS: {args}')
        comp_name = args.get('name')
        host = args.get('host')
        port = args.get('port')
        user = args.get('user')
        password = args.get('password')
        db_name = args.get('db_name')
        if 'MySQL' in comp_name:
            db = args.get('db')
            if db == 'MySQL':
                url = f'mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}'
            else:
                url = f'mariadb+mariadbconnector://{user}:{password}@{host}:{port}/{db_name}'
        elif 'Postgres' in comp_name:
            url = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}'
        elif 'SQLite' in comp_name:
            url = f'sqlite:////plugin/resources/sqlite/{db_name}.db'

        logger.debug(f'URL: {url}')

        dao = connections[url]

        return f(dao, value, args)
    return tmp


@app.on_request
async def start_service(request):
    dashes = str("-" * 10)
    logger.info(f'{dashes}  Start:  {request.method} {request.path} {dashes}')


@app.on_response
async def end_service(request, response):
    dashes = str("-" * 10)
    if response.status == 200:
        logger.info(f'{dashes}  End (ok):  {request.method} {request.path} {dashes}')
    else:
        logger.info(
            f'{dashes}  End (error): {response.status} - {response.body} - {request.method} {request.path} {dashes}')

@bp.post("/save")
@doc.summary('It saves elements into a table given its name')
@doc.description('''
**Example:**

    {"value": [{"article": 1, "dealer": "A", "price": "3.45"}], 
     "args": {"name": "MySQL/MariaDB", "db": "MySQL", "host": "0.0.0.0", "port": 3306, 
              "user": "root", "password": "root_password", "db_name": "mydb", 
              "table_name": "mytable"}}
    ''')
@doc.consumes(doc.JsonBody({"value": dict, "args": dict}), location="body")
@extract_value_args()
@_get_dao
async def save(dao, elements, args):
    table = args.get('table_name')
    logger.debug(f'TABLE: {table}')
    if re.search('[^a-zA-Z0-9_]', table):
        return sanic.response.json('only alphanumeric and "_" characters are allowed in a table name', 400)
    elements = elements if isinstance(elements, list) else [elements]
    dao.save(table, elements)
    logger.debug(f"{len(elements)} elements saved")
    return sanic.json(f"{len(elements)} elements saved")



@bp.post("/query")
@doc.summary('Submit a query to a table and get the results')
@doc.description('''
**Example:**

    {"value": "SELECT * FROM mytable LIMIT 10 OFFSET 5",      
     "args": {"name": "MySQL/MariaDB", "db": "MySQL", "host": "0.0.0.0", "port": 3306, 
              "user": "root", "password": "root_password", "db_name": "mydb", 
              "table_name": "mytable"}}
    ''')
@doc.consumes(doc.JsonBody({"value": dict, "args": dict}), location="body")
@extract_value_args()
@_get_dao
async def query(dao, q, args):
    q = dao.query(q)
    return sanic.json(list(q))



@app.exception(Exception)
async def manage_exception(request, exception):
    logger.debug(exception)
    logger.exception('ERROR')
    if isinstance(exception, NotFound):
        return sanic.json(str(exception), status=404)
    if isinstance(exception, NotFoundError):
        return sanic.json(str(exception), status=400)
    return sanic.json(str(exception), status=500)



if __name__ == "__main__":
    app.run("0.0.0.0", 8080)
