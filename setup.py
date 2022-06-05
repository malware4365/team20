import mysql.connector
from mysql.connector import errorcode
from database import cursor, db, dbname

def create_database(db_name):
    cursor.execute("CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET 'utf8'".format(db_name))
    print(f"Database {db_name} created.")

# %%
def create_tables(filename):
    with open(filename, 'r') as f:
        for line in f.read().split(';'):
            try:
                cursor.execute(line.strip())
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print(f'\n Table "{line.strip().split("(")[0].split()[-1].upper()}" exists.')
                else:
                    print(err.msg)


def insert_table(filename):
    with open(filename, 'r') as f:
        for line in f.read().split(';'):
            if line != '':
                cursor.execute(line.strip())
        db.commit()

# %%
create_database(dbname)
cursor.execute(f'USE {dbname}')

import os
path = os.getcwd() + "/sql_setup"
create_tables(f'{path}/mytables.sql')
import os
for item in sorted(os.listdir(path)):
    if item.startswith('insert_'):
        try:
            insert_table(path+'/'+item)
        except:
            print('error', item)

#cursor.execute("""CREATE VIEW ageview AS (SELECT nfc_id, timestampdiff( year , customer.birthdate, CURDATE()) AS AGE FROM customer)""")
