DROP DATABASE IF EXISTS `g3t4`;
CREATE DATABASE `g3t4`;
USE `g3t4`;

DROP TABLE IF EXISTS users;
CREATE TABLE users (
	User_ID int not null auto_increment,
    Name varchar(255) not null,
    Username varchar(255) not null,
    Password varchar(255) not null,
    UserType int not null, 
    Designation varchar(255),
    Department varchar(255),
    -- user_types: {1 -> engineer, 2-> trainer, 3 -> hr}
    primary key (User_ID)
)engine=innoDB;

INSERT INTO `g3t4`.`users` (Name, Username, Password, UserType, Designation, Department) VALUES ('Richard',  'RG', 'r_pass', '1', 'designee', 'operations');
INSERT INTO `g3t4`.`users` (Name, Username, Password, UserType, Designation, Department) VALUES ('YS',  'YS', 'ys_pass', '2', 'designee', 'operations');
INSERT INTO `g3t4`.`users` (Name, Username, Password, UserType, Designation, Department) VALUES ('Stephen',  'S', 's_pass', '1', 'designee', 'servicing');
INSERT INTO `g3t4`.`users` (Name, Username, Password, UserType, Designation, Department) VALUES ('Isaac',  'I', 'i_pass', '2', 'designee', 'servicing');
INSERT INTO `g3t4`.`users` (Name, Username, Password, UserType, Designation, Department) VALUES ('Chee Kuang',  'CK', 'ck_pass', '3', 'designee', 'human resource');
INSERT INTO `g3t4`.`users` (Name, Username, Password, UserType, Designation, Department) VALUES ('Sarah',  'Sara', 'sara_pass', '1', 'designee', 'engineer');

DROP TABLE IF EXISTS courses;
CREATE TABLE courses (
	Course_ID varchar(15) not null,
    Course_Name varchar(255) not null,
    Course_Outline varchar(255),
    primary key (Course_ID)
)engine=innoDB;

INSERT INTO `g3t4`.`courses` (Course_ID, Course_Name, Course_Outline) VALUES ('ES102', 'Intro to Engineering', 'The basics of engineering');
INSERT INTO `g3t4`.`courses` (Course_ID, Course_Name, Course_Outline) VALUES ('IS111', 'Intro to Progamming', 'Python Program helps you to python');
INSERT INTO `g3t4`.`courses` (Course_ID, Course_Name, Course_Outline) VALUES ('IS216', 'Web Development I', 'Web Development for Beginners');

DROP TABLE IF EXISTS course_prereqs;
CREATE TABLE course_prereqs (
	Course_ID varchar(15) not null,
    Course_prereq_ID varchar(15) not null,
    -- list of courseid required to be completed before eligible for the course
    constraint PK_Prereq primary key (Course_ID, Course_prereq_ID),
 	foreign key (Course_ID) references courses(Course_ID) on delete cascade on update cascade,
    foreign key (Course_prereq_ID) references courses(Course_ID) on delete cascade on update cascade
--     foreign key (Course_prereq_ID) references Courses(Course_ID)
)engine=innoDB;

INSERT INTO `g3t4`.`course_prereqs` (Course_ID, Course_prereq_ID) VALUES ('IS216', 'IS111');
INSERT INTO `g3t4`.`course_prereqs` (Course_ID, Course_prereq_ID) VALUES ('IS216', 'ES102');

DROP TABLE IF EXISTS quiz;
CREATE TABLE quiz (
    Quiz_ID varchar(100) not null,
    Time_Limit int not null,
    PRIMARY KEY (Quiz_ID)
)engine=innoDB;
INSERT INTO `g3t4`.`quiz` (Quiz_ID, Time_Limit) VALUES ('IS111-1-1','15');
INSERT INTO `g3t4`.`quiz` (Quiz_ID, Time_Limit) VALUES ('IS111-1-2','60');

