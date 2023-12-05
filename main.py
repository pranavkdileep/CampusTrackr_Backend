from typing import List  
from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel  
from dotenv import load_dotenv  
import os  
import MySQLdb  
import csv  
import uvicorn
import json
  
# load_dotenv()  
app = FastAPI()  
  

def get_db_connection():  
    connection = MySQLdb.connect(  
        host=os.getenv("DB_HOST"),  
        user=os.getenv("DB_USERNAME"),  
        passwd=os.getenv("DB_PASSWORD"),  
        db=os.getenv("DB_NAME"),  
        autocommit=True,  
        ssl_mode="VERIFY_IDENTITY",  
        ssl={  
            "ca": "/etc/ssl/certs/ca-certificates.crt"  
        }  
    )  
    return connection  
  

class Subject(BaseModel):
    subject_name: str

    
def get_db_cursor(connection):  
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)  
    return cursor

def get_all_subject():
    connection = get_db_connection()
    cursor = get_db_cursor(connection)
    cursor.execute("SELECT * FROM subjects")
    subjects = cursor.fetchall()
    return [subject['subject_name'] for subject in subjects]

@app.get('/getallsubjects')
async def get_all_subjects():
    subjects = get_all_subject()
    return subjects


@app.post('/addsubject')
async def add_subject(subject: Subject):
    connection = get_db_connection()
    cursor = get_db_cursor(connection)
    cursor.execute("INSERT INTO subjects (subject_name) VALUES (%s)", (subject.subject_name,))
    return {"subject_name": subject.subject_name}

@app.post('/removesubject')
async def remove_subject(subject: Subject):
    connection = get_db_connection()
    cursor = get_db_cursor(connection)
    subject_id = cursor.execute("SELECT subject_id FROM subjects WHERE subject_name = %s", (subject.subject_name,))
    if subject_id:
        subject_id = cursor.fetchone()['subject_id']
        cursor.execute("DELETE FROM subjects WHERE subject_id = %b", (subject_id,))
        cursor.execute("DELETE FROM students WHERE subject_id = %b", (subject_id,))
        cursor.execute("DELETE FROM subject_assignments WHERE subject_id = %b", (subject_id,))
        cursor.execute("DELETE FROM subject_attendance WHERE subject_id = %b", (subject_id,))
        cursor.execute("DELETE FROM subject_internals WHERE subject_id = %b", (subject_id,))
        print(subject_id)
        return {"subject_name": subject.subject_name}
    else:
        return {"subject_name": "Subject not found"}
#get student list by subject id SELECT * FROM students WHERE subject_id = 1; 
@app.get('/getstudentlist/{subject_id}')
async def get_student_list(subject_id: int):
    connection = get_db_connection()
    cursor = get_db_cursor(connection)
    cursor.execute("SELECT * FROM students WHERE subject_id = %s", (subject_id,))
    students = cursor.fetchall()
    return students





class Student(BaseModel):
    student_name: str
    subject_id: int

@app.post('/addstudent')
async def add_student(student: Student):
    connection = get_db_connection()
    cursor = get_db_cursor(connection)
    cursor.execute("INSERT INTO students (student_name, subject_id) VALUES (%s, %s)", (student.student_name, student.subject_id))
    connection.commit()
    return {"student_name": student.student_name, "subject_id": student.subject_id}

class DStudent(BaseModel):
    student_id: int

@app.post('/removestudent')
async def remove_student(student: DStudent):
    connection = get_db_connection()
    cursor = get_db_cursor(connection)
    tables = ['students', 'subject_assignments', 'subject_attendance', 'subject_internals']
    for table in tables:
        query = f"DELETE FROM `{table}` WHERE `student_id`=%s"
        cursor.execute(query, (student.student_id,))
    connection.commit()
    return {"id": student.student_id}

class Assignment(BaseModel):
    student_id: int
    marks_obtained: int
    subject_id: int
    assignment_number: int
    max_marks: int

class DAssignment(BaseModel):
    assignment_id: int

@app.post('/addassignment')
async def add_assignment(assignment: Assignment):
    connection = get_db_connection()
    cursor = get_db_cursor(connection)
    cursor.execute("INSERT INTO subject_assignments (student_id, marks_obtained, subject_id, assignment_number, max_marks) VALUES (%s, %s, %s, %s, %s)", (assignment.student_id, assignment.marks_obtained, assignment.subject_id, assignment.assignment_number, assignment.max_marks))
    connection.commit()
    return {"student_id": assignment.student_id, "marks_obtained": assignment.marks_obtained, "subject_id": assignment.subject_id, "assignment_number": assignment.assignment_number, "max_marks": assignment.max_marks}

@app.post('/removeassignment')
async def remove_assignment(assignment: DAssignment):
    connection = get_db_connection()
    cursor = get_db_cursor(connection)
    cursor.execute("DELETE FROM subject_assignments WHERE assignment_id = %s", (assignment.assignment_id,))
    connection.commit()
    return {"assignment_id": assignment.assignment_id}

class Attendance(BaseModel):
    student_id: int
    subject_id: int
    attendance_date: str
    is_present: bool
class DAttendance(BaseModel):
    attendance_id: int
@app.post('/addattendance')
async def add_attendance(attendance: Attendance):
    connection = get_db_connection()
    cursor = get_db_cursor(connection)
    cursor.execute("INSERT INTO subject_attendance (student_id, subject_id, attendance_date, is_present) VALUES (%s, %s, %s, %s)", (attendance.student_id, attendance.subject_id, attendance.attendance_date, attendance.is_present))
    connection.commit()
    return {"student_id": attendance.student_id, "subject_id": attendance.subject_id, "attendance_date": attendance.attendance_date, "is_present": attendance.is_present}
@app.post('/removeattendance')
async def remove_attendance(attendance: DAttendance):
    connection = get_db_connection()
    cursor = get_db_cursor(connection)
    cursor.execute("DELETE FROM subject_attendance WHERE attendance_id = %s", (attendance.attendance_id,))
    connection.commit()
    return {"attendance_id": attendance.attendance_id}

class Internal(BaseModel):
    student_id: int
    subject_id: int
    internal_number: int
    marks_obtained: int
    max_marks: int

class DInternal(BaseModel):
    internal_id: int

@app.post('/addinternal')
async def add_internal(internal: Internal):
    connection = get_db_connection()
    cursor = get_db_cursor(connection)
    cursor.execute("INSERT INTO subject_internals (student_id, subject_id, internal_number, marks_obtained, max_marks) VALUES (%s, %s, %s, %s, %s)", (internal.student_id, internal.subject_id, internal.internal_number, internal.marks_obtained, internal.max_marks))
    connection.commit()
    return {"student_id": internal.student_id, "subject_id": internal.subject_id, "internal_number": internal.internal_number, "marks_obtained": internal.marks_obtained, "max_marks": internal.max_marks}
@app.post('/removeinternal')
async def remove_internal(internal: DInternal):
    connection = get_db_connection()
    cursor = get_db_cursor(connection)
    cursor.execute("DELETE FROM subject_internals WHERE internal_id = %s", (internal.internal_id,))
    connection.commit()
    return {"internal_id": internal.internal_id}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
