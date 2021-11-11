# To test if DB control works, Add the following rows into SQL
# INSERT INTO course_eligibility VALUES (1,1,'Ineligible')
# INSERT into quiz VALUES (5,60);
# INSERT into sections VALUES (3,1,1,'WAD Part 0',5,'Part 0 Course Materials');
# INSERT into engineer_course_section VALUES (3,1,3,1,'Available',5);
from Engineer_Course_Controller import Engineer_Course_Controller 

def test():
    controller = Engineer_Course_Controller()

    # Getting Enrolment, Section and Eligibility for a partiuclar engineer and course
    engineer_course_enrolment = controller.getEngineerCourseEnrolment(1,1,1)
    print("Old Enrolment: ", engineer_course_enrolment.getCourseStatus())

    engineer_course_section = controller.getEngineerCourseSection(3,1,3,2)
    print("Old Section ",engineer_course_section.getSectionStatus())

    # Update Course eligibility to complete
    engineer_course_eligibility = controller.getEngineerCourseEligibility(1,1)
    print("Old eligibility: ", engineer_course_eligibility.getCourseEligibility())
    
    controller.updateCourseEligibility(engineer_course_eligibility)

    new_engineer_course_eligibility = controller.getEngineerCourseEligibility(1,1)
    print("New eligibility: ", new_engineer_course_eligibility.getCourseEligibility())

    controller.completeCourse(engineer_course_enrolment)

    new_engineer_course_enrolment = controller.getEngineerCourseEnrolment(1,1,1)
    print("New enrolment: ", new_engineer_course_enrolment.getCourseStatus())

    prev_section = controller.getEngineerCourseSection(3,1,3,1)
    controller.accessNextSection(prev_section)
    new_section = controller.getEngineerCourseSection(3,1,3,2)
    print("New updated section: ",new_section.getSectionStatus())

test()