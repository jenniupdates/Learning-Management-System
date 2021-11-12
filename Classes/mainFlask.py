from flask import Flask, request, jsonify, render_template, redirect, url_for, send_file
import requests
from datetime import datetime
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from Database import DBHelper
from Person import Person
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
        url = request.args.get('url')
        class_id = request.args.get('class_id')
        trainer_name = request.args.get('trainer_name')
        f = request.files['file']
        file_name = f.filename
        file_data = f.read()
        sql = "INSERT INTO section_course_materials VALUES (%s,%s,%s,%s,%s)"
        val = (upload_id_list[0],upload_id_list[1],upload_id_list[2],file_name,file_data)
        db.execute(sql,val)
        print("url-------",url)
        return "file uploaded successfully <script>window.location.replace("+url+"&class_id="+class_id+"&trainer_name="+trainer_name+"')</script>"

@app.route('/engineer/getCourseMaterials')
def engineer_getCourseMaterials():
    course_id = request.args.get('course_id')
    class_id = request.args.get('class_id')
    section_id = request.args.get('section_id')
    sql = "SELECT * FROM section_course_materials WHERE Course_ID = %s AND Class_ID = %s AND Section_ID = %s"
    val = (course_id,class_id,section_id)
    result = db.fetch(sql,val)
    course_materials = []
    for row in result:
        material_id = course_id + "-" + class_id + "-" + section_id
        course_materials.append({
            "material_id": material_id,
            "material_name": row['Course_Material_Name']
        })
    
    return jsonify({
        "course_materials": course_materials
    })
    
@app.route('/download',methods=['GET', 'POST'])
def download():
    download_id = request.args.get('di')
    file_name = request.args.get('name')
    download_id_list = download_id.split("-")
    sql = "SELECT * FROM section_course_materials WHERE Course_ID = %s AND Class_ID = %s AND Section_ID = %s"
    val = (download_id_list[0],download_id_list[1],download_id_list[2])
    result = db.fetch(sql,val)
    first_file = result[0]
    return send_file(BytesIO(first_file['Course_Material']), attachment_filename=file_name,as_attachment=False,mimetype='application/zip')

@app.route('/trainers/createQuiz')
def createQuiz():
    quiz_id = request.args.get('quiz_id')
    time_limit = request.args.get('time_limit')
    # split the quiz id into course, class, section
    sql1 = 'INSERT INTO quiz (quiz_id, time_limit) VALUES (%s,%s)'
    val1 = (quiz_id, time_limit)
    db.execute(sql1, val1)
    tmp = quiz_id.split("-")
    course_id = tmp[0]
    class_id = tmp[1]
    section_id = tmp[2]
    if section_id == 'Final':
        sql3 = 'UPDATE course_class SET final_quiz_id = %s WHERE (course_id, class_id) = (%s, %s)'
        val3 = (quiz_id, course_id, class_id)
        db.execute(sql3, val3)
    else:
        sql2 = 'UPDATE sections SET quiz_id = %s WHERE (course_id, class_id, section_id) = (%s, %s, %s)'
        val2 = (quiz_id, course_id, class_id, section_id)
        db.execute(sql2, val2)
    return jsonify({
        "course_id" : course_id,
        "class_id" : class_id,
        "section_id" : section_id
    })

@app.route('/trainers/getFinalQuiz')
def getFinalQuiz():
    course_id = request.args.get('course_id')
    class_id = request.args.get('class_id')
    sql = 'SELECT final_quiz_id FROM course_class WHERE (Course_ID, Class_ID) = (%s,%s)'
    val = (course_id, class_id)
    result = db.fetch(sql, val)
    return jsonify({
        "final_quiz_id": result[0]["final_quiz_id"]
    })

