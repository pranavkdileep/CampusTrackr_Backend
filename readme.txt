Write a secure (connection using secure key) Python Fast API to perform the operations. Add subjects, add student, remove and delete that student data, add new internal exam mark, remove internal exams, add new assignment mark, remove assignment, add new attendance, remove attendance,download prosessed(show attantance as persentage) data of each subjects as csv. Note : python library to connect SQL is mysqlclient here is the example code to connect database :python 
from dotenv import load_dotenv
load_dotenv()
import os
import MySQLdb

connection = MySQLdb.connect(
  host= os.getenv("DB_HOST"),
  user=os.getenv("DB_USERNAME"),
  passwd= os.getenv("DB_PASSWORD"),
  db= os.getenv("DB_NAME"),
  autocommit = True,
  ssl_mode = "VERIFY_IDENTITY",
  ssl      = {
    "ca": "/etc/ssl/cert.pem"
  }
)
  


hello i need to develop a application for my collage staff to mark students attendance internal exam mark and assignment mark,the primary structure will be subject_attandecse subject_internals subject_assignments, so how can I implement it using MySQL,write all possible my SQL commadas,I can add and remove subs,students data ,ther are multiple internals and multiple assisgments

