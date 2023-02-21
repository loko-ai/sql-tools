mysql_mariadb_doc = '''### Description
**MySQL/MariaDB** component is used to persist the data processed through the developed flows.

It allows to query and insert the data in the chosen database directly within the workflows.

### Configuration
- **DB** allows to select the DB type: MySQL or MariaDB.

- **Host** is used to set the host name. If you're using the extension's side container use "sql-tools_mysql" or 
"sql-tools_mariadb".

- **Port** is used to set the default port.

- **User** is used to set the user account.

- **Password** is the password associated to the user account.

- **DB name** is used to set the SQL DB.

- **Table name** is used to insert new data into a table. 

### Input
The component has two inputs:
- **Insert** accepts single dictionaries (representing rows of the table) or list of dictionaries. 
  Passing single rows as input can be time consuming. 
- **Query** requires a string containing the SQL query.

### Output
- **Save** returns a string with the number of elements saved.
- **Query** returns a dictionary for each element of the requested query. If the query produces no results, 
  "Query executed" will be returned.
'''

postgres_doc = '''### Description
**Postgres** component is used to persist the data processed through the developed flows.

It allows to query and insert the data in the chosen database directly within the workflows.

### Configuration

- **Host** is used to set the host name. If you're using the extension's side container use "sql-tools_postgres".

- **Port** is used to set the default port.

- **User** is used to set the user account.

- **Password** is the password associated to the user account.

- **DB name** is used to set the SQL DB.

- **Table name** is used to insert new data into a table. 

### Input
The component has two inputs:
- **Insert** accepts single dictionaries (representing rows of the table) or list of dictionaries. 
  Passing single rows as input can be time consuming. 
- **Query** requires a string containing the SQL query.

### Output
- **Save** returns a string with the number of elements saved.
- **Query** returns a dictionary for each element of the requested query. If the query produces no results, 
  "Query executed" will be returned.
'''

sqlite_doc = '''### Description
**SQLite** component is used to persist the data processed through the developed flows.

It allows to query and insert the data in the chosen database directly within the workflows.

### Configuration

- **DB name** is used to set the SQL DB.

- **Table name** is used to insert new data into a table. 

### Input
The component has two inputs:
- **Insert** accepts single dictionaries (representing rows of the table) or list of dictionaries. 
  Passing single rows as input can be time consuming. 
- **Query** requires a string containing the SQL query.

### Output
- **Save** returns a string with the number of elements saved.
- **Query** returns a dictionary for each element of the requested query. If the query produces no results, 
  "Query executed" will be returned.
'''