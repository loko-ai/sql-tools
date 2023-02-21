from doc.doc import mysql_mariadb_doc, postgres_doc, sqlite_doc
from loko_extensions.model.components import Component, save_extensions, Input, Arg, AsyncSelect, Dynamic, Select, \
    Output


host_mysql = Arg(name="host",
                 label="Host",
                 type="text",
                 value="sql-tools_mysql")

port_mysql = Arg(name="port",
                 label="Port",
                 type="number",
                 value=3306)

user = Arg(name="user",
           label="User",
           type="text",
           value="root")

password = Arg(name="password",
               label="Password",
               type="password",
               value="root_password")


db_name = Arg(name="db_name",
              label="DB name",
              type="text",
              helper="Specify the DB name",
              value="mydb")

table_name = Arg(name="table_name",
                 label="Table name",
                 type="text",
                 helper="Specify the table name",
                 value="mytable")

db = Select(name='db',
            label='DB',
            options=['MySQL', 'MariaDB'],
            helper='Specify the DB type',
            value='MySQL')

inputs = [Input(id="insert", service="save", to="insert"), Input(id="query", service="query", to="query")]
outputs = [Output(id="insert"), Output(id="query")]
mysql_mariadb = Component(name="MySQL/MariaDB", inputs=inputs, outputs=outputs, icon="RiDatabase2Line",
                          args=[db, host_mysql, port_mysql, user, password, db_name, table_name],
                          description=mysql_mariadb_doc)

host_postgres = Arg(name="host",
                    label="Host",
                    type="text",
                    value="sql-tools_postgres")

port_postgres = Arg(name="port",
                 label="Port",
                 type="number",
                 value=5432)

inputs = [Input(id="insert", service="save", to="insert"), Input(id="query", service="query", to="query")]
outputs = [Output(id="insert"), Output(id="query")]
postgres = Component(name="Postgres", inputs=inputs, outputs=outputs, icon="RiDatabase2Line",
                     args=[host_postgres, port_postgres, user, password, db_name, table_name],
                     description=postgres_doc)


sqlite = Component(name="SQLite", inputs=inputs, outputs=outputs, icon="RiDatabase2Line",
                   args=[db_name, table_name],
                   description=sqlite_doc)


save_extensions([mysql_mariadb, postgres, sqlite])
