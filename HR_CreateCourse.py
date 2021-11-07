from flask import Flask, render_template , redirect, url_for, request
from Database import DBHelper



app = Flask(__name__)
db = DBHelper()


@app.route('/')
def index():
    return render_template('HR_CreateCourse.html')# this is to allow the display of the html page 

@app.route('/success',methods = ["GET","POST"])
def success():
    try:
        if request.method == "POST":
            CourseID = request.form.get("id")
            Course = request.form.get("CourseName")
            Course_prereq = request.form.get("course_prereq")
            CourseOutline = request.form.get("outline")
            Class_id = request.form.get("class_id")
            print(CourseID)
            print(Course)
            print(Course_prereq)
            print(CourseOutline)
            print(Class_id)
            db = DBHelper()
            db.execute("INSERT INTO course_prereqs (Course_ID, Course_prereq_ID) VALUES(%s,%s)",(CourseID, Course_prereq))#insert into course_prereq
            db.execute("INSERT INTO courses (Course_ID, Course_Name,HR_ID, Course_Outline) VALUES(%s,%s,%s,%s)",(CourseID, Course,"2",CourseOutline))#insert into courses
            db.execute("INSERT INTO engineer_course_enrolment (Course_ID, Class_ID) VALUES(%s,%s)",(CourseID, Class_id)) #inserting in to engineer course enrolment


            return '''
                    <h1>Success!</h1>'''
    except:
        return  '''
                    <h1>ERROR!</h1>'''  
                  
    







if  __name__ =="__main__":
    app.run(debug=True)