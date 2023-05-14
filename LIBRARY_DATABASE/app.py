# from flask import Flask,make_response,render_template
# from flask import request
import flask
from flask_mysqldb import MySQL
import mysql.connector as con
from flask_mysqldb import MySQL
from flask_cors import CORS,cross_origin
# from flask import jsonify
import route_functions

import json
# from datetime import date

app = flask.Flask(__name__)
cors = CORS(app,resources={
    r"/*":{
        "origins":"*"
    }
})

mydb = con.connect(
host = "localhost",
user = "root",
password = "",#"ChoedanKal2002",
database = "schooldatabasev4",
autocommit = True
)

cursor = mydb.cursor(buffered = True)



@app.route('/register', methods=['GET','POST'])
def register():
    if flask.request.method == 'GET':
        # cursor.execute('SELECT name FROM School')
        # to_send = cursor.fetchall()

        # return flask.jsonify(to_send)
        cursor.execute('SELECT name,city FROM School')
        to_send = cursor.fetchall()
        data = [dict(zip(("name","city"), x))for x in to_send]
        return flask.jsonify(data)
    elif flask.request.method == 'POST':
        data = flask.request.get_json(['body'])
        #school_id = route_functions.fschool_name(data['school_name'])
        school_id = route_functions.fschool_name_city(data['school_name'],data['city'])
        admin_id = route_functions.fadmin_schoolid(school_id)
        route_functions.insert_user(school_id,data['first_name'],data['last_name'],data['birthday'].split('-')[0],data['role'],admin_id)
        user_id = route_functions.fuser_flname(data['first_name'],data['last_name'])
        route_functions.insert_authentication(user_id,data['username'],data['password'])

        return {"data":"monument"}
    else:
        print("ERROR")
        return 1



@app.route('/signin',methods = ['POST'])
@cross_origin(headers=['Content-Type']) 
def sign_in():
    
    data = flask.request.get_json(['body'])
    username = data['username']
    password = data['password']
    cursor.execute('SELECT user_id FROM Authentication WHERE username = "{}" AND password = "{}"'.format(username, password))
    try:
        user_id = cursor.fetchall()[0][0]
        cursor.execute('SELECT Authentication.username,Authentication.password,School.name\
                       ,App_user.first_name,App_user.last_name,App_user.type,App_user.age\
                        FROM Authentication JOIN App_user\
                        ON App_user.user_id = Authentication.user_id JOIN School\
                        ON School.school_id = App_user.school_id\
                        WHERE Authentication.user_id = {}'.format(user_id))
        result = cursor.fetchall()
        mydb.commit()
        return flask.jsonify({"username":result[0][0],"password":result[0][1],"school_name":result[0][2],"first_name":result[0][3],"last_name":result[0][4],"role":result[0][5],"age":result[0][6],"user_id":user_id})
    except:
        print("no user found")
        return flask.jsonify({"result": "failure","data":0})
    # else:
    #     return 1

@app.route('/books',methods = ['POST'])
@cross_origin(headers=['Content-Type'])
def books():
    data = flask.request.get_json(['body'])
    school_name = data['school_name']
    #school_city = data['city']
    cursor.execute('SELECT Books.isbn,Books.page_count,Books.publisher,Books.title,Books.summary,Books.cover_path,Books.m_cover_path,Stores.copies\
                FROM Books\
                JOIN Stores\
                ON Stores.isbn = Books.isbn\
                JOIN School\
                ON School.school_id = Stores.school_id\
                WHERE School.name = "{}";'.format(school_name))#AND School.city = "{}";'.format(school_name,school_city))
    book_data = cursor.fetchall()
    book_dict = [dict(zip(("isbn","page_count","publisher","title","summary","cover","cover_m","copies"), x))for x in book_data]
    for i in range(len(book_dict)):
        cursor.execute('SELECT Authors.first_name,Authors.last_name FROM Authors WHERE Authors.isbn = {}'.format(book_dict[i]['isbn']))
        authors = cursor.fetchall()
        book_dict[i]['authors'] = authors
    for i in range(len(book_dict)):
        cursor.execute('SELECT Keywords.keyword FROM Keywords WHERE isbn = {}'.format(book_dict[i]['isbn']))
        keywords = cursor.fetchall()
        book_dict[i]['keywords'] = keywords

    #cursor.execute('SELECT Keywords.keyword FROM Keywords JOIN ')

    return flask.jsonify(book_dict)
    # "result":"success","isbn":book_data[0][0],"page_count":book_data[0][1],"publisher":book_data[0][2],"title":book_data[0][3],"summary":book_data[0][4],"cover":book_data[0][5]


