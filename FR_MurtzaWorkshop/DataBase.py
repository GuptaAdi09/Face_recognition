import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime
import time
import json

cred = credentials.Certificate("ServiceAC.json")
firebase_admin.initialize_app(cred,{

    "databaseURL":"https://facerecognitionattendanc-b78e8-default-rtdb.firebaseio.com/",
     "storageBuket":"gs://facerecognitionattendanc-b78e8.appspot.com"
})

ref=db.reference("students")


data={
 "adi":{
     "Roll_No":1,
     "Class":"Ty_bscit",
     "FullName":"chandrabhan Gupta",
     "total_attendance":2,
     'Division':"B",
     'last_attendance_time':datetime.now().strftime("%Y-%m-%d %H:%M:%S")},"elon":{

     "Roll_No":2,
     "Class":"sy_bscit",
     "FullName":"Elon_musk",
     "total_attendance":10,
     'Division':"A",
     'last_attendance_time':datetime.now().strftime("%Y-%m-%d %H:%M:%S")
   },"pat":{
     "Roll_No":3,
     "Class":"Ty_bcom",
     "FullName":"Pat Cummins",
     "total_attendance":7,
     'Division':"A",
     'last_attendance_time':datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
        "virat":{
     "Roll_No":4,
     "Class":"Ty_bcom",
     "FullName":"Virat Kohli",
     "total_attendance":7,
     'Division':"C",
     'last_attendance_time':datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },"cr7":{
     "Roll_No":5,
     "Class":"Football",
     "FullName":"cristiano ronaldo",
     "total_attendance":7,
     'Division':"C",
     'last_attendance_time':datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },"rahul":{
     "Roll_No":4,
     "Class":"Tyit",
     "FullName":"Rahul Chauhan",
     "total_attendance":1,
     'Division':"Null",
     'last_attendance_time':datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    }


for key,value in data.items():
    ref.child(key).set(value)