@app.route('/trainers/updateQuestions', methods=["POST"])
def updateQuestions():
    data = request.get_json()
    quiz_id = data["quiz_id"]
    question_list = data["question_list"]
    time_limit = data["time_limit"]
    # delete all questions in the sql tableW for this quiz_id
    sql = "DELETE FROM question WHERE quiz_id = %s"
    val = quiz_id
    db.execute(sql, val)
    #update the time liit
    sql = "UPDATE quiz SET time_limit = %s WHERE quiz_id = %s"
    val = (time_limit, quiz_id)
    db.execute(sql, val)
    # insert into the question table in database
    for qn in question_list:
        sql = "INSERT INTO question (Quiz_ID, Question_ID, Question_Name, Question_Type, Answer)" + \
                "VALUES (%s,%s,%s,%s,%s)"
        val = (quiz_id, qn['question_id'], qn['question'], qn['question_type'], qn['answer'])
        db.execute(sql, val)
        for option in qn['mcq_options']:
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
        
        sql = "SELECT count(*) FROM sections WHERE (Course_ID, Class_ID) = (%s,%s)"
        val = (course_id, class_id)
        result = db.fetch(sql, val)
        section_count = result[0]['count(*)']
        for i in range(section_count):
            sql = "INSERT INTO engineer_course_section (Course_ID, Class_ID, User_ID, Section_ID, Section_Status) VALUES (%s,%s,%s,%s,%s)"
            val = (course_id, class_id, user_id,i+1,"unavailable")
            db.execute(sql, val)
        sql = "UPDATE engineer_course_section SET section_status = 'incomplete' WHERE (Course_ID, Class_ID, User_ID, Section_ID) = (%s,%s,%s,%s)"
        val = (course_id, class_id, user_id, '1')
        db.execute(sql, val)
        
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

        sql = "SELECT count(*) FROM sections WHERE (Course_ID, Class_ID) = (%s,%s)"
        val = (course_id, class_id)
        result = db.fetch(sql, val)
        section_count = result[0]['count(*)']
        for i in range(section_count):
            sql = "INSERT INTO engineer_course_section (Course_ID, Class_ID, User_ID, Section_ID, Section_Status) VALUES (%s,%s,%s,%s,%s)"
            val = (course_id, class_id, user_id,i+1,"unavailable")
            db.execute(sql, val)
        sql = "UPDATE engineer_course_section SET section_status = 'incomplete' WHERE (Course_ID, Class_ID, User_ID, Section_ID) = (%s,%s,%s,%s)"
        val = (course_id, class_id, user_id, '1')
        db.execute(sql, val)

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
            val2 = (course_id,i,0,class_start,class_end,size_limit,reg_start,reg_end,None)
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
    
@app.route('/users/withdrawFromCourse')
def withdrawFromCourse():
    course_id = request.args.get('course_id')
    class_id = request.args.get('class_id')
    user_id = request.args.get('user_id')
    sql = 'UPDATE engineer_course_enrolment SET course_status = "eligible", class_id = "0" WHERE (Course_ID, Class_ID, User_ID) = (%s,%s,%s)'
    val = (course_id, class_id, user_id)
    db.execute(sql, val)
    return jsonify({
            "code": 200,
            "message": "Course withdrawn from successfully! Refreshing page in 3 seconds."
        })

@app.route('/engineer/completeCourse', methods=['POST'])
def completeCourse():
    course_id = request.json.get('course_id')
    class_id = request.json.get('class_id')
    user_id = request.json.get('user_id')
    score = str(request.json.get('score'))

    sql = "UPDATE engineer_course_enrolment SET Course_Status = %s, Score = %s WHERE (Course_ID, Class_ID, User_ID) = (%s,%s,%s)"
    val = ('completed', score, course_id, class_id, user_id)
    db.execute(sql, val)
    return jsonify({
        "code": 200,
        "message": "Completed course and final quiz successsfully"
    })
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

@app.route('/engineer/makeNextSectionAvl', methods=['POST'])
def makeNextSectionAvl():
    course_id = request.json.get('course_id')
    class_id = request.json.get('class_id')
    section_id = int(request.json.get('section_id'))
    user_id = request.json.get('user_id')
    next_section_id = section_id + 1
    # Check if next section exist
    sql = "SELECT * FROM engineer_course_section WHERE Course_ID = %s AND Class_ID = %s AND User_ID = %s AND Section_ID = %s"
    val = (course_id,class_id,user_id,next_section_id)
    result = db.fetch(sql,val)
    if len(result) == 0:
        return jsonify({
            "next?": "no",
            "message": "You have reached the last section of this course. You now need to take the final quiz and get 80% in order to pass the course."
        })
    else:
        sql2 = "UPDATE engineer_course_section SET Section_Status = %s WHERE Course_ID = %s AND Class_ID = %s AND User_ID = %s AND Section_ID = %s"
        val2 = ("incomplete",course_id,class_id,user_id,next_section_id)
        db.execute(sql2,val2)
        return jsonify({
            "next?": "yes",
            "next_section_id": next_section_id,
            "message": "You have completed this section. You may now proceed to the next section, or retake the quiz."
        })
        
        
@app.route('/HR/getTrainerlessClasses')
def getTrainerlessClasses():
    sql = "SELECT * FROM course_class WHERE Trainer_ID = %s"
    val = (0)
    result = db.fetch(sql,val)
    trainerless_classes = []
    for row in result:
        sql2 = "SELECT * FROM courses WHERE Course_ID = %s"
        val2 = (row['Course_ID'])
        result2 = db.fetch(sql2,val2)
        course = Course(result2[0]['Course_ID'],result2[0]['Course_Name'],result2[0]['Course_Outline'])
        course_name = course.name()
        trainer_class = {
            "course_id": row['Course_ID'],
            "class_id": row['Class_ID'],
            "course_name": course_name
        }
        trainerless_classes.append(trainer_class)
        
    return jsonify({
        "classes": trainerless_classes
    })
    
