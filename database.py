import mysql.connector

dbname = "team20"

config = {
    'host':'localhost',
    'user':'root',
    'passwd':'123456',
    'auth_plugin':'mysql_native_password',
}

db  = mysql.connector.connect(**config)
cursor = db.cursor(buffered=True)


def fetch_tables():
    """gets table names"""
    tables = dict()
    cursor.execute('show tables')
    t_keys = [x[0].encode("utf-8").decode("utf-8") for x in cursor.fetchall()]
    for x in t_keys:
        sql = f'show columns from {x}'
        cursor.execute(sql)
        t_val = [val[0] for val in cursor.fetchall()]
        tables.update({x:t_val})
    return tables