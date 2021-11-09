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


@app.route('/trainers/getClassDetails')
def getClassDetails():
    trainer_id = request.args.get('trainer_id')
    tclasses= cc.getClassByTrainer(trainer_id)
    courses = []
    for tclass in tclasses:
        tclass_dict = {}
        tcourse = cc.getCourse(tclass['Course_ID'])
        tcoursename = tcourse.name()
        tcourse_enrolled = ec.getClassCapacity(tcourse.cid(), tclass["Class_ID"])
        tclass_dict['name'] = tclass['Course_ID'] + " - " + tcoursename
        tclass_dict['class'] = tclass['Class_ID']
        tclass_dict['capacity'] = str(tcourse_enrolled) + "/" + str(tclass['Size_Limit'])
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

@app.route('/loadAllCourses')
def loadAllCourses():
    sql = "SELECT * FROM courses"
    result = db.fetch(sql)
    course_tup_list = [] # Each Course is a tuple (Course Name, Course ID)
    for row in result:
        course = Course(row['Course_ID'],row['Course_Name'],row['Course_Outline'])
        course_tup_list.append( (course.name(),course.cid()) )
    
    return jsonify(
        {
            "courses": course_tup_list
        }
    )
    
@app.route('/getAllClasses/<string:courseID>')
def getAllClasses(courseID):
    sql = "SELECT * FROM course_class WHERE Course_ID = %s"
    val = (courseID)
    result = db.fetch(sql,val)
    course_classes = []
    for row in result:
        course_class = Course_Class(row['Course_ID'],
                                    row['Class_ID'],
                                    row['Trainer_ID'],
                                    row['Class_Start'],
                                    row['Class_End'],
                                    row['Size_Limit'],
                                    row['Reg_Start'],
                                    row['Reg_End'],
                                    row['Final_Quiz_ID'])
        course_classes.append( {
            "class_id": course_class.clid(),
            "trainer_id": course_class.tid(),
            "class_start": course_class.classstart(),
            "class_end": course_class.classend(),
            "size_limit": course_class.sizelimit()
        })

    return jsonify(
        {
            "classes": course_classes
        }
    )

@app.route('/users/getTrainerName')
def getTrainerNames():
    class_id = request.args.get('class_id')
    course_id = request.args.get('course_id')
    sql = "SELECT * FROM course_class WHERE Course_ID = %s AND Class_ID = %s"
    val = (course_id,class_id)
    result = db.fetch(sql,val)
    sql = "SELECT Name FROM users WHERE User_ID = %s"
    val = (result[0]["Trainer_ID"])
    result2 = db.fetch(sql,val)

    return jsonify({
        "trainer_name": result2[0]["Name"]
    })

@app.route('/getUsersEligibility/<string:courseID>')
def getUsersEligibility(courseID):
    sql = "SELECT * FROM engineer_course_enrolment WHERE Course_ID = %s AND Class_ID = 0"
    val = (courseID)
    result = db.fetch(sql,val)
    course_eli_list = []
    for row in result:
        course_eli = Course_Eligibility(row['Course_ID'],row['User_ID'],row['Course_Status'])
        sql = "SELECT * FROM users WHERE User_ID = %s"
        val = (course_eli.getUserID())
        result2 = db.fetch(sql,val)
        course_eli_list.append({
            "user_id": result2[0]['User_ID'],
            "name": result2[0]['Name'],
            "username": result2[0]['Username'],
            "eligibility": course_eli.getCourseEligibility()
        })

    return jsonify({
        "eligibilities": course_eli_list
    })

@app.route('/enrolLearner',methods=['PUT'])
def enrolLearner():
    try:
        user_id = request.json.get('uid')
        course_id = request.json.get('cid')
        class_id = request.json.get('clid')

        sql = "UPDATE engineer_course_enrolment SET Class_ID = %s, Course_Status = 'enrolled' WHERE Course_ID = %s AND User_ID = %s"
        val = (class_id,course_id,user_id)
        db.execute(sql,val)
        return jsonify({
            "code": 200,
            "message": "Successfully enrolled, refreshing the page in 2 seconds."
        }),200
    except Exception as e:
        return jsonify({
            "code":500,
            "message":"An error occurred while enrolling student: " + str(e)
        }),500

@app.route('/getQuestionsAndOptions/<string:quiz_id>')
def getQuestionsAndOptions(quiz_id):
    sql = "SELECT * FROM question WHERE Quiz_ID = %s"
    val = (quiz_id)
    result = db.fetch(sql,val)
    quiz_dict = []
    for row in result:
        question_name = row['Question_Name']
        options = []
        sql2 = "SELECT * FROM mcq_options WHERE Quiz_ID = %s AND Question_ID = %s"
        val2 = (row["Quiz_ID"],row["Question_ID"])
        result2 = db.fetch(sql2,val2)
        for row2 in result2:
            options.append(row2['Question_Option'])
        
        quiz_dict.append({"question_name": question_name, "options": options})

    return jsonify({
        "quiz": quiz_dict
    })

@app.route('/gradeQuiz',methods=["POST"])
def gradeQuiz():
    data = request.get_json()
    quiz_id = data['quiz_id']
    quiz_answers = data['submission']
    sql = "SELECT * FROM question WHERE Quiz_ID = %s"
    val = (quiz_id)
    result = db.fetch(sql,val)
    answer_key = {}
    for row in result:
        answer_key[str(row['Question_ID'])] = row['Answer']
    
    correct_list = []
    for quiz_answer in quiz_answers:
        qn_dict = {"question_id": quiz_answer['question_id']}
        if quiz_answer['answer'] == answer_key[quiz_answer['question_id']]:
            qn_dict['correct?'] = 'Yes'
        else:
            qn_dict['correct?'] = 'No'
        qn_dict['correct_answer'] = answer_key[quiz_answer['question_id']]
        
        correct_list.append(qn_dict)

    return jsonify({
        "quiz_results": correct_list
    })


