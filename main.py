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
import pandas as pd
import io

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
@app.get('/getperformance_dumy/{subject_id}', response_model=List[Performance])
async def get_performance_dumy(subject_id: int):
    # only send student id and name, others are demy costant value 0
    connection = get_db_connection()
    cursor = get_db_cursor(connection)
    cursor.execute("SELECT * FROM students WHERE subject_id = %s", (subject_id,))
    students = cursor.fetchall()
    performance = []
    for student in students:
        student_id = student['student_id']
        student_name = student['student_name']
        performance.append(Performance(student_id=student_id, student_name=student_name, total_lectures=0, lectures_present=0, attendance_percentage=0, average_internal_marks=0))
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
    cursor.execute("SELECT student_name FROM students WHERE student_id = %s", (student_id,))
    student_name = cursor.fetchone()['student_name']
    attendance_list = []
    for attend in attendance:
        student_id = attend['student_id']
        student_name = student_name
        date = attend['attendance_date']
        attendance_id = attend['attendance_id']
        present = attend['is_present']
        attendance_list.append(Getattendance(studentId=student_id, studentName=student_name, date=str(date), AttandanceId=attendance_id, present=present))
    return attendance_list

class UpdateAttendance(BaseModel):
    attendance_id: int
    present: bool

@app.post('/updateattendance')
async def update_attendance(attendance: UpdateAttendance, token: str = Depends(get_current_user)):
    connection = get_db_connection()
    cursor = get_db_cursor(connection)
    cursor.execute("UPDATE subject_attendance SET is_present = %s WHERE attendance_id = %s", (attendance.present, attendance.attendance_id))
    connection.commit()
    return {"attendance_id": attendance.attendance_id, "present": attendance.present}

class internalStudentList(BaseModel):
    student_id: int
    marks_obtained: int

class BulkInternal(BaseModel):
    subject_id: int
    internal_number: int
    max_marks: int
    bulk_internal: List[internalStudentList]

@app.post('/addbulkinternal')
async def bulk_internal(bulk_internalb: BulkInternal, token: str = Depends(get_current_user)):
    connection = get_db_connection()
    cursor = get_db_cursor(connection)
    for internal in bulk_internalb.bulk_internal:
        query = "INSERT INTO subject_internals (subject_id, internal_number, student_id, marks_obtained, max_marks) VALUES (%s, %s, %s, %s, %s)"
        values = (bulk_internalb.subject_id, bulk_internalb.internal_number, internal.student_id, internal.marks_obtained, bulk_internalb.max_marks)
        cursor.execute(query, values)
    
    connection.commit()
    return {"subject_id": bulk_internalb.subject_id, "internal_number": bulk_internalb.internal_number, "max_marks": bulk_internalb.max_marks}
class ListInternal(BaseModel):
    student_id: int
    student_name: str
    marks_obtained: int
    max_marks: int
    internal_id: int
@app.get('/getinternal/{subject_id}/{internal_number}', response_model=List[ListInternal])
async def get_bulk_internal(subject_id: int, internal_number: int):
    connection = get_db_connection()
    cursor = get_db_cursor(connection)
    cursor.execute("SELECT * FROM subject_internals WHERE subject_id = %s AND internal_number = %s", (subject_id, internal_number))
    internal = cursor.fetchall()
    internal_list = []
    for intern in internal:
        student_id = intern['student_id']
        cursor.execute("SELECT student_name FROM students WHERE student_id = %s", (student_id,))
        student_name = cursor.fetchone()['student_name']
        marks_obtained = intern['marks_obtained']
        max_marks = intern['max_marks']
        internal_id = intern['internal_id']
        internal_list.append(ListInternal(student_id=student_id, student_name=student_name, marks_obtained=marks_obtained, max_marks=max_marks, internal_id=internal_id))
    return internal_list

class UpdateInternal(BaseModel):
    internal_id: int
    marks_obtained: int