DROP TABLE IF EXISTS question;
CREATE TABLE question (
	Quiz_ID varchar(100) not null, -- each quiz got its own unique id
    Question_ID int not null , -- each quiz has few questions, where each question have unique id
    Question_Name tinytext, -- this is the question itself, attached to a question id (question title)
    Question_Type int not null, -- 1: MCQ, 2: T/F
    Answer varchar(255) not null,
    constraint PK_Question primary key (Quiz_ID, Question_ID),
    foreign key (Quiz_ID) references quiz(Quiz_ID) on delete cascade on update cascade
)engine=innoDB;

INSERT INTO `g3t4`.`question` (Quiz_ID, Question_ID, Question_Name, Question_Type, Answer) VALUES ('IS111-1-1', '1', 'What is 1 + 999?', '1', '1000'); -- changed to fit MCQ_Options
INSERT INTO `g3t4`.`question` (Quiz_ID, Question_ID, Question_Name, Question_Type, Answer) VALUES ('IS111-1-1', '2', 'printf(\"hihi\"). What is the output?', '1', 'hihi');
INSERT INTO `g3t4`.`question` (Quiz_ID, Question_ID, Question_Name, Question_Type, Answer) VALUES ('IS111-1-2', '1', 'Web App is the fundamental.', '2', 'true');

DROP TABLE IF EXISTS course_class;
CREATE TABLE course_class (
	Course_ID varchar(15) not null,
    Class_ID int not null,
    Trainer_ID int not null, # set to 0 if no trainer has been assigned yet.
    Class_Start date not null,
    Class_End date not null,
    Size_Limit int,
    Reg_Start date not null,
    Reg_End date not null,
    Final_Quiz_ID varchar(100),
    constraint PK_Class primary key (Course_ID, Class_ID),
    foreign key (Course_ID) references courses(Course_ID) on delete cascade on update cascade,
    foreign key (Final_Quiz_ID) references quiz(Quiz_ID)
)engine=innoDB;


INSERT INTO `g3t4`.`course_class` (Course_ID, Class_ID, Trainer_ID, Class_Start, Class_End, Size_Limit, Reg_Start, Reg_End, Final_Quiz_ID) VALUES ('ES102', '1', '2', '2021-09-29', '2021-10-20', '40', '2021-09-10', '2021-09-13', null);
INSERT INTO `g3t4`.`course_class` (Course_ID, Class_ID, Trainer_ID, Class_Start, Class_End, Size_Limit, Reg_Start, Reg_End, Final_Quiz_ID) VALUES ('ES102', '2', '2', '2021-10-27', '2021-11-20', '35', '2021-10-20', '2021-10-15', null);
INSERT INTO `g3t4`.`course_class` (Course_ID, Class_ID, Trainer_ID, Class_Start, Class_End, Size_Limit, Reg_Start, Reg_End, Final_Quiz_ID) VALUES ('IS216', '1', '4', '2021-10-27', '2021-11-20', '40', '2021-10-20', '2021-10-15', null);
INSERT INTO `g3t4`.`course_class` (Course_ID, Class_ID, Trainer_ID, Class_Start, Class_End, Size_Limit, Reg_Start, Reg_End, Final_Quiz_ID) VALUES ('IS111', '1', '4', '2021-10-27', '2021-11-20', '40', '2021-10-20', '2021-10-15', null);

DROP TABLE IF EXISTS sections;
CREATE TABLE sections (
	Course_ID varchar(15) not null,
    Class_ID int not null,
    Section_ID int not null,
    Description tinytext,
    Quiz_ID varchar(100),
    constraint PK_Section primary key (Course_ID, Class_ID, Section_ID),
    foreign key (Course_ID, Class_ID) references course_class(Course_ID, Class_ID) on delete cascade on update cascade,
    foreign key (Quiz_ID) references quiz(Quiz_ID) on delete cascade on update cascade
)engine=innoDB;

