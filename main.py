from typing import List  
from fastapi import FastAPI, HTTPException, File, UploadFile  
from pydantic import BaseModel  
from dotenv import load_dotenv  
import os  
import MySQLdb  
import csv  
  
load_dotenv()  
app = FastAPI()  
  
# Establish a connection to the database  
def get_db_connection():  
    connection = MySQLdb.connect(  
        host=os.getenv("DB_HOST"),  
        user=os.getenv("DB_USERNAME"),  
        passwd=os.getenv("DB_PASSWORD"),  
        db=os.getenv("DB_NAME"),  
        autocommit=True,  
        ssl_mode="VERIFY_IDENTITY",  
        ssl={  
            "ca": "/etc/ssl/cert.pem"  
        }  
    )  
    return connection  
  
class Student(BaseModel):  
    name: str
  
class Subject(BaseModel):  
    subject_name: str 
  
class InternalMark(BaseModel):  
    subject_id: int  
    student_id: int  
    internal_number: int  
    marks_obtained: float  
    max_marks: float  
  
class AssignmentMark(BaseModel):  
    subject_id: int  
    student_id: int  
    assignment_number: int  
    marks_obtained: float  
    max_marks: float  
  
class AttendanceRecord(BaseModel):  
    subject_id: int  
    student_id: int  
    date: str  
    status: str  
  
@app.post("/add-student/")  
def add_student(student: Student):  
    connection = get_db_connection()  
    try:  
        with connection.cursor() as cursor:  
            cursor.execute(  
                "INSERT INTO Students (first_name, last_name, email, enrollment_number) VALUES (%s, %s, %s, %s)",  
                (student.first_name, student.last_name, student.email, student.enrollment_number)  
            )  
        return {"message": "Student added successfully"}  
    finally:  
        connection.close()  
  
@app.delete("/remove-student/{student_id}")  
def remove_student(student_id: int):  
    connection = get_db_connection()  
    try:  
        with connection.cursor() as cursor:  
            cursor.execute("DELETE FROM Students WHERE student_id = %s", (student_id,))  
        return {"message": "Student removed successfully"}  
    finally:  
        connection.close()  

# ... [previous code]  
  
# Endpoint to get a list of subjects  
@app.get("/subjects", response_model=List[Subject])  
def get_subjects():  
    connection = get_db_connection()  
    try:  
        with connection.cursor() as cursor:  
            cursor.execute("SELECT subject_code, subject_name, credit FROM Subjects")  
            subjects_data = cursor.fetchall()  
            subjects = [Subject(subject_code=row[0], subject_name=row[1], credit=row[2]) for row in subjects_data]  
            return subjects  
    finally:  
        connection.close()  
  
# Endpoint to get a list of students by subject ID  
@app.get("/students/{subject_id}", response_model=List[Student])  
def get_students_by_subject(subject_id: int):  
    connection = get_db_connection()  
    try:  
        with connection.cursor() as cursor:  
            # Assuming there's a junction table 'SubjectStudents' that links students to subjects  
            cursor.execute(  
                "SELECT s.first_name, s.last_name, s.email, s.enrollment_number "  
                "FROM Students s "  
                "JOIN SubjectStudents ss ON s.student_id = ss.student_id "  
                "WHERE ss.subject_id = %s", (subject_id,)  
            )  
            students_data = cursor.fetchall()  
            students = [Student(first_name=row[0], last_name=row[1], email=row[2], enrollment_number=row[3]) for row in students_data]  
            return students  
    finally:  
        connection.close()  
  
# ... [rest of the code]  

# Add similar endpoints for add_subject, remove_subject, add_internal_mark, remove_internal_mark, add_assignment_mark, remove_assignment, add_attendance, remove_attendance  
  
@app.get("/download-subject-data/{subject_id}")  
def download_subject_data(subject_id: int):  
    connection = get_db_connection()  
    try:  
        with connection.cursor() as cursor:  
            cursor.execute(  
                "SELECT student_id, COUNT(case when status = 'Present' then 1 end) as present_count, COUNT(*) as total_count "  
                "FROM Attendance WHERE subject_id = %s GROUP BY student_id", (subject_id,)  
            )  
            result = cursor.fetchall()  
  
            # Process result to calculate percentage  
            processed_data = []  
            for row in result:  
                student_id = row[0]  
                present_count = row[1]  
                total_count = row[2]  
                attendance_percentage = (present_count / total_count) * 100  
                processed_data.append([student_id, attendance_percentage])  
  
            # Write processed data to CSV file  
            with open(f'subject_{subject_id}_data.csv', 'w', newline='') as file:  
                writer = csv.writer(file)  
                writer.writerow(['Student ID', 'Attendance Percentage'])  
                writer.writerows(processed_data)  
  
            return File(f'subject_{subject_id}_data.csv')  
    finally:  
        connection.close()  
  
# Run the app with: uvicorn main:app --reload  
