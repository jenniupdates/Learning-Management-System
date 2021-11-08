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

# Upload files settings


# this method returns a dictionary of details for all classes a trainer is teaching

@app.route('/trainers/getClassDetails')
def getClassDetails():
    trainer_id = request.args.get('trainer_id')
    tclasses= cc.getClassByTrainer(trainer_id)
    courses = []
    for tclass in tclasses:
        # Initialize a dictionary
        tclass_dict = {}
        # Get the course name from Course object
        tcourse = cc.getCourse(tclass['Course_ID'])
        tcoursename = tcourse.name()
        # Get the current enrolment from Engineer_Course_Class 
        tcourse_enrolled = ec.getClassCapacity(tcourse.cid(), tclass["Class_ID"])
        # Append values to dictionary
        tclass_dict['name'] = tclass['Course_ID'] + " - " + tcoursename
        tclass_dict['class'] = tclass['Class_ID']
        tclass_dict['capacity'] = str(tcourse_enrolled) + "/" + str(tclass['Size_Limit'])
        # Append dictionary to array to be displayed (courses)
        courses.append(tclass_dict)
    return jsonify(
        {
            "courses": courses
        }
    )
    
@app.route('/trainers/getTrainerName')
def getTrainerName():
    trainer_id = request.args.get('trainer_id')
    sql = "SELECT name FROM users WHERE user_id = %s"
    val = trainer_id
    result = db.fetch(sql, val)
    return jsonify({
        "trainer_name": result[0]["name"]
    })

@app.route('/trainers/getAllSections')
def getAllSections():
    class_id = request.args.get('class_id')
    course_id = request.args.get('course_id')
    sections = []
    sql = "SELECT * FROM sections WHERE (course_id, class_id) = (%s,%s)"
    val = (course_id, class_id)
    result = db.fetch(sql, val)
    for row in result:
        section = {}
        section["section_id"] = row["Section_ID"]
        section["description"] = row["Description"]
        section["quiz_id"] = row["Quiz_ID"]
        sql2 = "SELECT * FROM section_course_materials WHERE Course_ID = %s AND Class_ID = %s AND Section_ID = %s"
        val2 = (row['Course_ID'],row['Class_ID'],row['Section_ID'])
        result2 = db.fetch(sql2,val2)
        course_materials = []
        for row2 in result2:
            material_id = row['Course_ID'] + "-" + str(row['Class_ID']) + "-" + str(row['Section_ID']) + "-" + row2['Course_Material_Name']
            course_materials.append({"name":row2['Course_Material_Name'], "material_id":material_id})
        section['course_materials'] = course_materials
        sections.append(section)

    return jsonify({
        "sections": sections
    })

@app.route('/trainers/updateSections')
def updateSections():
    section_id = request.args.get("section_id")
    description = request.args.get("description")
    course_id = request.args.get("course_id")
    class_id = request.args.get("class_id")
    quiz_id = request.args.get("quiz_id")
    sql = "INSERT INTO sections (course_id, class_id, section_id, description, quiz_id)" + \
        "VALUES (%s,%s,%s,%s,%s)"
    val = (course_id, class_id, section_id, description, quiz_id)
    db.execute(sql, val)
    return jsonify({
        "status": "success"
    })

@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        upload_id = request.args.get('ui')
        upload_id_list = upload_id.split("-")
        print(upload_id)
        f = request.files['file']
        file_name = f.filename
        file_data = f.read()
        sql = "INSERT INTO Section_Course_Materials VALUES (%s,%s,%s,%s,%s)"
        val = (upload_id_list[0],upload_id_list[1],upload_id_list[2],file_name,file_data)
        db.execute(sql,val)
        return 'file uploaded successfully'

@app.route('/download',methods=['GET', 'POST'])
def download():
    # NEED TO FIX
    download_id = request.args.get('di')
    file_name = request.args.get('name')
    download_id_list = download_id.split("-")
    sql = "SELECT * FROM Section_Course_Materials WHERE Course_ID = %s AND Class_ID = %s AND Section_ID = %s"
    val = (download_id_list[0],download_id_list[1],download_id_list[2])
    result = db.fetch(sql,val)
    first_file = result[0]
    return send_file(BytesIO(first_file['Course_Material']), attachment_filename=file_name,as_attachment=False,mimetype='application/zip')

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

@app.route('/trainers/updateQuestions', methods=["POST"])
def updateQuestions():
    data = request.get_json()
    quiz_id = data["quiz_id"]
    question_list = data["question_list"]
    # insert into the question table in database
    for qn in question_list:
        # if question is true/false
        if qn['question_type'] == 1:
            sql = "INSERT INTO question (Quiz_ID, Question_ID, Question_Name, Question_Type, Answer)" + \
                "VALUES (%s,%s,%s,%s,%s)"
            val = (quiz_id, qn['question_id'], qn['question'], qn['question_type'], qn['answer'])
            db.execute(sql, val)
        # if question type is MCQ
        if qn['question_type'] == 2:
            sql = "INSERT INTO question (Quiz_ID, Question_ID, Question_Name, Question_Type, Answer)" + \
                "VALUES (%s,%s,%s,%s,%s)"
            val = (quiz_id, qn['question_id'], qn['question'], qn['question_type'], qn['answer'])
            db.execute(sql, val)
            for option in qn['mcq_choices']:
                sql = "INSERT INTO mcq_options (Quiz_ID, Question_ID, Question_Option)" + \
                    "VALUES (%s, %s, %s)"
                val = (quiz_id, qn['question_id'], option)
                db.execute(sql, val)

    return jsonify({
        "quiz_id": quiz_id,
        "questions": question_list
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)