#encoding:utf-8
from mysql import Mysql
import datetime
import time
from MySQLdb import escape_string

db = Mysql(host='localhost',user='root',passwd='123456',port=3306,db='pythoner_db')

def _time_stamp():
    time_stamp = datetime.datetime.fromtimestamp(time.time()).isoformat()
    return time_stamp

def insert_book(name,author,translator,publish,pub_date,instrution,price,pages,isbn,douban_id):
    """
    """

    time = _time_stamp()
    sql = """ SELECT id FROM books_book WHERE isbn='%s'""" %isbn
    name = escape_string(name)
    author = escape_string(author)
    translator = escape_string(translator)
    publish = escape_string(publish)
    instrution = escape_string(instrution)


    if db.query_one(sql):
        sql = """ UPDATE books_book SET name='%s',author='%s',translator='%s',publish='%s',pub_date='%s',instrution='%s',price='%s',pages=%d,douban_id=%d WHERE isbn='%s'""" %(name,author,translator,publish,pub_date,instrution,price,pages,douban_id,isbn)

    else:
        sql = """ INSERT INTO books_book (name,author,translator,publish,pub_date,instrution,price,pages,isbn,douban_id,category_id)
    VALUES ('%s','%s','%s','%s','%s','%s','%s',%d,%d,%d,%d)""" %(name,author,translator,publish,pub_date,instrution,price,int(pages),int(isbn),douban_id,1)

    #print sql

    return db.execute(sql)

if __name__ == '__main__':
    print insert_book('cookbook','张三','李无','人民邮电出版社','2012-12','好啊','15.2',100,123456789,12121)
