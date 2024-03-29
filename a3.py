import psycopg2

#Prompts the user for information which is necessary to connect to the postgres database
db = input("Login to the students database manager!\nWhat is the database name?")
host = input("What is the host name?")
user = input("What is the user name?")
pword = input("What is the password?")
port = input("What is the port?")

conn = psycopg2.connect(database=db,
                        host=host,
                        user=user,
                        password=pword,
                        port=port)

cursor = conn.cursor()

#Create table
cursor.execute('''
    drop table if exists students;;
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        student_id SERIAL PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        enrollment_date DATE
    );
''')

conn.commit()

#Insert starting data
cursor.execute(''' INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES
('John', 'Doe', 'john.doe@example.com', '2023-09-01'),
('Jane', 'Smith', 'jane.smith@example.com', '2023-09-01'),
('Jim', 'Beam', 'jim.beam@example.com', '2023-09-02'); ''')
conn.commit()

#Returns all of the students in the students table
def getAllStudents():
    cursor.execute(''' Select * from students;''')
    for i in cursor.fetchall():
        print(i)

#Adds a student to the student table with the given parameters
def addStudent(first_name, last_name, email, enrollment_date):
    cursor.execute(f''' INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES
    ('{first_name}', '{last_name}', '{email}', '{enrollment_date}'); ''')
    conn.commit()

#Updates a student's emial using the parameters
def updateStudentEmail(student_id, new_email):
    cursor.execute(f'''
        UPDATE students
        SET email = '{new_email}'
        WHERE student_id = {student_id};
    ''')
    conn.commit()

#Deletes a student using their id
def deleteStudent(student_id):
    cursor.execute(f'''
        DELETE FROM students
        WHERE student_id = {student_id};
    ''')
    conn.commit()

#Menu Loop
choice = "-1"
while(choice != "0"):
    print()
    choice = input("Welcome to the students database manager\nPress 1 to get all students \nPress 2 to add a student\nPress 3 to update a student's email\nPress 4 to delete a student\nPress 0 to exit: ")
    print()
    if choice == "1":
        getAllStudents()
    elif choice == "2":
        fname = input("What is the first name of the student? ")
        lname = input("What is the last name of the student? ")
        email = input("What is the email of the student? ")
        enrollment = input("What is the enrollment date of the student? ")
        addStudent(fname, lname, email, enrollment)
    elif choice == "3":
        id = input("What is the student's id? ")
        email = input("What is the new email that you'd like to change to? ")
        updateStudentEmail(id, email)
    elif choice == "4":
        id = input("What is the student's id? ")
        deleteStudent(id)
    elif choice == "0":
        print("Exiting...")
        break
    else:
        print("Input a valid choice")


conn.close()