INSERT INTO `g3t4`.`sections` (Course_ID, Class_ID, Section_ID, Description, Quiz_ID) VALUES ('IS111', '1', '1', 'Intro to Programming Part 1', 'IS111-1-1');
INSERT INTO `g3t4`.`sections` (Course_ID, Class_ID, Section_ID, Description, Quiz_ID) VALUES ('IS111', '1', '2', 'Intro to Programming Part 2', 'IS111-1-2');

DROP TABLE IF EXISTS section_course_materials;
CREATE TABLE section_course_materials (
	Course_ID varchar(15) not null,
    Class_ID int not null,
    Section_ID int not null,
    Course_Material_Name varchar(200) not null,
    Course_Material BINARY(255) not null,
    constraint PK primary key (Course_ID, Class_ID, Section_ID,Course_Material),
    foreign key (Course_ID, Class_ID, Section_ID) references sections(Course_ID, Class_ID, Section_ID) on delete cascade on update cascade
)engine=innoDB;

DROP TABLE IF EXISTS mcq_options;
-- if mcq, otherwise question wont have any rows here??? or one row?
CREATE TABLE mcq_options (
	Quiz_ID varchar(100) not null, -- one row for each question option
    Question_ID int not null, -- 1 if the option is the answer, else 0
    Question_Option varchar(25) not null,
    constraint PK_Option primary key (Quiz_ID, Question_ID, Question_Option),
    foreign key (Quiz_ID, Question_ID) references question(Quiz_ID, Question_ID) on delete cascade on update cascade
)engine=innoDB;

INSERT INTO `g3t4`.`mcq_options` (Quiz_ID, Question_ID, Question_Option) VALUES ('IS111-1-1', '1', '33');
INSERT INTO `g3t4`.`mcq_options` (Quiz_ID, Question_ID, Question_Option) VALUES ('IS111-1-1', '1', '55');
INSERT INTO `g3t4`.`mcq_options` (Quiz_ID, Question_ID, Question_Option) VALUES ('IS111-1-1', '1', '1000'); -- correct answer
INSERT INTO `g3t4`.`mcq_options` (Quiz_ID, Question_ID, Question_Option) VALUES ('IS111-1-1', '2', 'hihi'); -- correct answer
INSERT INTO `g3t4`.`mcq_options` (Quiz_ID, Question_ID, Question_Option) VALUES ('IS111-1-1', '2', 'bibi');
INSERT INTO `g3t4`.`mcq_options` (Quiz_ID, Question_ID, Question_Option) VALUES ('IS111-1-1', '2', 'lili');
INSERT INTO `g3t4`.`mcq_options` (Quiz_ID, Question_ID, Question_Option) VALUES ('IS111-1-2', '1', 'true'); -- new line for testing
INSERT INTO `g3t4`.`mcq_options` (Quiz_ID, Question_ID, Question_Option) VALUES ('IS111-1-2', '1', 'false'); -- new line for testing

DROP TABLE IF EXISTS engineer_course_enrolment;
CREATE TABLE engineer_course_enrolment (
	Course_ID varchar(15) not null,
    Class_ID int not null, # 0 if user is not enrolled / completed
    User_ID int not null,
    Course_Status varchar(255), # enrolled / completed / ineligible / eligible / pending
    Score int default 0, # Updated once they have taken final quiz
    constraint PK_Enrolled primary key (Course_ID, Class_ID, User_ID),
    foreign key (Course_ID) references courses(Course_ID) on delete cascade on update cascade,
    foreign key (User_ID) references users(User_ID) on delete cascade on update cascade
)engine=innoDB;

