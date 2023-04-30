import requests
from flask import Flask,make_response,request,render_template
from flask_mysqldb import MySQL
import mysql.connector as con
import random
import json

mydb = con.connect(
host = "localhost",
user = "root",
password = "",
database = "schooldatabasev4"
)

cursor = mydb.cursor(buffered = True)

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def Insert_Books(isbn,page_count,publisher,title,summary,s_cover_path,m_cover_path):
        try:
            cursor.execute('INSERT INTO Books (isbn,page_count,publisher,title,summary,cover_path) VALUES ({},{},"{}","{}","{}","{}")'\
                    .format(int(isbn),page_count,publisher[0],title,summary[:699],s_cover_path,m_cover_path))
            mydb.commit()
        except:
            print("error in book insert")

def Insert_Stores(isbn):
    try:
        cursor.execute('SELECT school_id FROM School ORDER BY RAND()')
        school_id = cursor.fetchall()[0][0]
        copies = random.randint(0,20)
        cursor.execute('INSERT INTO Stores (isbn,school_id,copies) VALUES ({},{},{})'.format(isbn,school_id,copies))
        mydb.commit()
    except:
        print("error in store insert")

def Insert_Categories(isbn,Categories):
    try:
        cursor.execute('INSERT INTO Categories (isbn,category) VALUES ({},"{}")'.format(isbn,Categories))
        mydb.commit()
    except:
        print("error in category insert")

def Insert_Keywords(isbn,keyword):
    for i in range(len(keyword)):
        try:
            cursor.execute('INSERT INTO Keywords (isbn,keyword) VALUES ({},"{}")'.format(isbn,keyword[i]))
            mydb.commit()
        except:
            print("error in keyword insert")

def Insert_Authors(isbn,author):
    try:
        full_name = author.split(' ')
        first_name =""
        last_name = ""
        if len(full_name) == 1:
            first_name = full_name[0]
        else:
            first_name = full_name[0]
            last_name = full_name[1]
        cursor.execute('INSERT INTO Authors (isbn,first_name,last_name) VALUES ({},"{}","{}")'.format(isbn,first_name,last_name))
        mydb.commit()
    except:
        print("error in author insert")



No_of_books = 100
response = requests.get('https://openlibrary.org/subjects/juvenile_literature.json?limit={}'.format(No_of_books))
data = response.json()

for i in range(No_of_books):
    try:
        categories = data['name']
        author = data['works'][i]['authors'][0]['name']
        olid_id = data['works'][i]['availability']['openlibrary_edition']
        print("ID = ",olid_id)
        works_di = data['works'][i]['key']
        response_works = requests.get("https://openlibrary.org{}.json".format(works_di))
        response_id = requests.get("https://openlibrary.org/books/{}.json".format(olid_id))
        response_id_json = response_id.json()
        response_works_json = response_works.json()
        try:
            title = response_id_json['title']
        except:
            print("no title found")
        try:
            publishers = response_id_json['publishers']
        except:
            publishers = "no publisher found"
        try:
            page_count = response_id_json['number_of_pages']
        except:
            print("no number of pages found")
        try:
            s_cover_path = "https://covers.openlibrary.org/b/OLID/{}-S.jpg".format(data['works'][i]['cover_edition_key'])
            m_cover_path = "https://covers.openlibrary.org/b/OLID/{}-M.jpg".format(data['works'][i]['cover_edition_key'])
            #print("https://covers.openlibrary.org/b/OLID/{}-L.jpg".format(data['works'][i]['cover_edition_key']))
        except:
            s_cover_path = "no small cover url found"
            m_cover_path = "no medium cover url found"
        try:
            summary = response_works_json['description'][:699]
        except:
            summary = "no description found"
        try:
            subjects = response_works_json['subjects'][:10]
        except:
            print("no subjects found")
        #categories , author, olid_id[2:len(olid_id)-1],title, publishers, page_count, cover_url, m_cover_url, summary, subjects
        try:
            Insert_Books(olid_id[2:len(olid_id)-1],page_count,publishers,title,summary,s_cover_path,m_cover_path)
        except:
            pass
        try:
            Insert_Stores(olid_id[2:len(olid_id)-1])
        except:
            pass
        try:
            Insert_Categories(olid_id[2:len(olid_id)-1],categories)
        except:
            pass
        try:
            Insert_Keywords(olid_id[2:len(olid_id)-1],subjects)
        except:
            pass
        try:
            Insert_Authors(olid_id[2:len(olid_id)-1],author)
        except:
            pass
        print("\n")
    except:
        pass

print("END OF PROGRAMM")
cursor.close()
