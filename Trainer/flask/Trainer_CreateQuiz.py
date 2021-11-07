from flask import Flask, request, jsonify, render_template, redirect, url_for
import requests
from datetime import datetime
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from Database import DBHelper
from Course import Course
from Course_Class import Course_Class
from Engineer_Course_Controller import Engineer_Course_Controller
from Section_Controller import Section_Controller
from Course_Controller import CourseController



app = Flask(__name__)
db = DBHelper()
CORS(app)

# SQL Settings
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

@app.route('/trainers/createQuiz')
def createQuiz():
    quiz_id = request.args.get('quiz_id')
    time_limit = request.args.get('time_limit')
    # split the quiz id into course, clas, section
    tmp = quiz_id.split("-")
    course_id = tmp[0]
    class_id = tmp[1]
    section_id = tmp[2]
    sql1 = 'INSERT INTO quiz (quiz_id, time_limit) VALUES (%s,%s)'
    sql2 = 'UPDATE sections SET quiz_id = %s WHERE (course_id, class_id, section_id) = (%s, %s, %s)'
    val1 = (quiz_id, time_limit)
    val2 = (quiz_id, course_id, class_id, section_id)
    db.execute(sql1, val1)
    db.execute(sql2, val2)
    return jsonify({
        "course_id" : course_id,
        "class_id" : class_id,
        "section_id" : section_id
    })

@app.route('/answer',methods = ["GET","POST"])
def answer():
    #try:
        if request.method == "POST":
            db = DBHelper()
            data = request.json
            print(data)
            for answer in data:
                db.execute("INSERT INTO question (Quiz_ID, Question_ID, Question_Name,Question_Type,Answer) VALUES(%s,%s,%s,%s,%s)",("is111-1-4",answer[0],answer[1],answer[2],answer[3]))#MCQ Options
            
        

@app.route('/mcqOptions',methods = ["GET","POST"])
def mcqOptions():
    #try:
        if request.method == "POST":
            db = DBHelper()
            data = request.json
            print(data)
            for question in data:
                for i in range(1,len(question)):
                    print(question[i])
                    db.execute("INSERT INTO mcq_options (Quiz_ID, Question_ID, Question_Option) VALUES(%s,%s,%s)",(1,question[0] ,question[i]))#MCQ Options.
            
            return jsonify(data)

           

            #return jsonify(data)
            #return '''
           #         <h1>Success!</h1>'''
    #except:
       # return  '''
          #          <h1>ERROR!</h1>'''

#assume course id , section and class is being given.
#quiz mcq options quiz id , question id and  question option is needed to be included.

if  __name__ =="__main__":
    app.run(debug=True)
