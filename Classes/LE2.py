from flask import Flask, request, jsonify, render_template, redirect, url_for, send_file
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

@app.route('/users/getAllCourses')
def getAllCourses():
    user_id = request.args.get('user_id')
    sql = "SELECT * FROM engineer_course_enrolment WHERE User_ID = %s AND (Course_Status = 'completed' OR Course_Status = 'enrolled' OR Course_Status = 'pending')"
    courses = []
    val = user_id
    result = db.fetch(sql, 1)
    for row in result:
        course = {}
        course["course_id"] = row["Course_ID"]
        course["class_id"] = row["Class_ID"]
        course["course_status"] = row["Course_Status"]
        courses.append(course)
    return jsonify (
        {
            "courses" : courses
        }
    )

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)