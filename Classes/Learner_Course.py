from flask import Flask, render_template , redirect, url_for, request
from Database import DBHelper



app = Flask(__name__)

headings =("Course ID","Class ID", "Trainer ID", "Size Limit")
db = DBHelper()
data = db.fetchall("select Course_ID , Class_ID , Trainer_ID , Size_Limit from course_class")

print(data)

@app.route('/')
def index():
    return render_template('Learner_course.html',headings = headings, data = data)# this is to allow the display of the html page 

    
    
if  __name__ =="__main__":
    app.run(debug=True)


# Display enrolled courses of that user's