@app.route('/getSectionQuizID',methods=['POST'])
def getSectionQuizID():
    # REQUIRES JS object {'course_ID','class_ID','section_ID'}
    data = request.get_json()
    course_id = data['course_ID']
    class_id = data['class_ID']
    section_id = data['section_ID']

    sql = "SELECT * FROM sections WHERE Course_ID = %s AND Class_ID = %s AND Section_ID = %s"
    val = (course_id,class_id,section_id)
    result = db.fetch(sql,val)
    if len(result) < 1:
        return jsonify({
        "quiz_id": None
    })
    else:
        quiz_id = result[0]['Quiz_ID']

        return jsonify({
            "quiz_id": quiz_id
        })

@app.route('/getAllPendingEnrolment')
def getAllPendingEnrolment():
    sql = "SELECT * FROM engineer_course_enrolment WHERE Course_Status = 'pending'"
    result = db.fetch(sql)
    pending_tup_list = [] 
    for row in result:
        sql = "SELECT * FROM users WHERE User_ID = %s"
        val = (row['User_ID'])
        result2 = db.fetch(sql,val)
        name = result2[0]['Name']
        username = result2[0]['Username']

        pending_tup_list.append({"course_id": row['Course_ID'],
                                "user_id": row['User_ID'],
                                "name": name,
                                "username": username,
                                "class_id": row['Class_ID']
                                })
    
    return jsonify(
        {
            "pending_list": pending_tup_list
        }
    )

@app.route('/hr/approveEnrolment',methods=['PUT'])
def approveEnrolment():
    try:
        # REQUIRES JS object {'course_ID','class_ID','user_ID'}
        data = request.get_json()
        course_id = data['course_ID']
        class_id = data['class_ID']
        user_id = data['user_ID']
        
        sql = "UPDATE engineer_course_enrolment SET Course_Status = 'enrolled' WHERE Course_ID = %s AND Class_ID = %s AND User_ID = %s"
        val = (course_id,class_id,user_id)
        db.execute(sql,val)

        return jsonify({
            "code": 200,
            "message": "User enrolment accepted! Refreshing the page in 2 seconds."
        })
    except Exception as e:
        return jsonify({
            "code":500,
            "message":"An error occurred while accepting enrolment of engineer: " + str(e)
        }),500

@app.route('/hr/rejectEnrolment',methods=['PUT']) 
def rejectEnrolment():
    try:
        # REQUIRES JS object {'course_ID','class_ID','user_ID'}
        data = request.get_json()
        course_id = data['course_ID']
        class_id = data['class_ID']
        user_id = data['user_ID']
        
        sql = "UPDATE engineer_course_enrolment SET Course_Status = 'eligible' WHERE Course_ID = %s AND Class_ID = %s AND User_ID = %s"
        val = (course_id,class_id,user_id)
        db.execute(sql,val)

        return jsonify({
            "code": 200,
            "message": "User enrolment rejected! Refreshing the page in 2 seconds."
        })
    except Exception as e:
        return jsonify({
            "code":500,
            "message":"An error occurred while rejecting enrolment of engineer: " + str(e)
        }),500
        
@app.route('/users/getAllCourses')
def getAllCourses():
    user_id = request.args.get('user_id')
    sql = "SELECT * FROM engineer_course_enrolment WHERE User_ID = %s AND (Course_Status = 'completed' OR Course_Status = 'enrolled' OR Course_Status = 'pending')"
    courses = []
    val = (user_id)
    result = db.fetch(sql, val)
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
        
@app.route('/users/getAllCourses')
def users_getAllCourses():
    user_id = request.args.get('user_id')
    sql = "SELECT * FROM engineer_course_enrolment WHERE User_ID = %s AND (Course_Status = 'completed' OR Course_Status = 'enrolled' OR Course_Status = 'pending')"
    courses = []
    val = user_id
    result = db.fetch(sql, val)
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

@app.route('/users/getClassSections')
def getClassSections():
    course_id = request.args.get('course_id')
    class_id = request.args.get('class_id')
    user_id = request.args.get('user_id')
    sections = []
    sql = 'SELECT ecs.Section_ID, ecs.Section_Status, s.Description, s.Quiz_ID FROM engineer_course_section AS ecs INNER JOIN sections AS s ON ecs.Course_ID = s.Course_ID AND ecs.Class_ID = s.Class_ID AND ecs.Section_ID = s.Section_ID WHERE (ecs.Course_ID, ecs.Class_ID, ecs.User_ID) = (%s,%s,%s)'
    val = (course_id, class_id, user_id)
    result = db.fetch(sql, val)
    sections = []
    for row in result:
        section = {}
        section["section_id"] = row["Section_ID"]
        section["section_status"] = row["Section_Status"]
        section["description"] = row["Description"]
        section["quiz_id"] = row["Quiz_ID"]
        sections.append(section)
    return jsonify(
        {
            "sections" : sections,
        }
    )
    
    
@app.route('/engineer/completeSection',methods=['POST'])
def completeSection():
    course_id = request.json.get('course_id')
    class_id = request.json.get('class_id')
    section_id = request.json.get('section_id')
    user_id = request.json.get('user_id')
    sql = "UPDATE engineer_course_section SET Section_Status = %s WHERE Course_ID = %s AND Class_ID = %s AND User_ID = %s AND Section_ID = %s"
    val = ('completed',course_id,class_id,user_id,section_id)
    db.execute(sql,val)
    return jsonify({
        "code": 200,
        "message": "Completed course successsfully"
    })

@app.route('/engineer/accessNextSection')
def accessNextSection():
    pass

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)