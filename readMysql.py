import pymysql.cursors

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='pdb',
                             charset='utf8')
try:
    with connection.cursor() as cursor:
        sql = "select `name` from `pytable` where `state`='待售'"
        count = cursor.execute(sql)
        print(count)

        # result=cursor.fetchmany(size=10)
        result=cursor.fetchall()
        print(result)
finally:
    connection.close()
