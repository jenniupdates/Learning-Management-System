-- DROP DATABASE IF EXISTS `g3t4`;
-- CREATE DATABASE `g3t4`;
-- USE `g3t4`;
DROP TABLE IF EXISTS Users;
CREATE TABLE Users (
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

INSERT INTO `g3t4`.`Users` (Name, Username, Password, UserType, Designation, Department) VALUES ('Richard',  'RG', 'r_pass', '1', 'designee', 'operations');
INSERT INTO `g3t4`.`Users` (Name, Username, Password, UserType, Designation, Department) VALUES ('YS',  'YS', 'ys_pass', '2', 'designee', 'operations');
INSERT INTO `g3t4`.`Users` (Name, Username, Password, UserType, Designation, Department) VALUES ('Stephen',  'S', 's_pass', '1', 'designee', 'servicing');
INSERT INTO `g3t4`.`Users` (Name, Username, Password, UserType, Designation, Department) VALUES ('Isaac',  'I', 'i_pass', '2', 'designee', 'servicing');
INSERT INTO `g3t4`.`Users` (Name, Username, Password, UserType, Designation, Department) VALUES ('Chee Kuang',  'CK', 'ck_pass', '3', 'designee', 'human resource');
INSERT INTO `g3t4`.`Users` (Name, Username, Password, UserType, Designation, Department) VALUES ('Sarah',  'Sara', 'sara_pass', '1', 'designee', 'engineer');

DROP TABLE IF EXISTS Courses;
CREATE TABLE Courses (
	Course_ID varchar(15) not null,
    Course_Name varchar(255) not null,
    Course_Outline varchar(255),
    primary key (Course_ID)
)engine=innoDB;

INSERT INTO `g3t4`.`Courses` (Course_ID, Course_Name, Course_Outline) VALUES ('ES102', 'Intro to Engineering', 'The basics of engineering');
INSERT INTO `g3t4`.`Courses` (Course_ID, Course_Name, Course_Outline) VALUES ('IS111', 'Intro to Progamming', 'Python Program helps you to python');
INSERT INTO `g3t4`.`Courses` (Course_ID, Course_Name, Course_Outline) VALUES ('IS216', 'Web Development I', 'Web Development for Beginners');

DROP TABLE IF EXISTS Course_prereqs;
CREATE TABLE Course_prereqs (
	Course_ID varchar(15) not null,
    Course_prereq_ID varchar(15) not null,
    -- list of courseid required to be completed before eligible for the course
    constraint PK_Prereq primary key (Course_ID, Course_prereq_ID),
 	foreign key (Course_ID) references Courses(Course_ID) on delete cascade on update cascade,
    foreign key (Course_prereq_ID) references Courses(Course_ID) on delete cascade on update cascade
--     foreign key (Course_prereq_ID) references Courses(Course_ID)
)engine=innoDB;

INSERT INTO `g3t4`.`course_prereqs` (Course_ID, Course_prereq_ID) VALUES ('IS216', 'IS111');
INSERT INTO `g3t4`.`course_prereqs` (Course_ID, Course_prereq_ID) VALUES ('IS216', 'ES102');

DROP TABLE IF EXISTS Quiz;
CREATE TABLE Quiz (
    Quiz_ID varchar(100) not null,
    Time_Limit int not null,
    PRIMARY KEY (Quiz_ID)
)engine=innoDB;
INSERT INTO `g3t4`.`quiz` (Quiz_ID, Time_Limit) VALUES ('IS111-1-1','15');
INSERT INTO `g3t4`.`quiz` (Quiz_ID, Time_Limit) VALUES ('IS111-1-2','60');

DROP TABLE IF EXISTS Question;
CREATE TABLE Question (
	Quiz_ID varchar(100) not null, -- each quiz got its own unique id
    Question_ID int not null , -- each quiz has few questions, where each question have unique id
    Question_Name tinytext, -- this is the question itself, attached to a question id (question title)
    Question_Type int not null, -- 1: MCQ, 2: T/F
    Answer varchar(255) not null,
    constraint PK_Question primary key (Quiz_ID, Question_ID),
    foreign key (Quiz_ID) references Quiz(Quiz_ID) on delete cascade on update cascade
)engine=innoDB;

INSERT INTO `g3t4`.`question` (Quiz_ID, Question_ID, Question_Name, Question_Type, Answer) VALUES ('IS111-1-1', '1', 'What is x * y', '1', '1000'); -- changed to fit MCQ_Options
INSERT INTO `g3t4`.`question` (Quiz_ID, Question_ID, Question_Name, Question_Type, Answer) VALUES ('IS111-1-1', '2', 'printf(\"hihi\")', '1', 'hihi');
INSERT INTO `g3t4`.`question` (Quiz_ID, Question_ID, Question_Name, Question_Type, Answer) VALUES ('IS111-1-2', '1', 'WAD2ishard', '2', 'T');

DROP TABLE IF EXISTS Course_Class;
CREATE TABLE Course_Class (
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
    foreign key (Course_ID) references Courses(Course_ID) on delete cascade on update cascade,
    foreign key (Final_Quiz_ID) references Quiz(Quiz_ID)
)engine=innoDB;


INSERT INTO `g3t4`.`course_class` (Course_ID, Class_ID, Trainer_ID, Class_Start, Class_End, Size_Limit, Reg_Start, Reg_End, Final_Quiz_ID) VALUES ('ES102', '1', '2', '2021-09-29', '2021-10-20', '40', '2021-09-10', '2021-09-13', null);
INSERT INTO `g3t4`.`course_class` (Course_ID, Class_ID, Trainer_ID, Class_Start, Class_End, Size_Limit, Reg_Start, Reg_End, Final_Quiz_ID) VALUES ('ES102', '2', '2', '2021-10-27', '2021-11-20', '35', '2021-10-20', '2021-10-15', null);
INSERT INTO `g3t4`.`course_class` (Course_ID, Class_ID, Trainer_ID, Class_Start, Class_End, Size_Limit, Reg_Start, Reg_End, Final_Quiz_ID) VALUES ('IS216', '1', '4', '2021-10-27', '2021-11-20', '40', '2021-10-20', '2021-10-15', null);
INSERT INTO `g3t4`.`course_class` (Course_ID, Class_ID, Trainer_ID, Class_Start, Class_End, Size_Limit, Reg_Start, Reg_End, Final_Quiz_ID) VALUES ('IS111', '1', '4', '2021-10-27', '2021-11-20', '40', '2021-10-20', '2021-10-15', null);

DROP TABLE IF EXISTS Sections;
CREATE TABLE Sections (
	Course_ID varchar(15) not null,
    Class_ID int not null,
    Section_ID int not null,
    Description tinytext,
    Quiz_ID varchar(100),
    constraint PK_Section primary key (Course_ID, Class_ID, Section_ID),
    foreign key (Course_ID, Class_ID) references Course_Class(Course_ID, Class_ID) on delete cascade on update cascade,
    foreign key (Quiz_ID) references Quiz(Quiz_ID) on delete cascade on update cascade
)engine=innoDB;

INSERT INTO `g3t4`.`sections` (Course_ID, Class_ID, Section_ID, Description, Quiz_ID) VALUES ('IS111', '1', '1', 'Intro to Programming Part 1', 'IS111-1-1');
INSERT INTO `g3t4`.`sections` (Course_ID, Class_ID, Section_ID, Description, Quiz_ID) VALUES ('IS111', '1', '2', 'Intro to Programming Part 2', 'IS111-1-2');

DROP TABLE IF EXISTS Section_Course_Materials;
CREATE TABLE Section_Course_Materials (
	Course_ID varchar(15) not null,
    Class_ID int not null,
    Section_ID int not null,
    Course_Material_Name varchar(200) not null,
    Course_Material BINARY(255) not null,
    constraint PK primary key (Course_ID, Class_ID, Section_ID,Course_Material),
    foreign key (Course_ID, Class_ID, Section_ID) references Sections(Course_ID, Class_ID, Section_ID) on delete cascade on update cascade
)engine=innoDB;

DROP TABLE IF EXISTS MCQ_Options;
-- if mcq, otherwise question wont have any rows here??? or one row?
CREATE TABLE MCQ_Options (
	Quiz_ID varchar(100) not null, -- one row for each question option
    Question_ID int not null, -- 1 if the option is the answer, else 0
    Question_Option varchar(25) not null,
    constraint PK_Option primary key (Quiz_ID, Question_ID, Question_Option),
    foreign key (Quiz_ID, Question_ID) references Question(Quiz_ID, Question_ID) on delete cascade on update cascade
)engine=innoDB;

INSERT INTO `g3t4`.`mcq_options` (Quiz_ID, Question_ID, Question_Option) VALUES ('IS111-1-1', '1', '33');
INSERT INTO `g3t4`.`mcq_options` (Quiz_ID, Question_ID, Question_Option) VALUES ('IS111-1-1', '1', '55');
INSERT INTO `g3t4`.`mcq_options` (Quiz_ID, Question_ID, Question_Option) VALUES ('IS111-1-1', '1', '1000'); -- correct answer
INSERT INTO `g3t4`.`mcq_options` (Quiz_ID, Question_ID, Question_Option) VALUES ('IS111-1-1', '2', 'hihi'); -- correct answer
INSERT INTO `g3t4`.`mcq_options` (Quiz_ID, Question_ID, Question_Option) VALUES ('IS111-1-1', '2', 'bibi');
INSERT INTO `g3t4`.`mcq_options` (Quiz_ID, Question_ID, Question_Option) VALUES ('IS111-1-1', '2', 'lili');
INSERT INTO `g3t4`.`mcq_options` (Quiz_ID, Question_ID, Question_Option) VALUES ('IS111-1-2', '1', 'T'); -- new line for testing
INSERT INTO `g3t4`.`mcq_options` (Quiz_ID, Question_ID, Question_Option) VALUES ('IS111-1-2', '1', 'F'); -- new line for testing

DROP TABLE IF EXISTS Engineer_Course_Enrolment;
CREATE TABLE Engineer_Course_Enrolment (
	Course_ID varchar(15) not null,
    Class_ID int not null, # 0 if user is not enrolled / completed
    User_ID int not null,
    Course_Status varchar(255), # enrolled / completed / ineligible / eligible / pending
    Score int default 0, # Updated once they have taken final quiz
    constraint PK_Enrolled primary key (Course_ID, Class_ID, User_ID),
    foreign key (Course_ID) references Courses(Course_ID) on delete cascade on update cascade,
    foreign key (User_ID) references Users(User_ID) on delete cascade on update cascade
)engine=innoDB;

INSERT INTO `g3t4`.`engineer_course_enrolment` (Course_ID, Class_ID, User_ID, Course_Status) VALUES ('ES102', '1', '1', 'completed');
INSERT INTO `g3t4`.`engineer_course_enrolment` (Course_ID, Class_ID, User_ID, Course_Status) VALUES ('IS111', '1', '1', 'completed');
INSERT INTO `g3t4`.`engineer_course_enrolment` (Course_ID, Class_ID, User_ID, Course_Status) VALUES ('IS216', '0', '1', 'eligible');
INSERT INTO `g3t4`.`engineer_course_enrolment` (Course_ID, Class_ID, User_ID, Course_Status) VALUES ('IS111', '1', '3', 'enrolled');
INSERT INTO `g3t4`.`engineer_course_enrolment` (Course_ID, Class_ID, User_ID, Course_Status) VALUES ('ES102', '1', '3', 'pending');
INSERT INTO `g3t4`.`engineer_course_enrolment` (Course_ID, Class_ID, User_ID, Course_Status) VALUES ('IS216', '0', '3', 'ineligible');
INSERT INTO `g3t4`.`engineer_course_enrolment` (Course_ID, Class_ID, User_ID, Course_Status) VALUES ('IS111', '0', '6', 'eligible');
INSERT INTO `g3t4`.`engineer_course_enrolment` (Course_ID, Class_ID, User_ID, Course_Status) VALUES ('ES102', '2', '6', 'pending');
INSERT INTO `g3t4`.`engineer_course_enrolment` (Course_ID, Class_ID, User_ID, Course_Status) VALUES ('IS216', '0', '6', 'ineligible');


DROP TABLE IF EXISTS Engineer_Course_Section;
-- need to rename this table to a more intuitive name (easier to understand name)
CREATE TABLE Engineer_Course_Section (
	Course_ID varchar(15) not null,
    Class_ID int not null,
    User_ID int not null,
    Section_ID int not null,
    Section_Status varchar(255), -- incomplete / complete / unavailable
    constraint PK_Enrolled_Section primary key (Course_ID, Class_ID, Section_ID, User_ID),
    foreign key (Course_ID, Class_ID, User_ID) references Engineer_Course_Enrolment (Course_ID, Class_ID, User_ID) on delete cascade on update cascade,
    foreign key (Course_ID, Class_ID, Section_ID) references Sections (Course_ID, Class_ID, Section_ID) on delete cascade on update cascade
)engine=innoDB;

INSERT INTO `g3t4`.`engineer_course_section` (Course_ID, Class_ID, User_ID, Section_ID, Section_Status) VALUES ('IS111', '1', '1', '1', 'incomplete');
INSERT INTO `g3t4`.`engineer_course_section` (Course_ID, Class_ID, User_ID, Section_ID, Section_Status) VALUES ('IS111', '1', '1', '2', 'unavailable');

DROP TABLE IF EXISTS Quiz_User;
CREATE TABLE Quiz_User (
	Quiz_ID varchar(100) not null,
    Question_ID int not null,
    User_ID int not null,
    User_Answer varchar(255),
    constraint PK_User_Answer primary key (Quiz_ID, Question_ID, User_ID),
    foreign key (Quiz_ID, Question_ID) references Question (Quiz_ID, Question_ID) on delete cascade on update cascade,
    foreign key (User_ID) references Users(User_ID) on delete cascade on update cascade
    -- foreign key (User_ID) references User (User_ID) -- changed to Engineer_Course_Section (User_ID) also doesnt work
)engine=innoDB;

INSERT INTO `g3t4`.`Quiz_User` (Quiz_ID, Question_ID, User_ID, User_Answer) VALUES ('IS111-1-1', '1', '1', '3');

DROP TABLE IF EXISTS Thread;
CREATE TABLE Thread (
	Thread_ID int not null auto_increment,
    User_ID int not null,
    Subject tinytext not null,
    Description tinytext,
    Created_At datetime default current_timestamp,
    Likes int,
    primary key (Thread_ID),
    foreign key (User_ID) references Users(User_ID) on update cascade
)engine=innoDB;

INSERT INTO `g3t4`.`thread` (Thread_ID, User_ID, Subject, Description, Created_At, Likes) VALUES ('1', '1', 'Help in Python IS101', 'Idk how to do thsee please teach me', '2021-10-04', '5');

DROP TABLE IF EXISTS BadgeDB;
-- or rather i feel the badgedb should contain the respective badges picture,
-- along with the badges pre-req aka courses/sections to be completed to receive the badge
-- and not sure about the HR approving a user getting the badge --> is this a step required in the project brief? 
CREATE TABLE BadgeDB (
  Course_ID varchar(15) not null,
  User_ID INT NOT NULL,
  Badge_Name VARCHAR(45) NOT NULL,
  Badge_Info VARCHAR(225) NOT NULL, 
  PRIMARY KEY (Course_ID, User_ID),
  FOREIGN KEY (Course_ID) REFERENCES Courses(Course_ID),
  FOREIGN KEY (User_ID) REFERENCES Users(User_ID)
)engine=innoDB;