@app.route('/HR/getTrainers')
def getTrainers():
    sql = "SELECT * FROM users WHERE UserType = %s"
    val = (2)
    result = db.fetch(sql,val)
    trainers = []
    for row in result:
        person_trainer = Person(row['Name'],row['User_ID'],row['UserType'],row['Password'])
        trainer = {
            "user_id": person_trainer.getUserID(),
            "name": person_trainer.getName()
        }
        trainers.append(trainer)
    
    return jsonify({
        "trainers": trainers
    })
    
@app.route('/HR/assignTrainer', methods=['PUT'])
def assignTrainer():
    try:
        course_id = request.json.get('course_id')
        class_id = request.json.get('class_id')
        trainer_id = request.json.get('trainer_id')
        
        sql = "UPDATE course_class SET Trainer_ID = %s WHERE Course_ID = %s AND Class_ID = %s"
        val = (trainer_id,course_id,class_id)
        db.execute(sql,val)
        
        return jsonify({
            "code": 200,
            "message": "Trainer has been assigned to the class successfully. Refreshing page in 2 seconds."
        })
        
    except Exception as e:
        return jsonify({
            "code":500,
            "message":"An error occurred while assigning trainer: " + str(e)
        }),500
        
@app.route('/HR/getCurCapacity')
def getCurCapacity():
    class_id = request.args.get('class_id')
    course_id = request.args.get('course_id')
    sql = "SELECT * FROM engineer_course_enrolment WHERE Course_ID = %s AND Class_ID = %s AND (Course_Status = %s OR Course_Status = %s)"
    val = (course_id,class_id,'enrolled','completed')
    result = db.fetch(sql,val)
    count = 0
    for row in result:
        count += 1
    return jsonify({
        "cur_capacity": count
    })
    
@app.route('/HR/getMaxCapacity')
def getMaxCapacity():
    class_id = request.args.get('class_id')
    course_id = request.args.get('course_id')
    sql = "SELECT * FROM course_class WHERE Course_ID = %s AND Class_ID = %s"
    val = (course_id,class_id)
    result = db.fetch(sql,val)
    if len(result) > 0:
        size_limit = result[0]['Size_Limit']
        return jsonify({
            "size_limit": size_limit
        })
    else:
        return jsonify({
            "size_limit": "Not found"
        })
    
    
@app.route('/trainers/populateQuestions')
def populateQuestions():
    quiz_id = request.args.get('quiz_id')
    question_list = []
    sql = "SELECT time_limit FROM quiz WHERE quiz_id = %s"
    val = quiz_id
    result = db.fetch(sql, val)
    sql1 = "SELECT * FROM question WHERE quiz_id = %s"
    val1 = quiz_id
    result1 = db.fetch(sql1, val1)
    for row in result1:
        curr_qn = {}
        curr_qn["question_id"] = row["Question_ID"]
        curr_qn["question"] = row["Question_Name"]
        curr_qn["question_type"] = row["Question_Type"]
        curr_qn["answer"] = row["Answer"]
        if row["Question_Type"] == 1:
            options = []
            sql2 = "SELECT * FROM mcq_options WHERE (Quiz_ID, Question_ID) = (%s,%s)"
            val2 = (quiz_id, row["Question_ID"])
            result2 = db.fetch(sql2, val2)
            for row2 in result2:
                options.append(row2["Question_Option"])
            curr_qn["mcq_options"] = options
        else:
            curr_qn['mcq_options'] = ['true','false']
        question_list.append(curr_qn)
    return jsonify({
        "quiz_id": quiz_id,
        "question_list": question_list,
        "time_limit": result[0]["time_limit"]
    })
    
@app.route('/getCoursePrerequisites')
def getCoursePrerequisites():
    course_prereq_dict = {}
    sql = "SELECT * FROM courses"
    result = db.fetch(sql)
    for row in result:
        course_id = row['Course_ID']
        course_prereq_dict[course_id] = []
        sql2 = "SELECT * FROM course_prereqs WHERE Course_ID = %s"
        val2 = (course_id)
        result2 = db.fetch(sql2,val2)
        for row2 in result2:
            course_prereq_dict[course_id].append(row2['Course_prereq_ID'])
            
    return jsonify({
        "course_prereqs": course_prereq_dict
    })
    
        
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)