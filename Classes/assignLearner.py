from flask import Flask, request, jsonify, render_template, redirect, url_for, send_file
import requests
from datetime import datetime
from flask_cors import CORS
from Database import DBHelper
from Course import Course
from Course_Class import Course_Class
from Course_Eligibility import Course_Eligibility

app = Flask(__name__)
db = DBHelper()
CORS(app)

# SQL Settings
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

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

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)

