import pymysql
from icecream import ic
import sys

ic.configureOutput(includeContext=True)

# SQL Tutorial
# https://www.w3schools.com/sql/sql_where.asp
# https://www.tutorialspoint.com/sql/sql-create-table.htm

class Database:
    def __init__(self, host, user, passwd, db):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db

        self.cursor = None  # Cursor 객체
        self.conn = None    # Connection 객체

    ###################################################################
    # Connect DB
    ###################################################################
    def connect_db(self):
        try:
            if self.conn is None:
                self.conn = pymysql.connect(host=self.host,
                                            user=self.user,
                                            password=self.passwd,
                                            db=self.db)
                # self.cursor = self.conn.cursor()                            # row[0], row[1], row[2], ...
                self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)  # row['user'], row['age'], row['name'], ...

            ic('DB is connected')
        except Exception as e:
            message = f'--> Exception is {e} (Line: {sys.exc_info()[-1].tb_lineno})'
            ic(message)

    ################################################################
    # Execute Only
    ################################################################
    def execute_only(self, sql, values=None):
        try:
            # select * from elias;
            # select * from elias where name = "kim" and age = 20;
            # name = "kim"
            # age = 20
            # sql = 'select * from elias where name = %s, and age = %s;'
            # values = (name, age)
            # sql = f'select * from elias where name = "{name}", and age = {age};'
            if self.conn is not None:
                if values is None:
                    self.cursor.execute(sql)
                else:
                    self.cursor.execute(sql, values)
            else:
                ic('DB is not connected!!!')
        except Exception as e:
            message = f'--> Exception is {e} (Line: {sys.exc_info()[-1].tb_lineno})'
            ic(message)

    ################################################################
    # Execute And Commit (Insert, Update, Delete, ...)
    ################################################################
    def execute_and_commit(self, sql, values=None):
        try:
            if self.conn is not None:
                self.execute_only(sql, values)
                self.conn.commit()
            else:
                ic('DB is not connected!!!')
        except Exception as e:
            message = f'--> Exception is {e} (Line: {sys.exc_info()[-1].tb_lineno})'
            ic(message)

    ################################################################
    # Commit Only
    ################################################################
    def commit_only(self):
        try:
            if self.conn is not None:
                self.conn.commit()
            else:
                ic('DB is not connected!!!')
        except Exception as e:
            message = f'--> Exception is {e} (Line: {sys.exc_info()[-1].tb_lineno})'
            ic(message)

    ################################################################
    # Execute and Return All
    ################################################################
    def execute_and_return(self, sql, values=None):
        try:
            if self.conn is not None:
                self.execute_only(sql, values)
                data_list = self.cursor.fetchall()
                return data_list
            else:
                ic('DB is not connected!!!')
        except Exception as e:
            message = f'--> Exception is {e} (Line: {sys.exc_info()[-1].tb_lineno})'
            ic(message)

    ################################################################
    # Execute and Return One
    ################################################################
    def execute_and_return_one(self, sql, values=None):
        try:
            if self.conn is not None:
                self.execute_only(sql, values)
                data = self.cursor.fetchone()
                return data
            else:
                ic('DB is not connected!!!')
        except Exception as e:
            message = f'--> Exception is {e} (Line: {sys.exc_info()[-1].tb_lineno})'
            ic(message)

    ################################################################
    # Disconnect
    ################################################################
    def disconnect_db(self):
        try:
            if self.conn is not None:
                self.conn.close()
                self.conn = None
                self.cursor = None
            else:
                ic('DB is not connected!!!')
        except Exception as e:
            message = f'--> Exception is {e} (Line: {sys.exc_info()[-1].tb_lineno})'
            ic(message)

if __name__ == '__main__':
    # DB 객체 생성 및 연결
    db = Database(host='211.169.249.211', user='dbuser', passwd='dbuser', db='lg_autotest')
    db.connect_db()

    table_name = 'elias'

    ################################################################
    # Create Table
    ################################################################
    # sql = f'create table if not exists {table_name} (' \
    #       f'id int(11) not null auto_increment, ' \
    #       f'reg_datetime datetime default current_timestamp(), ' \
    #       f'name varchar(32) default null, ' \
    #       f'age int(11) default 0, ' \
    #       f'key id (id)) ' \
    #       f'engine=innodb default charset=utf8mb4 collate=utf8mb4_general_ci;'
    # db.execute_and_commit(sql)

    ################################################################
    # Insert Data
    ################################################################
    name = "Elias Kim"
    age = 20
    # Way I
    # sql = f'insert into {table_name} (name, age) values ("{name}", {age});'
    # db.execute_and_commit(sql)

    # Way II
    # sql = f'insert into {table_name} (name, age) values (%s, %s);'
    # values = (name, age)
    # db.execute_and_commit(sql, values)

    # for i in range(100):
    #     sql = f'insert into {table_name} (name, age) values(%s, %s);'
    #     values = (f'{table_name}_{i+1}', (20 + i)) # elias_1, 20, elias_2, 21, ...
    #     # db.execute_and_commit(sql, values)
    #     db.execute_only(sql, values)
    # db.commit_only()

    ################################################################
    # Get Data List from Table
    ################################################################
    # sql = f'select * from {table_name};'
    # data_list = db.execute_and_return(sql)
    # for data in data_list:
    #     ic(data)

    ################################################################
    # Get One Data from Table
    ################################################################
    # sql = f'select count(*) as cnt from {table_name};'
    # data = db.execute_and_return_one(sql)
    # ic(data)
    # ic(data['cnt'])

    ################################################################
    # Update Data
    ################################################################
    # id = 2
    # new_name = 'Hong Gil Dong'
    # new_age = 30
    #
    # sql = f'update {table_name} set name = %s, age=%s, reg_datetime=current_timestamp() where id = %s;'
    # values = (new_name, new_age, id)
    # db.execute_and_commit(sql, values)

    ################################################################
    # Delete Data
    ################################################################
    # id = 2
    # sql = f'delete from {table_name} where id = {id};'
    # db.execute_and_commit(sql)

    ################################################################
    # Disconnect DB
    ################################################################
    db.disconnect_db()


















