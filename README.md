<html><p><a href="https://loko-ai.com/" target="_blank" rel="noopener"> <img style="vertical-align: middle;" src="https://user-images.githubusercontent.com/30443495/196493267-c328669c-10af-4670-bbfa-e3029e7fb874.png" width="8%" align="left" /> </a></p>
<h1>SQL-tools</h1><br></html>


 **SQL-tools** is a Loko extension dealing with SQL DBs connections:

- **MySQL**
- **MariaDB**
- **Postgres**
- **SQLite**

It allows to query and insert the data in the chosen database directly within the workflows.

Within the blocks you can set the connection information: 

<p align="center"><img src="https://user-images.githubusercontent.com/30443495/220159411-c9d66c16-b30c-4d2d-8f7a-c223d01de41a.png" width="80%" /></p>

Ones the block is configured, you can insert new data directly from dictionaries:
<p align="center"><img src="https://user-images.githubusercontent.com/30443495/220306011-2db2650d-c603-4f1c-960b-8d20a858181d.png" width="80%" /></p>

Or execute any query you need using strings:

**Example 1:** create a new table
```
CREATE TABLE mytable (article varchar(255), dealer varchar(255), price double);
```
**Example 2:** query the DB
```
SELECT * FROM mytable LIMIT 10 OFFSET 20
```
In this case,  you'll receive the result as the output of the block.

## Configuration

In the file *config.json* you can find some ready-to-use side containers:

- **mysql**
- **mariadb**
- **postgres**
- **phpadmin**

The last one is a GUI to interact with mysql and mariadb.

<p align="center"><img src="https://user-images.githubusercontent.com/30443495/220311102-4a3ff4d0-a8d8-4814-a953-bf93522a4ce1.png" width="80%" /></p>

In the main volumes you can mount the **SQLite** db:

```
{
  "main": {
    "volumes": [
      "/var/opt/loko/sqlite:/plugin/resources/sqlite"
    ]
  },
...
```


