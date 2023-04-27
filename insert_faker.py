from faker_data import school_provider,user_provider

from faker import Faker
from flask import Flask,make_response,request,render_template
from __init__ import app,mysql
from flask_mysqldb import MySQL
import mysql.connector as con
import random


mydb = con.connect(
host = "localhost",
user = "root",
password = "",
database = "schooldatabasev4"
)


fake = Faker('el_GR')

cursor = mydb.cursor(buffered = True)


#Βρίσκει τον αριθμό τον schools που υπάρχουν στο σύστημα 
def Number_of_Schools():
    cursor.execute('SELECT COUNT(*) FROM School')
    N = cursor.fetchall()[0][0]
    return N

#Προσθέτει στην βάση δεδομένων εναν συγκεκριμένο αριθμό σχολείων
def Insert_Schools(N_Schools):
    for i in range(N_Schools):
        school = school_provider(fake)
        try:
            cursor.execute('INSERT INTO School (name,city,email,address) VALUES ("{}","{}","{}","{}")'.format(school.get_name(),school.get_city(),school.get_email(),school.get_address()))
        except:
            print("probably duplicate entry")
        mydb.commit()

#Προσθέτει στην βάση δεδομένων έναν Admin για κάθε σχολείο
def Insert_Admins():
    N = Number_of_Schools()
    for i in range(N):
        user = user_provider(fake)
        school_id = cursor.execute('INSERT INTO App_user (school_id,admin_id,first_name,last_name,age,type,approved) VALUES(\
                                {},NULL,"{}","{}",{},"Admin",0)'.format(i+1,user.get_first_name(),user.get_last_name(),user.get_age()))
        mydb.commit()

#Προσθέτει στην βάση ένα συγκεκριμένο αριθμό App_user (Μαθητών ή Καθηγητών)
def Insert_Users(N_Users):
    cursor.execute('SELECT user_id FROM App_user WHERE App_user.type = "Admin" ORDER BY RAND()')
    admin_id = cursor.fetchall()[0][0]
    print(admin_id)
    N = Number_of_Schools()


    for i in range(N_Users):
        user = user_provider(fake)
        school_id = cursor.execute('INSERT INTO App_user (school_id,admin_id,first_name,last_name,age,type,approved) VALUES(\
                                {},{},"{}","{}",{},"{}",0)'.format(random.randint(1,N),admin_id,user.get_first_name(),\
                                user.get_last_name(),user.get_age(),user.get_type()))
        mydb.commit()

#Αδειάζει όλα τα δεδομένα όλων των πινάκων της βάσης
def Empty_Tables():
    try:
        sql_file = open("sql_schemas/drop_schema.sql")  
    except:
        print("hello world")
    sql_string = sql_file.read().split(';')
    for row in sql_string:
        try:
            if(row[0] == '\n'):
                cursor.execute(row[1:])
            else:
                cursor.execute(row)
        except:
            print("error")

#Συνδιάζει τις παραπάνω συναρτήσεις
def create_objects(N_Schools,N_Users):
    Empty_Tables()
    Insert_Schools(N_Schools)
    Insert_Admins()
    Insert_Users(N_Users)

create_objects(10,10)

#Για να τρέξουμε ξεχωριστά τις συναρτήσεις πρέπει να το κάνουμε ακολουθώντας την συγκεκριμένη σειρά που φαίνεται παραπάνω






