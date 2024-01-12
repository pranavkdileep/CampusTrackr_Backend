from typing import List  
from fastapi import FastAPI, HTTPException, File, UploadFile, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials  
from pydantic import BaseModel  
from dotenv import load_dotenv  
from datetime import datetime
import os  
import MySQLdb  
import csv  
import uvicorn
import json

load_dotenv()  
app = FastAPI()  
  

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    correct_token = os.getenv("TOKEN")
    if credentials.credentials != correct_token:
        raise HTTPException(status_code=403, detail="Invalid authorization token")
    return credentials.credentials

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

class Dsubject(BaseModel):
    subject_id: int

    
def get_db_cursor(connection):  
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)  
    return cursor

def get_all_subject():
    connection = get_db_connection()
    cursor = get_db_cursor(connection)
    cursor.execute("SELECT * FROM subjects")
    subjects = cursor.fetchall()
    return subjects

@app.get('/getallsubjects')
async def get_all_subjects():
    subjects = get_all_subject()
    return subjects


@app.post('/addsubject')
async def add_subject(subject: Subject,token: str = Depends(get_current_user)):
    connection = get_db_connection()
    cursor = get_db_cursor(connection)
    cursor.execute("INSERT INTO subjects (subject_name) VALUES (%s)", (subject.subject_name,))
    return {"subject_name": subject.subject_name}

@app.post('/removesubject')
async def remove_subject(subject: Dsubject, token: str = Depends(get_current_user)):
    subject_id = subject.subject_id
    print(subject_id)
    connection = get_db_connection()
    cursor = get_db_cursor(connection)
    tables = ['subjects','students', 'subject_assignments', 'subject_attendance', 'subject_internals']
    for table in tables:
        query = f"DELETE FROM `{table}` WHERE `subject_id`=%s"
        cursor.execute(query, (subject_id,))
    connection.commit()
    return {"subject_id": subject_id}

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
async def add_student(student: Student,token: str = Depends(get_current_user)):
    connection = get_db_connection()
    cursor = get_db_cursor(connection)
    cursor.execute("INSERT INTO students (student_name, subject_id) VALUES (%s, %s)", (student.student_name, student.subject_id))
    connection.commit()
    return {"student_name": student.student_name, "subject_id": student.subject_id}

class DStudent(BaseModel):
    student_id: int

@app.post('/removestudent')
async def remove_student(student: DStudent,token: str = Depends(get_current_user)):
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
async def add_assignment(assignment: Assignment,token: str = Depends(get_current_user)):
    connection = get_db_connection()
    cursor = get_db_cursor(connection)
    cursor.execute("INSERT INTO subject_assignments (student_id, marks_obtained, subject_id, assignment_number, max_marks) VALUES (%s, %s, %s, %s, %s)", (assignment.student_id, assignment.marks_obtained, assignment.subject_id, assignment.assignment_number, assignment.max_marks))
    connection.commit()
    return {"student_id": assignment.student_id, "marks_obtained": assignment.marks_obtained, "subject_id": assignment.subject_id, "assignment_number": assignment.assignment_number, "max_marks": assignment.max_marks}

@app.post('/removeassignment')
async def remove_assignment(assignment: DAssignment,token: str = Depends(get_current_user)):
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
async def add_attendance(attendance: Attendance,token: str = Depends(get_current_user)):
    connection = get_db_connection()
    cursor = get_db_cursor(connection)
    cursor.execute("INSERT INTO subject_attendance (student_id, subject_id, attendance_date, is_present) VALUES (%s, %s, %s, %s)", (attendance.student_id, attendance.subject_id, attendance.attendance_date, attendance.is_present))
    connection.commit()
    return {"student_id": attendance.student_id, "subject_id": attendance.subject_id, "attendance_date": attendance.attendance_date, "is_present": attendance.is_present}
