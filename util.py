import pymysql
# import pymysql.cursors

def create_connection():
    connection = pymysql.connect(host='localhost',
                                user='root',
                                password='root',
                                db='twitter_love',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)

    return connection

def close_connection(connection=None):
    if not connection:
        return
    else:
        connection.commit()
        connection.close()