@app.post('/updateinternal')
async def update_internal(internal: UpdateInternal, token: str = Depends(get_current_user)):
    connection = get_db_connection()
    cursor = get_db_cursor(connection)
    cursor.execute("UPDATE subject_internals SET marks_obtained = %s WHERE internal_id = %s", (internal.marks_obtained, internal.internal_id))
    connection.commit()
    return {"internal_id": internal.internal_id, "marks_obtained": internal.marks_obtained}

class AssignmentStudentList(BaseModel):
    student_id: int
    student_name: str
    marks_obtained: int
    max_marks: int
    assignment_id: int
@app.get('/getassignment/{subject_id}/{assignment_number}', response_model=List[AssignmentStudentList])
async def get_bulk_assignment(subject_id: int, assignment_number: int):
    connection = get_db_connection()
    cursor = get_db_cursor(connection)
    cursor.execute("SELECT * FROM subject_assignments WHERE subject_id = %s AND assignment_number = %s", (subject_id, assignment_number))
    assignment = cursor.fetchall()
    assignment_list = []
    for assign in assignment:
        student_id = assign['student_id']
        cursor.execute("SELECT student_name FROM students WHERE student_id = %s", (student_id,))
        student_name = cursor.fetchone()['student_name']
        marks_obtained = assign['marks_obtained']
        max_marks = assign['max_marks']
        assignment_id = assign['assignment_id']
        assignment_list.append(AssignmentStudentList(student_id=student_id, student_name=student_name, marks_obtained=marks_obtained, max_marks=max_marks, assignment_id=assignment_id))
    return assignment_list
class BulkAssignment(BaseModel):
    student_id: int
    marks_obtained: int
class BulkAssignmentAdd(BaseModel):
    subject_id: int
    assignment_number: int
    max_marks: int
    bulk_assignment: List[BulkAssignment]
@app.post('/addbulkassignment')
async def bulk_assignment(bulk_assignmentb: BulkAssignmentAdd, token: str = Depends(get_current_user)):
    connection = get_db_connection()
    cursor = get_db_cursor(connection)
    for assignment in bulk_assignmentb.bulk_assignment:
        query = "INSERT INTO subject_assignments (subject_id, student_id, assignment_number, marks_obtained, max_marks) VALUES (%s, %s, %s, %s, %s)"
        values = (bulk_assignmentb.subject_id, assignment.student_id, bulk_assignmentb.assignment_number, assignment.marks_obtained, bulk_assignmentb.max_marks)
        cursor.execute(query, values)
    
    connection.commit()
    return {"subject_id": bulk_assignmentb.subject_id, "assignment_number": bulk_assignmentb.assignment_number, "max_marks": bulk_assignmentb.max_marks}
class updateAssignment(BaseModel):
    assignment_id: int
    marks_obtained: int
@app.post('/updateassignment')
async def update_assignment(assignment: updateAssignment, token: str = Depends(get_current_user)):
    connection = get_db_connection()
    cursor = get_db_cursor(connection)
    cursor.execute("UPDATE subject_assignments SET marks_obtained = %s WHERE assignment_id = %s", (assignment.marks_obtained, assignment.assignment_id))
    connection.commit()
    return {"assignment_id": assignment.assignment_id, "marks_obtained": assignment.marks_obtained}

@app.post('/uploadstudentslist/{subject_id}')
async def upload_students_list(subject_id: int, file: UploadFile = File(...), token: str = Depends(get_current_user)):
    file_bytes = await file.read()
    file_extension = file.filename.split('.')[-1]

    if file_extension == 'xlsx':
        df = pd.read_excel(io.BytesIO(file_bytes))
    elif file_extension == 'csv':
        df = pd.read_csv(io.StringIO(file_bytes.decode('utf-8')))
    else:
        return {"error": "Invalid file format"}

    connection = get_db_connection()
    cursor = get_db_cursor(connection)
    for index, row in df.iterrows():
        cursor.execute("INSERT INTO students (student_name, subject_id) VALUES (%s, %s)", (row['student_name'], subject_id))
    connection.commit()
    return {"subject_id": subject_id}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