@app.post('/removeattendance')
async def remove_attendance(attendance: DAttendance,token: str = Depends(get_current_user)):
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
async def add_internal(internal: Internal,token: str = Depends(get_current_user)):
    connection = get_db_connection()
    cursor = get_db_cursor(connection)
    cursor.execute("INSERT INTO subject_internals (student_id, subject_id, internal_number, marks_obtained, max_marks) VALUES (%s, %s, %s, %s, %s)", (internal.student_id, internal.subject_id, internal.internal_number, internal.marks_obtained, internal.max_marks))
    connection.commit()
    return {"student_id": internal.student_id, "subject_id": internal.subject_id, "internal_number": internal.internal_number, "marks_obtained": internal.marks_obtained, "max_marks": internal.max_marks}
@app.post('/removeinternal')
async def remove_internal(internal: DInternal,token: str = Depends(get_current_user)):
    connection = get_db_connection()
    cursor = get_db_cursor(connection)
    cursor.execute("DELETE FROM subject_internals WHERE internal_id = %s", (internal.internal_id,))
    connection.commit()
    return {"internal_id": internal.internal_id}

class Performance(BaseModel):
    student_id: int
    student_name: str
    total_lectures: int
    lectures_present: int
    attendance_percentage: float
    average_internal_marks: float


@app.get('/getperformance/{subject_id}', response_model=List[Performance])
async def get_performance(subject_id: int):
    connection = get_db_connection()
    cursor = get_db_cursor(connection)
    cursor.execute("SELECT * FROM students WHERE subject_id = %s", (subject_id,))
    students = cursor.fetchall()
    performance = []
    for student in students:
        student_id = student['student_id']
        student_name = student['student_name']

        cursor.execute("SELECT COUNT(*) AS total FROM subject_attendance WHERE student_id = %s AND subject_id = %s", (student_id, subject_id))
        total_lectures = cursor.fetchone()['total']

        cursor.execute("SELECT COUNT(*) AS present FROM subject_attendance WHERE student_id = %s AND subject_id = %s AND is_present = 1", (student_id, subject_id))
        lectures_present = cursor.fetchone()['present']

        attendance_percentage = (lectures_present / total_lectures) * 100 if total_lectures > 0 else 0

        cursor.execute("SELECT AVG(marks_obtained) AS average FROM subject_internals WHERE student_id = %s AND subject_id = %s", (student_id, subject_id))
        average_internal_marks_row = cursor.fetchone()
        average_internal_marks = average_internal_marks_row['average'] if average_internal_marks_row['average'] is not None else 0.0

        performance.append(Performance(student_id=student_id, student_name=student_name, total_lectures=total_lectures, lectures_present=lectures_present, attendance_percentage=attendance_percentage, average_internal_marks=average_internal_marks))
    return performance

class AttendanceM(BaseModel):
    student_id: int
    present: bool

class BulkAttendance(BaseModel):
    subject_id: int
    date: str
    bulk_attendance: List[AttendanceM]


@app.post('/addbulkattendance')
async def bulk_attendance(bulk_attendanceb: BulkAttendance, token: str = Depends(get_current_user)):
    connection = get_db_connection()
    cursor = get_db_cursor(connection)
    date_str = bulk_attendanceb.date
    date_obj = datetime.strptime(date_str, '%m/%d/%Y')
    formatted_date = date_obj.strftime('%Y-%m-%d')
    for attendance in bulk_attendanceb.bulk_attendance:
        query = "INSERT INTO subject_attendance (subject_id, attendance_date, student_id, is_present) VALUES (%s, %s, %s, %s)"
        values = (bulk_attendanceb.subject_id, formatted_date, attendance.student_id, attendance.present)
        cursor.execute(query, values)
    
    connection.commit()
class Getattendance(BaseModel):
    studentId: int
    studentName: str
    date: str
    AttandanceId: int
    present : bool

@app.get('/getattendance/{student_id}', response_model=List[Getattendance])
async def get_bulk_attendance(student_id: int):
    connection = get_db_connection()
    cursor = get_db_cursor(connection)
    cursor.execute("SELECT * FROM subject_attendance WHERE student_id = %s", (student_id,))
    attendance = cursor.fetchall()
    attendance_list = []
    for attend in attendance:
        student_id = attend['student_id']
        student_name = 'pkd'
        date = attend['attendance_date']
        attendance_id = attend['attendance_id']
        present = attend['is_present']
        attendance_list.append(Getattendance(studentId=student_id, studentName=student_name, date=str(date), AttandanceId=attendance_id, present=present))
    return attendance_list

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
