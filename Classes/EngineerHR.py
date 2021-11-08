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
from Course_Controller import CourseController
from io import BytesIO

app = Flask(__name__)
db = DBHelper()
cc = CourseController()
ec = Engineer_Course_Controller()
CORS(app)

# SQL Settings
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}


@app.route('/engineer/getAllCourses')
def engineer_getAllCourses():
    user_id = request.args.get('user_id')
    sql = "SELECT * FROM engineer_course_enrolment WHERE User_ID = %s"
    val = (user_id)
    result = db.fetch(sql,val)
    courses = []
    for row in result:
        course = {}
        course['course_id'] = row['Course_ID']
        sql2 = "SELECT * FROM courses WHERE Course_ID = %s"
        val2 = (course['course_id'])
        result2 = db.fetch(sql2,val2)
        course['course_name'] = result2[0]['Course_Name']
        course['course_outline'] = result2[0]['Course_Outline']
        course['class_id'] = row['Class_ID']
        course_classes = []
        sql3 = "SELECT * FROM course_class WHERE Course_ID = %s"
        val3 = (course['course_id'])
        result3 = db.fetch(sql3,val3)
        for row3 in result3:
            course_classes.append(row3['Class_ID'])
        course['course_classes'] = course_classes
        course['course_status'] = row['Course_Status']
        courses.append(course)

    return jsonify({
        "courses": courses
    })

@app.route('/engineer/enroll')
def engineer_enroll():
    try:
        user_id = request.args.get('user_id')
        course_id = request.args.get('course_id')
        class_id = request.args.get('class_id')
        sql = "UPDATE engineer_course_enrolment SET Course_Status = 'pending', Class_ID = %s WHERE Course_ID = %s AND Class_ID = 0 AND User_ID = %s"
        val = (class_id,course_id,user_id)
        db.execute(sql,val)

        return jsonify({
            "code": 200,
            "message": "Your enrolment is now pending approval from HR. Refreshing page in 4 seconds."
        })
    except Exception as e:
        return jsonify({
            "code":500,
            "message":"An error occurred while enrolling for course: " + str(e)
        }),500

@app.route('/HR/getAllCourses')
def hr_getAllCourses():
    sql = "SELECT * FROM courses"
    result = db.fetch(sql)
    courses = []
    for row in result:
        course = Course(row['Course_ID'],row['Course_Name'],row['Course_Outline'])
        courses.append({
            "course_id": course.cid(),
            "course_name": course.name(),
            "course_outline": course.outline()
        })
    
    return jsonify({
        "courses": courses
    })

@app.route('/HR/createCourse',methods=['POST'])
def hr_createCourse():
    try:
        course_id = request.json.get('courseID')
        course_name = request.json.get('courseName')
        course_outline = request.json.get('courseOutline')
        num_classes = int(request.json.get('numOfClasses'))
        size_limit = int(request.json.get('size_limit'))
        prereq_list = request.json.get('prereq_list')
        class_start = request.json.get('class_start')
        class_end = request.json.get('class_end')
        reg_start = request.json.get('reg_start')
        reg_end = request.json.get('reg_end')
        # INSERT INTO Courses Database
        sql = "INSERT INTO courses VALUES (%s,%s,%s)"
        val = (course_id,course_name,course_outline)
        db.execute(sql,val)

        # INSERT into course_class
        for i in range(1,num_classes+1):
            sql2 = "INSERT INTO course_class VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val2 = (course_id,i,None,class_start,class_end,size_limit,reg_start,reg_end,None)
            db.execute(sql2,val2)
        
        # INSERT into course_prereqs
        for prereq in prereq_list:
            sql3 = "INSERT INTO course_prereqs VALUES (%s,%s)"
            val3 = (course_id,prereq)
            db.execute(sql3,val3)
        
        # Insert into engineer_course_enrolment 
        ## Get all engineers
        sql4 = "SELECT * FROM users WHERE UserType = 1"
        engineer_result = db.fetch(sql4)
        for engineer in engineer_result:
            engineer_id = engineer['User_ID']
            eligibility = "eligible"
            # Check if they have completed prerequisites
            for prereq_id in prereq_list:
                sql5 = "SELECT * FROM engineer_course_enrolment WHERE Course_ID = %s AND User_ID = %s"
                val5 = (prereq_id,engineer_id)
                prereq_result = db.fetch(sql5,val5)
                if prereq_result[0]['Course_Status'] != 'completed':
                    eligibility = "ineligible"
            
            # insert into course enrolment
            sql6 = "INSERT INTO engineer_course_enrolment VALUES(%s,%s,%s,%s,%s)"
            val6 = (course_id,0,engineer_id,eligibility,None)
            db.execute(sql6,val6)

        return jsonify({
            "code": 200,
            "message": "Course created successfully! Refreshing page in 3 seconds."
        })

    except Exception as e:
        print(e)
        return jsonify({
            "code":500,
            "message":"An error occurred while creating course: " + str(e)
        }),500





if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)