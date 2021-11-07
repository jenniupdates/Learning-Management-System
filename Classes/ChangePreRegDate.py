from flask import Flask, render_template , redirect, url_for, request
from Database import DBHelper

app = Flask(__name__)
db = DBHelper()

@app.route('/')
def index():
    return render_template('ChangePreRegDate.html')# this is to allow the display of the html page 


@app.route('/PreRegistrationDateChangeSuccess',methods = ["GET","POST"])
def success():
    if request.method == "POST":
        CourseID = request.form.get("courseid")
        ClassID = request.form.get("classid")
        TrainerID = request.form.get("trainerid")
        RegStart = request.form.get("regStart")
        RegEnd = request.form.get("regEnd")
        db = DBHelper()

        sql = "UPDATE course_class SET Reg_Start = %s, Reg_End = %s WHERE Course_ID = %s AND Class_ID = %s AND Trainer_ID = %s"
        val = (RegStart, RegEnd, CourseID, ClassID, TrainerID)
        db.execute(sql, val)

        
if  __name__ =="__main__":
    app.run(debug=True)