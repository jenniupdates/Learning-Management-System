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
from Course_Eligibility import Course_Eligibility
from io import BytesIO


app = Flask(__name__)
db = DBHelper()
cc = CourseController()
ec = Engineer_Course_Controller()
CORS(app)

# SQL Settings
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

@app.route('/users/getClassSections')
def getClassSections():
    course_id = request.args.get('course_id')
    class_id = request.args.get('class_id')
    user_id = request.args.get('user_id')
    sections = []
    sql = 'SELECT ecs.Section_ID, ecs.Section_Status, s.Description, s.Quiz_ID, s.Course_Material FROM engineer_course_section AS ecs INNER JOIN sections AS s ON ecs.Course_ID = s.Course_ID AND ecs.Class_ID = s.Class_ID AND ecs.Section_ID = s.Section_ID WHERE (ecs.Course_ID, ecs.Class_ID, ecs.User_ID) = (%s,%s,%s)'
    val = (course_id, class_id, user_id)
    result = db.fetch(sql, val)
    sections = []
    for row in result:
        section = {}
        section["section_id"] = row["Section_ID"]
        section["section_status"] = row["Section_Status"]
        section["description"] = row["Description"]
        section["quiz_id"] = row["Quiz_ID"]
        section["course_material"] = row["Course_Material"]
        sections.append(section)
    return jsonify(
        {
            "sections" : sections,
        }
    )

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)