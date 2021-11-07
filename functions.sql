DELIMITER //
CREATE PROCEDURE GetAllCourses() 
BEGIN
	SELECT * FROM courses;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE AddNewCourse(HR_ID int, Name varchar(255), Course_Outline varchar(255)) 
BEGIN
	INSERT INTO courses(HR_ID, Name, Course_Outline)
    VALUES (HR_ID, Name, Course_Outline);
END //
DELIMITER ;

/*test*/

