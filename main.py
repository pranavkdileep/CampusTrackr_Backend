from flask import Flask, request, jsonify  
import MySQLdb  
import os  
  
app = Flask(__name__)  
  
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
  
@app.route('/subjects', methods=['GET', 'POST'])  
def manage_subjects():  
    conn = get_db_connection()  
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)  
      
    if request.method == 'GET':  
        cursor.execute('SELECT * FROM subjects')  
        subjects = cursor.fetchall()  
        return jsonify(subjects)  
      
    if request.method == 'POST':  
        new_subject = request.json['subject_name']  
        cursor.execute('INSERT INTO subjects (subject_name) VALUES (%s)', (new_subject,))  
        conn.commit()  
        return jsonify({"message": "Subject added successfully"}), 201  
  
@app.route('/students', methods=['GET', 'POST'])  
def manage_students():  
    conn = get_db_connection()  
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)  
      
    if request.method == 'GET':  
        cursor.execute('SELECT * FROM students')  
        students = cursor.fetchall()  
        return jsonify(students)  
      
    if request.method == 'POST':  
        new_student = request.json['student_name']  
        subject_id = request.json['subject_id']  
        cursor.execute('INSERT INTO students (student_name, subject_id) VALUES (%s, %s)', (new_student, subject_id))  
        conn.commit()  
        return jsonify({"message": "Student added successfully"}), 201  
  
@app.route('/attendance', methods=['POST'])  
def mark_attendance():  
    conn = get_db_connection()  
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)  
      
    subject_id = request.json['subject_id']  
    student_id = request.json['student_id']  
    attendance_date = request.json['attendance_date']  
    is_present = request.json['is_present']  
      
    cursor.execute('INSERT INTO subject_attendance (subject_id, student_id, attendance_date, is_present) VALUES (%s, %s, %s, %s)',  
                   (subject_id, student_id, attendance_date, is_present))  
    conn.commit()  
    return jsonify({"message": "Attendance marked successfully"}), 201  
  
@app.route('/internals', methods=['POST'])  
def mark_internals():  
    conn = get_db_connection()  
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)  
      
    subject_id = request.json['subject_id']  
    student_id = request.json['student_id']  
    internal_number = request.json['internal_number']  
    marks_obtained = request.json['marks_obtained']  
    max_marks = request.json['max_marks']  
      
    cursor.execute('INSERT INTO subject_internals (subject_id, student_id, internal_number, marks_obtained, max_marks) VALUES (%s, %s, %s, %s, %s)',  
                   (subject_id, student_id, internal_number, marks_obtained, max_marks))  
    conn.commit()  
    return jsonify({"message": "Internal marks added successfully"}), 201  
  
@app.route('/assignments', methods=['POST'])  
def mark_assignments():  
    conn = get_db_connection()  
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)  
      
    subject_id = request.json['subject_id']  
    student_id = request.json['student_id']  
    assignment_number = request.json['assignment_number']  
    marks_obtained = request.json['marks_obtained']  
    max_marks = request.json['max_marks']  
      
    cursor.execute('INSERT INTO subject_assignments (subject_id, student_id, assignment_number, marks_obtained, max_marks) VALUES (%s, %s, %s, %s, %s)',  
                   (subject_id, student_id, assignment_number, marks_obtained, max_marks))  
    conn.commit()  
    return jsonify({"message": "Assignment marks added successfully"}), 201  
  
if __name__ == '__main__':  
    app.run(debug=True)  
