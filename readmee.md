Sure, to implement an application that allows college staff to mark students' attendance, internal exam marks, and assignment marks, you will need to structure your MySQL database with appropriate tables and relationships. Here are the steps and MySQL commands to set up the database:  
   
1. Create a database for your college application:  
   
```sql  
CREATE DATABASE college_management;  
```  
   
2. Select the created database to use:  
   
```sql  
USE college_management;  
```  
   
3. Create tables for your application. You will need tables for subjects, students, attendance, internals, and assignments:  
   
```sql  
-- Table for subjects  
CREATE TABLE subjects (  
    subject_id INT AUTO_INCREMENT PRIMARY KEY,  
    subject_name VARCHAR(100) NOT NULL,
    facultie_id INT
);  
   
-- Table for students  
CREATE TABLE students (  
    student_id INT AUTO_INCREMENT PRIMARY KEY,  
    student_name VARCHAR(100) NOT NULL,
    subject_id INT
);
-- Table for Facultie
CREATE TABLE faculties (  
    facultie_id INT AUTO_INCREMENT PRIMARY KEY,  
    facultie_name VARCHAR(100) NOT NULL,
    facultie_password VARCHAR(100) NOT NULL
);
   
-- Table for subject attendance  
CREATE TABLE subject_attendance (  
    attendance_id INT AUTO_INCREMENT PRIMARY KEY,  
    subject_id INT,  
    student_id INT,  
    attendance_date DATE,  
    is_present BOOLEAN 
);  
   
-- Table for internals  
CREATE TABLE subject_internals (  
    internal_id INT AUTO_INCREMENT PRIMARY KEY,  
    subject_id INT,  
    student_id INT,  
    internal_number INT,  
    marks_obtained DECIMAL(5,2),  
    max_marks DECIMAL(5,2),  
    UNIQUE(subject_id,internal_number)  
);  
   
-- Table for assignments  
CREATE TABLE subject_assignments (  
    assignment_id INT AUTO_INCREMENT PRIMARY KEY,  
    subject_id INT,  
    student_id INT,  
    assignment_number INT,  
    marks_obtained DECIMAL(5,2),  
    max_marks DECIMAL(5,2)
);  
```  
   
4. To add new subjects, students, and their data:  
   
```sql  
-- Adding a new subject  
INSERT INTO subjects (subject_name) VALUES ('Calculus');  
   
-- Adding a new student  
INSERT INTO students (student_name,subject_id) VALUES ('John Doe',1);  
   
-- Marking attendance for a student  
INSERT INTO subject_attendance (subject_id, student_id, attendance_date, is_present) VALUES (1, 1, '2021-09-01', TRUE);  
   
-- Adding internal exam marks for a student  
INSERT INTO subject_internals (subject_id, student_id, internal_number, marks_obtained, max_marks) VALUES (1, 1, 1, 85, 100);  
   
-- Adding assignment marks for a student  
INSERT INTO subject_assignments (subject_id, student_id, assignment_number, marks_obtained, max_marks) VALUES (1, 1, 1, 90, 100);  
```  
   
5. To remove subjects or students:  
   
```sql  
-- Deleting a subject  
DELETE FROM subjects WHERE subject_id = 1;  
   
-- Deleting a student  
DELETE FROM students WHERE student_id = 1;  
```  
   
6. To update data in case of errors or changes:  
   
```sql  
-- Updating a student's name  
UPDATE students SET student_name = 'Jane Doe' WHERE student_id = 1;  
   
-- Updating internal marks  
UPDATE subject_internals SET marks_obtained = 88 WHERE internal_id = 1;  
   
-- Updating assignment marks  
UPDATE subject_assignments SET marks_obtained = 92 WHERE assignment_id = 1;  
```  
   
Make sure to adjust the `subject_id`, `student_id`, `internal_number`, `assignment_number`, and dates according to your actual data. Additionally, consider implementing constraints and indexes for better data integrity and query performance.  
   
Keep in mind that these are just basic commands to get you started. You would likely need to expand upon these with additional features such as user authentication, role-based access, and a user interface for the college staff to interact with the system.


To retrieve and display data from your MySQL database, you can use the `SELECT` statement. Below are some examples of how to use the `SELECT` statement to show data for different scenarios in your college management application:  
   
1. To show all subjects:  
   
```sql  
SELECT * FROM subjects;  
```  
   
2. To show all students:  
   
```sql  
SELECT * FROM students;  
```  
   
3. To show a specific student's attendance:  
   
```sql  
SELECT sa.attendance_date, sa.is_present, s.subject_name  
FROM subject_attendance sa  
JOIN subjects s ON sa.subject_id = s.subject_id  
WHERE sa.student_id = 1;  -- Replace 1 with the actual student_id  
```  
   
4. To show internal marks for a specific subject:  
   
```sql  
SELECT si.internal_number, si.marks_obtained, si.max_marks, st.student_name  
FROM subject_internals si  
JOIN students st ON si.student_id = st.student_id  
WHERE si.subject_id = 1;  -- Replace 1 with the actual subject_id  
```  
   
5. To show assignment marks for all students in a particular subject:  
   
```sql  
SELECT sa.assignment_number, sa.marks_obtained, sa.max_marks, st.student_name  
FROM subject_assignments sa  
JOIN students st ON sa.student_id = st.student_id  
WHERE sa.subject_id = 1;  -- Replace 1 with the actual subject_id  
```  
   
6. To show the overall performance of a student across all subjects:  
   
```sql  
-- For internals  
SELECT s.subject_name, AVG(si.marks_obtained) AS average_internal_marks  
FROM subject_internals si  
JOIN subjects s ON si.subject_id = s.subject_id  
WHERE si.student_id = 1  -- Replace 1 with the actual student_id  
GROUP BY si.subject_id;  
   
-- For assignments  
SELECT s.subject_name, AVG(sa.marks_obtained) AS average_assignment_marks  
FROM subject_assignments sa  
JOIN subjects s ON sa.subject_id = s.subject_id  
WHERE sa.student_id = 1  -- Replace 1 with the actual student_id  
GROUP BY sa.subject_id;  
```  
   
7. To show the attendance percentage of each student for a specific subject:  
   
```sql  
SELECT st.student_name,   
       (SUM(CASE WHEN sa.is_present THEN 1 ELSE 0 END) / COUNT(sa.attendance_id)) * 100 AS attendance_percentage  
FROM subject_attendance sa  
JOIN students st ON sa.student_id = st.student_id  
WHERE sa.subject_id = 1  -- Replace 1 with the actual subject_id  
GROUP BY sa.student_id;  
```  
   
These commands provide a starting point for viewing the data within your application. You'll likely need to tailor these queries to fit the specific requirements of your application and the reports you wish to generate.
