import mysql.connector
from datetime import datetime

class mysql_execute():
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = 'password'
        self.cursor = None

    def connect_mysql(self):
        my_db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.password
        )

        my_cursor = my_db.cursor()
        if not self.cursor:
            self.cursor = my_cursor

    def check_database(self, database=None):
        if not database:
            return False
        my_db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.password
        )

        my_cursor = my_db.cursor()
        my_cursor.execute("SHOW DATABASES")
        for x in my_cursor:
            if x and isinstance(x, tuple) and x[0] == database:
                return True
        return False

    def check_table(self, database=None, table=None):
        if not database and self.check_database(database) and not table:
            return False
        my_db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.password,
            database=database
        )

        my_cursor = my_db.cursor()
        my_cursor.execute("SHOW TABLES")
        for x in my_cursor:
            if x and isinstance(x, tuple) and x[0] == table:
                return True
        return False

    def create_database(self, database_name=None):
        my_db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.password
        )

        my_cursor = my_db.cursor()
        if not database_name and self.check_database(database_name):
            return False
        query = 'CREATE DATABASE `' + str(database_name) + '`'
        my_cursor.execute(query)

    def create_table(self, database_name=None, table_name=None, column_data={}, is_check_exist=False):
        my_db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.password,
            database=database_name
        )

        my_cursor = my_db.cursor()
        query = 'CREATE TABLE ' + str(table_name)
        if is_check_exist:
            query = 'CREATE TABLE IF NOT EXISTS ' + str(table_name)
        list_column = list()
        for key, values in column_data.items():
            list_column.append(str(key) + ' ' + str(values))
        where = ', '.join(list_column)
        query = query + ' (' + where + ');'
        my_cursor.execute(query)
        return True

    def insert_data_row(self, database_name=None, table_name=None, data_query=dict()):
        my_db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.password,
            database=database_name
        )

        my_cursor = my_db.cursor()
        sql = "INSERT INTO " + str(table_name)
        list_key = list()
        list_value_df = list()
        for key, values in data_query.items():
            list_key.append(str(key))
            list_value_df.append('%(' + str(key) + ')s')
        list_key = ', '.join(list_key)
        list_value_df = ', '.join(list_value_df)
        sql = (sql + ' (' + list_key + ') VALUES (' + list_value_df + ');')
        my_cursor.execute(sql, data_query)
        my_db.commit()
        return my_cursor.lastrowid

    def select_data(self, database_name=None, table_name=None, data_query=dict()):
        my_db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.password,
            database=database_name
        )
        list_query = list()
        my_cursor = my_db.cursor()
        for key, values in data_query.items():
            if isinstance(values, list):
                list_query.append(str(key) + ' IN ("' + ','.join(values) + '")')
            else:
                list_query.append(str(key) + ' LIKE ' + str(values))

        sql = "SELECT * FROM " + table_name + ';' if not list_query else "SELECT * FROM " + table_name + ' WHERE ' + list_query[0] + ';'

        my_cursor.execute(sql)

        my_result = my_cursor.fetchall()
        all_result = list()
        for row in my_result:
            dict_result = dict()
            dict_result['id'] = row[0]
            dict_result['masv'] = row[1]
            dict_result['name'] = row[2]
            dict_result['age'] = row[3]
            dict_result['className'] = row[4]
            dict_result['address'] = row[5]
            dict_result['phone'] = row[6]
            dict_result['subject'] = row[7]
            dict_result['image_path'] = row[8]
            dict_result['id_path'] = row[9]
            all_result.append(dict_result)
        return all_result

    def select_data_report(self, database_name=None, data_query=dict()):
        my_db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.password,
            database=database_name
        )
        my_cursor = my_db.cursor()
        date_from = None
        date_to = None
        if data_query['from']:
            date_from = data_query['from']
        if data_query['to']:
            date_to = data_query['to']
        if not date_from:
            sql = "SELECT * FROM `report` WHERE created_at >= '" + date_from + "';"
        elif date_from and not date_to:
            sql = "SELECT * FROM `report` WHERE created_at <= '" + date_to + "';"
        elif date_from and date_to:
            sql = "SELECT * FROM `report` WHERE created_at >= '" + date_from + "' AND " + "created_at <= '" + date_to + "';"
        else:
            sql = "SELECT * FROM `report` WHERE 1;"

        my_cursor.execute(sql)

        my_result = my_cursor.fetchall()
        all_result = list()
        for row in my_result:
            dict_result = dict()
            dict_result['user_id'] = row[0]
            dict_result['created_at'] = row[1].strftime('%m-%d-%Y')
            all_result.append(dict_result)
        return all_result

    def delete_data(self, database_name=None, table_name=None, data_query=dict()):
        my_db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.password,
            database=database_name
        )
        list_query = list()
        my_cursor = my_db.cursor()
        for key, values in data_query.items():
            list_query.append('`' + str(key) + '` = ' + str(values))
        list_query = 'AND '.join(list_query) if len(list_query) > 1 else list_query[0]
        sql = "DELETE FROM " + table_name + " WHERE " + list_query
        my_cursor.execute(sql)
        my_db.commit()
        return True

    def update_data(self, database_name=None, table_name=None, data_query=dict(), where=dict()):
        my_db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.password,
            database=database_name
        )
        list_query = list()
        where_query = list()
        my_cursor = my_db.cursor()
        for key, values in where.items():
            where_query.append('`' + str(key) + '` = ' + str(values))

        for key, values in data_query.items():
            list_query.append('`' + str(key) + '` = "' + str(values) + '"')
        where_query = 'AND '.join(where_query) if len(where_query) > 1 else where_query[0]
        list_query = ', '.join(list_query) if len(list_query) > 1 else list_query[0]
        sql = "UPDATE " + table_name + " SET " + list_query + " WHERE " + where_query + ";"
        my_cursor.execute(sql)
        x = my_db.commit()
        return True