@app.route('/borrow',methods = ['POST','PUT'])
@cross_origin(headers=['Content-Type'])
def borrow():
    if flask.request.method == 'POST':
        data = flask.request.get_json(['body'])
        username = data['username']
        type = data['role']
        if type == "Μαθητής":
            try:
                result = route_functions.fborrow_username(username)
                borrow_dict = [dict(zip(('isbn','title','cover_m','username','first_name','last_name','return_date','acquire_date'),x)) for x in result]
                return flask.jsonify(borrow_dict)
            except:
                print("fail")
                return flask.jsonify({"result":"no_borrows"})
        elif (type == "Admin"):
            try:
                result = route_functions.fborrow_school(username)
                return flask.jsonify(result)
            except:
                print("hello from here")
                return flask.jsonify({"result": "fail"})
    elif flask.request.method == 'PUT':
        data = flask.request.get_json(['body'])
        username = data['username']
        title = data['title']
        isbn = route_functions.fbook_title(title)
        user_id = route_functions.fuser_username(username)
        print(user_id)
        print(isbn)
        route_functions.delete_borrow(user_id,isbn)
        #ΥΠΑΡΧΕΙ ΕΝΑ ERROR επειδή για καποιο λόγω βιβλία με διαφορετικό isbn μπορεί να έχουν το ιδιο
        #τίτλο και η sql δεν ξεχωρίζει τα κεφαλαία γράμματα απο τα μικρά
        return flask.jsonify({"delete":"success"})
    
@app.route('/request',methods = ['POST','PUT'])
@cross_origin(headers=['Content-Type']) #Δεν την έχω δοκιμάσει ακόμα
def request():
    if flask.request.method == 'POST':
        data = flask.request.get_json(['body'])
        username = data['username']
        type = data['role']
        print("hi from here")
        if type == "Μαθητής":
            # Στέλνω isbn,title,username,first_name,last_name,date_of_request
            result = route_functions.frequest_username(username)
            request_dict = [dict(zip(('isbn','title','cover_m','username','first_name','last_name','date_of_request'),x)) for x in result]
            return flask.jsonify(request_dict)
        elif type == "Admin":
            # Στέλνω isbn,title,username,first_name,last_name,date_of_request
            result = route_functions.frequest_school(username)
            return flask.jsonify(result)
    elif flask.request.method == 'PUT':
        data = flask.request.get_json(['body'])
        username = data['username']
        isbn = data['isbn']
        user_id = route_functions.fuser_username(username)
        route_functions.delete_request(user_id,isbn)
        return flask.jsonify({"delete":"successful"})


@app.route('/book_request',methods = ['POST'])
@cross_origin(headers=['Content-Type']) 
def request_book():
    data = flask.request.get_json(['body'])
    username = data['username']
    isbn = data['isbn']
    user_id = route_functions.fuser_username(username)
    cursor.execute('INSERT INTO Request(date_of_request, isbn, user_id) VALUES(CURDATE(), {},{})'.format(isbn,user_id))
    mydb.commit()
    return flask.jsonify({'success':'success'})

@app.route('/reviews',methods = ['POST'])
@cross_origin(headers=['Content-Type'])
def get_reviews():
    data = flask.request.get_json(['body'])
    isbn = data['isbn']
    type = data['role']
    username = data['username']

    if type == "Μαθητής":
        result = route_functions.freview_isbn_approved(isbn)
        reviews_dict = [dict(zip(('review_date','score','description','first_name','last_name','approved'),x))for x in result]

        return flask.jsonify(reviews_dict)
    elif type == "Admin":
        school_id = route_functions.fschool_username(username)
        result = route_functions.freview_school(school_id)
        reviews_dict = [dict(zip(('review_date','score','description','first_name','last_name','approved'),x))for x in result]
        return flask.jsonify(reviews_dict)


@app.route('/user_review',methods = ['POST'])
@cross_origin(headers=['Content-Type'])
def hasReviewed():
    data = flask.request.get_json(['body'])
    isbn = data['isbn']
    username = data['username']
    user_id = route_functions.fuser_username(username)
    cursor.execute('SELECT * FROM Review WHERE isbn={} AND user_id={}'.format(isbn,user_id))
    result = cursor.fetchall()
    mydb.commit()
    if result:
        return flask.jsonify({'reviewed':'yes'})
    else:
        return flask.jsonify({'reviewed': 'none'})

@app.route('/submit_review',methods = ['POST'])
@cross_origin(headers=['Content-Type'])
def submit_review():
    data = flask.request.get_json(['body'])
    isbn = data['isbn']
    username = data['username']
    score = data['score']
    description = data['description']
    score = int(score)
    user_id = route_functions.fuser_username(username)
    cursor.execute('INSERT INTO Review(date_of_review,score,description,isbn,user_id,approved) VALUES(CURDATE(),{}, "{}",{},{},{})'.format(score,description,isbn,user_id,0))
    mydb.commit()
    return flask.jsonify({'success':'success'})

@app.route('/accept_review',methods = ['POST'])
@cross_origin(headers = ['Content-Type'])
def accept_review():
    data = flask.request.get_json(['body'])
    isbn = data['isbn']
    username = data['username']
    approved = data['approved']
    if approved == 1:
        route_functions.approve_review(isbn,username)
    elif approved == 0:
        route_functions.delete_review(isbn,username)
    return flask.jsonify({"success":"success"})


@app.route('/change_password',methods = ['PUT'])
@cross_origin(headers=['Content-Type'])
def changePassword():
    data = flask.request.get_json(['body'])
    username = data['username']
    password = data['new_password']
    cursor.execute('UPDATE Authentication SET password="{}" WHERE username="{}"'.format(password,username))
    mydb.commit()
    return flask.jsonify({'success':'success'})


if __name__ == "__main__":
    app.debug = True
    app.run(debug = True, host="localhost", port = 5000)

