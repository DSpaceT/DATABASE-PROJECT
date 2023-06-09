import requests
from flask import Flask,make_response,request,render_template
# from flask_mysqldb import MySQL
import mysql.connector as con
import random
import json
import datetime
from datetime import timedelta

mydb = con.connect(
host = "localhost",
user = "root",
password = '',
database = "schooldatabasev4"
)

cursor = mydb.cursor(buffered = True)

cursor.execute('SELECT * FROM App_user WHERE type="Μαθητής" OR type="Καθηγητής" ORDER BY RAND()')
data = cursor.fetchall()

end_date_req = datetime.date.today()
start_date_req = end_date_req - datetime.timedelta(days=10)
start_date = datetime.date(2022, 9, 11)
end_date = datetime.date(2023,5,10)


for i in range(140):
    result = data[random.randint(0,len(data)-1)]
    user_id = result[0]
    school_id = result[1]
    cursor.execute('SELECT isbn,copies FROM Stores WHERE Stores.school_id={} ORDER BY RAND() LIMIT 1'.format(school_id))
    isbn = cursor.fetchall()[0][0]
    num_days = (end_date-start_date).days
    rand_days = random.randint(1,num_days)
    random_date = start_date + datetime.timedelta(days=rand_days)
    return_date = random_date + datetime.timedelta(days=7)
    cursor.execute('INSERT INTO Borrow(isbn,user_id,return_date,acquire_date,active) VALUES({},{},"{}","{}",0)'.format(isbn,user_id,return_date,random_date))
    mydb.commit()
    cursor.execute('SELECT School.total_borrows FROM School WHERE School.school_id = {}'.format(school_id))
    total_borrows = cursor.fetchall()[0][0]
    cursor.execute('UPDATE School SET School.total_borrows = {} WHERE School.school_id = {}'.format(total_borrows+1,school_id))
    mydb.commit()
    
for i in range(70):
    result = data[random.randint(0,len(data)-1)]
    user_id = result[0]
    school_id = result[1]
    cursor.execute('SELECT * FROM Request WHERE user_id={}'.format(user_id))
    check = cursor.fetchall()
    if check:
        continue
    else:
        cursor.execute('SELECT isbn FROM Stores WHERE Stores.school_id={} ORDER BY RAND() LIMIT 1'.format(school_id))
        isbn = cursor.fetchall()[0][0]
        num_days = (end_date_req - start_date_req).days
        rand_days = random.randint(1,num_days)
        random_date = start_date_req + datetime.timedelta(days=rand_days)
        cursor.execute('INSERT INTO Request(date_of_request,isbn,user_id) VALUES("{}",{},{})'.format(random_date,isbn,user_id))
        mydb.commit()
    
for i in range(40):
    result = data[random.randint(0,len(data)-1)]
    user_id = result[0]
    school_id = result[1]
    cursor.execute('SELECT isbn,copies FROM Stores WHERE Stores.school_id={} AND copies>0 ORDER BY RAND() LIMIT 1'.format(school_id))
    isbn = cursor.fetchall()[0][0]
    cursor.execute('SELECT * FROM Borrow WHERE user_id={} and active=1'.format(user_id))
    check = cursor.fetchall()
    if check:
        continue
    else:
        try:
            num_days = (end_date_req-start_date_req).days
            rand_days = random.randint(1,num_days)
            random_date = start_date_req + datetime.timedelta(days=rand_days)
            cursor.execute('INSERT INTO Borrow(isbn,user_id,acquire_date,active) VALUES({},{},"{}",1)'.format(isbn,user_id,random_date))
            mydb.commit()
            cursor.execute('UPDATE Stores SET copies WHERE isbn={} AND school_id={}'.format(isbn,school_id))
            mydb.commit()
            cursor.execute('UPDATE School SET total_borrows=total_borrows+1 WHERE school_id={}'.format(school_id))
            mydb.commit() 
        except:
            continue