INSERT INTO `g3t4`.`engineer_course_enrolment` (Course_ID, Class_ID, User_ID, Course_Status) VALUES ('ES102', '0', '1', 'eligible');
INSERT INTO `g3t4`.`engineer_course_enrolment` (Course_ID, Class_ID, User_ID, Course_Status) VALUES ('IS111', '0', '1', 'eligible');
INSERT INTO `g3t4`.`engineer_course_enrolment` (Course_ID, Class_ID, User_ID, Course_Status) VALUES ('IS216', '0', '1', 'ineligible');
INSERT INTO `g3t4`.`engineer_course_enrolment` (Course_ID, Class_ID, User_ID, Course_Status) VALUES ('IS111', '0', '3', 'eligible');
INSERT INTO `g3t4`.`engineer_course_enrolment` (Course_ID, Class_ID, User_ID, Course_Status) VALUES ('ES102', '0', '3', 'eligible');
INSERT INTO `g3t4`.`engineer_course_enrolment` (Course_ID, Class_ID, User_ID, Course_Status) VALUES ('IS216', '0', '3', 'ineligible');
INSERT INTO `g3t4`.`engineer_course_enrolment` (Course_ID, Class_ID, User_ID, Course_Status) VALUES ('IS111', '0', '6', 'eligible');
INSERT INTO `g3t4`.`engineer_course_enrolment` (Course_ID, Class_ID, User_ID, Course_Status) VALUES ('ES102', '0', '6', 'eligible');
INSERT INTO `g3t4`.`engineer_course_enrolment` (Course_ID, Class_ID, User_ID, Course_Status) VALUES ('IS216', '0', '6', 'ineligible');


DROP TABLE IF EXISTS engineer_course_section;
-- need to rename this table to a more intuitive name (easier to understand name)
CREATE TABLE engineer_course_section (
	Course_ID varchar(15) not null,
    Class_ID int not null,
    User_ID int not null,
    Section_ID int not null,
    Section_Status varchar(255), -- incomplete / complete / unavailable
    constraint PK_Enrolled_Section primary key (Course_ID, Class_ID, Section_ID, User_ID),
    foreign key (Course_ID, Class_ID, User_ID) references engineer_course_enrolment (Course_ID, Class_ID, User_ID) on delete cascade on update cascade,
    foreign key (Course_ID, Class_ID, Section_ID) references sections (Course_ID, Class_ID, Section_ID) on delete cascade on update cascade
)engine=innoDB;


DROP TABLE IF EXISTS quiz_user;
CREATE TABLE quiz_user (
	Quiz_ID varchar(100) not null,
    Question_ID int not null,
    User_ID int not null,
    User_Answer varchar(255),
    constraint PK_User_Answer primary key (Quiz_ID, Question_ID, User_ID),
    foreign key (Quiz_ID, Question_ID) references question (Quiz_ID, Question_ID) on delete cascade on update cascade,
    foreign key (User_ID) references users(User_ID) on delete cascade on update cascade
    -- foreign key (User_ID) references User (User_ID) -- changed to Engineer_Course_Section (User_ID) also doesnt work
)engine=innoDB;


DROP TABLE IF EXISTS thread;
CREATE TABLE thread (
	Thread_ID int not null auto_increment,
    User_ID int not null,
    Subject tinytext not null,
    Description tinytext,
    Created_At datetime default current_timestamp,
    Likes int,
    primary key (Thread_ID),
    foreign key (User_ID) references users(User_ID) on update cascade
)engine=innoDB;

INSERT INTO `g3t4`.`thread` (Thread_ID, User_ID, Subject, Description, Created_At, Likes) VALUES ('1', '1', 'Help in Python IS101', 'Idk how to do thsee please teach me', '2021-10-04', '5');

DROP TABLE IF EXISTS badgeDB;
-- or rather i feel the badgedb should contain the respective badges picture,
-- along with the badges pre-req aka courses/sections to be completed to receive the badge
-- and not sure about the HR approving a user getting the badge --> is this a step required in the project brief? 
CREATE TABLE badgeDB (
  Course_ID varchar(15) not null,
  User_ID INT NOT NULL,
  Badge_Name VARCHAR(45) NOT NULL,
  Badge_Info VARCHAR(225) NOT NULL, 
  PRIMARY KEY (Course_ID, User_ID),
  FOREIGN KEY (Course_ID) REFERENCES courses(Course_ID),
  FOREIGN KEY (User_ID) REFERENCES users(User_ID)
)engine=innoDB;