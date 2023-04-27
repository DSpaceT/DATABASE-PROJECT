from flask import Flask,make_response,request,render_template
from __init__ import app,mysql
from flask_mysqldb import MySQL
import mysql.connector as con

mydb = con.connect(
host = "localhost",
user = "root",
password = "",
database = "schooldatabasev4"
)


@app.route('/',methods= ['GET','POST'])
def start_page():
    return render_template('index.html')

@app.route('/sign_up',methods = ['GET','POST'])
def sign_up():
    cursor = mydb.cursor(buffered=True)
    cursor.execute("SELECT name FROM School")
    school_names = cursor.fetchall()
    cursor.close()

    return render_template('sign_up.html',data = school_names)

if __name__ == "__main__":
    app.run(debug = True)


