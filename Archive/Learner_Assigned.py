from flask import Flask, render_template , redirect, url_for, request,jsonify
from werkzeug.utils import environ_property
from Database import DBHelper
from Engineer_Course_Controller import Engineer_Course_Controller



app = Flask(__name__)



headings =("Course ID","Class ID","Class Size", "Capacity")
db = DBHelper()
course_controller = Engineer_Course_Controller()
row = []
rows = []

eligible_course = db.fetchall("SELECT Course_ID , Class_ID , Course_Status from engineer_course_enrolment where User_ID = '1'")# this is wat the user is eligible for
print(eligible_course)
for course in eligible_course:
    slots_avaliable = course_controller.getClassCapacity(course['Course_ID'],course['Class_ID'])
    vals = (course['Course_ID'],course['Class_ID'])
    sql = "SELECT Size_Limit FROM course_class WHERE Course_ID = %s AND Class_ID = %s"
    result = db.fetch(sql, vals)
    row.append(course['Course_ID'])
    row.append(course['Class_ID'])
    row.append(result[0]["Size_Limit"])
    row.append(slots_avaliable)
    rows.append(row)
    row = []

print(rows)

#trainer id



@app.route('/')
def index():
    return render_template('assign_course.html',headings = headings, rows = rows)# this is to allow the display of the html page 

    
    
if  __name__ =="__main__":
    app.run(debug=True)