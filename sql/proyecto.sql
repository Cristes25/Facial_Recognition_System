create database university_attendece;
use university_attendece;


create table students (
student_id int auto_increment primary key not null,
student_firstname varchar(20) not null,
student_lastname varchar(20) not null,  
student_email varchar(40)
);

create table student_images (
image_id int auto_increment primary key,
student_id int not null,
image_name varchar(50), -- optional, to describe the image (e.g., "with glasses", "without glasses")
student_picture longblob not null,
foreign key (student_id) references students(student_id)
);

create table professors (
professor_id int auto_increment primary key not null,
professor_firstname varchar(20) not null, 
professor_lastname varchar(20) not null,
professor_email varchar(50) not null
);

create table courses (
course_code varchar(20) primary key not null, #change to varchar(15)
course_name varchar(20),
start_date date,
end_date date,
professor_id int,
foreign key (professor_id) references professors(professor_id)
);

create table building (
building_code varchar(10) primary key not null,
classroom varchar(10) not null
);

create table classroom (
classroom_name varchar(15) primary key not null,
building_code varchar(10),
capacity int,
foreign key (building_code) references building(building_code)
);
#work only with lab and E building (insesrts)

create table course_enrollment (
enrollment_id int auto_increment primary key,
class_group int not null, #add this shit
student_id int not null,
course_code varchar(20) not null,
enrollment_date date,
foreign key (student_id) references students(student_id),
foreign key (course_code) references courses(course_code)
);

create table schedules (
schedule_id int auto_increment primary key,
course_code varchar(20) not null,
classroom_name varchar(15),
day_of_week enum('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'),
start_time time,
end_time time,
student_id int not null, #add the coneection with students table
foreign key (classroom_name) references classroom(classroom_name),
foreign key (course_code) references courses(course_code),
foreign key (student_id) references students(student_id)
);

create table attendance (
record_id int auto_increment primary key,
student_id int not null,
course_code varchar(20) not null,
attendance_date date not null,
status enum('Present', 'Absent', 'Late') default 'Absent',
foreign key (student_id) references students(student_id),
foreign key (course_code) references courses(course_code)
);

create table year(
Year year primary key
);

create table semester(
period enum ('Spring', 'Summer', 'Fall'),
year year,
schedule_id int, 
foreign key (schedule_id) references schedules(schedule_id),
foreign key (year) references year(year)
);

insert into students(student_firstname, student_lastname, student_email)
values ('Alejandro', 'Melendez', 'ale.melendez@tu.com'); 
insert into students(student_firstname, student_lastname, student_email)
values ('Ana', 'Jimenez', 'Ana.jimenez@tu.com'); 
insert into students(student_firstname, student_lastname, student_email)
values ('Andrea', 'Nunez', 'and.nunez@tu.com');
insert into students(student_firstname, student_lastname, student_email)
values ('Clifford', 'Lacayo', 'cliff.lacayo@tu.com');
insert into students(student_firstname, student_lastname, student_email)
values ('Fernando', 'Torrez', 'fer.torrez@tu.com');   
insert into students(student_firstname, student_lastname, student_email)
values ('Gabriel', 'Pocurrull', 'gab.pocurrull@tu.com');
insert into students(student_firstname, student_lastname, student_email)
values ('Guadalupe', 'Tapia', 'lupe.tapia@tu.com');  
insert into students(student_firstname, student_lastname, student_email)
values ('Jharet', 'Herrera', 'j.herrera@tu.com');
insert into students(student_firstname, student_lastname, student_email)
values ('Josue', 'Calero', 'j.calero@tu.com');  
insert into students(student_firstname, student_lastname, student_email)
values ('Juan', 'Hernandez', 'j.hernandez@tu.com'); 
insert into students(student_firstname, student_lastname, student_email)
values ('Lester', 'Pereira', 'lest.pereira@tu.com');
insert into students(student_firstname, student_lastname, student_email)
values ('Maria', 'Martinez', 'maria.martinez@tu.com');  
insert into students(student_firstname, student_lastname, student_email)
values ('Marian', 'Urbina', 'marian.urbina@tu.com'); 
insert into students(student_firstname, student_lastname, student_email)
values ('Meriyen', 'Palacios', 'meri.palacios@tu.com'); 
insert into students(student_firstname, student_lastname, student_email)
values ('Miguel', 'Fonseca', 'miguel.fonseca@tu.com'); 
insert into students(student_firstname, student_lastname, student_email)
values ('Osvaldo', 'Rodriguez', 'osva.rodriguez@tu.com'); 
insert into students(student_firstname, student_lastname, student_email)
values ('Sharon', 'Cadenaz', 'sharon.cadenaz@tu.com'); 
insert into students(student_firstname, student_lastname, student_email)
values ('Valeria', 'Martinez', 'vale.martinez@tu.com'); 
insert into students(student_firstname, student_lastname, student_email)
values ('Viktor', 'Miranda', 'vik.miranda@tu.com'); 
insert into students(student_firstname, student_lastname, student_email)
values ('Eduardo', 'Quant', 'edu.quant@tu.com'); 
insert into students(student_firstname, student_lastname, student_email)
values ('Cristiana', 'Espinoza', 'cris.espinoza@tu.com'); 
insert into professors(professor_firstname,professor_lastname,professor_email)
values ('Tania', 'Castro', 'andrea130405@gmail.com');
insert into professors(professor_firstname,professor_lastname,professor_email)
values ('Oscar', 'Somarriba', 'crisianaespinoza256@gmail.com');
insert into courses(course_code, course_name, start_date,end_date)
values ('COP1035C','Python programming','2024-09-02', '2024-12-22' );
insert into courses(course_code, course_name, start_date,end_date)
values ('CTS1305C','Networking','2024-09-02', '2024-12-22' );
insert into courses(course_code, course_name, start_date,end_date)
values ('ISM4212','Database Management','2024-09-02','2024-12-22');
#Since I have the images stored on my (D:) drive it would be necessary to remove the restrinction on MySQL because only has access to the (C:) drive
#so I will go to the my.ini and edit the [mysqld]
#secure_file_priv = NULL so will have access to all the computer
#SHOW VARIABLES LIKE 'secure_file_priv'; #now has access to all the files
#test to insesrt the faces
insert into student_images (student_id, image_name, student_picture)
values 
(1, 'No Glasses', LOAD_FILE('D:/Clases KU/fall 24/foto alumnos/Alejandro Melendez.jfif'));
#Becuase it was succes we proced to pupulate all the students
INSERT INTO student_images (student_id, image_name, student_picture)
VALUES 
(2, 'No Glasses', LOAD_FILE('D:/Clases KU/fall 24/foto alumnos/Ana Jimez.jfif'));

INSERT INTO student_images (student_id, image_name, student_picture)
VALUES 
(3, 'With Glasses', LOAD_FILE('D:/Clases KU/fall 24/foto alumnos/Andrea Nunez lentes.jfif'));

INSERT INTO student_images (student_id, image_name, student_picture)
VALUES 
(3, 'Without Glasses', LOAD_FILE('D:/Clases KU/fall 24/foto alumnos/Andrea Nunez sin lentes.jfif'));

INSERT INTO student_images (student_id, image_name, student_picture)
VALUES 
(4, 'No glasses', LOAD_FILE('D:/Clases KU/fall 24/foto alumnos/Clifford Lacayo.jfif'));

INSERT INTO student_images (student_id, image_name, student_picture)
VALUES 
(5, 'No glasses', LOAD_FILE('D:/Clases KU/fall 24/foto alumnos/Fernando Torrez.jfif'));

INSERT INTO student_images (student_id, image_name, student_picture)
VALUES 
(6, 'Without glasses', LOAD_FILE('D:/Clases KU/fall 24/foto alumnos/Gabe Pocurrul.jfif'));

INSERT INTO student_images (student_id, image_name, student_picture)
VALUES 
(6, 'With Glasses', LOAD_FILE('D:/Clases KU/fall 24/foto alumnos/Gabriel Pocurrul con lentes.jfif'));

INSERT INTO student_images (student_id, image_name, student_picture)
VALUES 
(7, 'With Glasses', LOAD_FILE('D:/Clases KU/fall 24/foto alumnos/Guadalupe Tapia.jfif'));

INSERT INTO student_images (student_id, image_name, student_picture)
VALUES 
(8, 'without Glasses', LOAD_FILE('D:/Clases KU/fall 24/foto alumnos/Jharet Herrera sin lentes.jfif'));

INSERT INTO student_images (student_id, image_name, student_picture)
VALUES 
(8, 'With Glasses', LOAD_FILE('D:/Clases KU/fall 24/foto alumnos/Jharet Herrera lentes.jfif'));

INSERT INTO student_images (student_id, image_name, student_picture)
VALUES 
(9, 'No Glasses', LOAD_FILE('D:/Clases KU/fall 24/foto alumnos/Josue Calero.jfif'));

INSERT INTO student_images (student_id, image_name, student_picture)
VALUES 
(10, 'No Glasses', LOAD_FILE('D:/Clases KU/fall 24/foto alumnos/Juan Hernandez.jfif'));

INSERT INTO student_images (student_id, image_name, student_picture)
VALUES 
(11, 'No Glasses', LOAD_FILE('D:/Clases KU/fall 24/foto alumnos/Lester Pereira.jfif'));

INSERT INTO student_images (student_id, image_name, student_picture)
VALUES 
(12, 'No Glasses', LOAD_FILE('D:/Clases KU/fall 24/foto alumnos/Maria Martinez.jfif'));

INSERT INTO student_images (student_id, image_name, student_picture)
VALUES 
(13, 'No Glasses', LOAD_FILE('D:/Clases KU/fall 24/foto alumnos/Marian Urbina.jfif'));

INSERT INTO student_images (student_id, image_name, student_picture)
VALUES 
(14, 'No Glasses', LOAD_FILE('D:/Clases KU/fall 24/foto alumnos/Meriyen Palacios.jfif'));

INSERT INTO student_images (student_id, image_name, student_picture)
VALUES 
(15, 'No Glasses', LOAD_FILE('D:/Clases KU/fall 24/foto alumnos/Miguel Fonseca.jfif'));

INSERT INTO student_images (student_id, image_name, student_picture)
VALUES 
(16, 'No Glasses', LOAD_FILE('D:/Clases KU/fall 24/foto alumnos/Osvaldo Rodriguez.jfif'));

INSERT INTO student_images (student_id, image_name, student_picture)
VALUES 
(17, 'No Glasses', LOAD_FILE('D:/Clases KU/fall 24/foto alumnos/Sharon Cadenas.jfif'));

INSERT INTO student_images (student_id, image_name, student_picture)
VALUES 
(18, 'Without Glasses', LOAD_FILE('D:/Clases KU/fall 24/foto alumnos/Valeria Martinez.jfif'));

INSERT INTO student_images (student_id, image_name, student_picture)
VALUES 
(18, 'With Glasses', LOAD_FILE('D:/Clases KU/fall 24/foto alumnos/Valeria Martines lentes.jfif'));

INSERT INTO student_images (student_id, image_name, student_picture)
VALUES 
(19, 'No Glasses', LOAD_FILE('D:/Clases KU/fall 24/foto alumnos/Vikor Miranda.jfif'));

INSERT INTO student_images (student_id, image_name, student_picture)
VALUES 
(20, 'With Glasses', LOAD_FILE('D:/Clases KU/fall 24/foto alumnos/Eduardo Quant con lentes.jfif'));

INSERT INTO student_images (student_id, image_name, student_picture)
VALUES 
(20, 'Without Glasses', LOAD_FILE('D:/Clases KU/fall 24/foto alumnos/Eduardo Quant.jfif'));

INSERT INTO student_images (student_id, image_name, student_picture)
VALUES 
(21, 'With Glasses', LOAD_FILE('D:/Clases KU/fall 24/foto alumnos/Cristiana Espinoza.jfif'));

INSERT INTO student_images (student_id, image_name, student_picture)
VALUES 
(21, 'Without Glasses', LOAD_FILE('D:/Clases KU/fall 24/foto alumnos/Cristiana Espinoza sin lentes.jfif'));


insert into building(building_code)
values ('E');

insert into building(building_code)
values ('Lab');

insert into building(building_code)
values ('F');

insert into building(building_code)
values ('sb');

insert into year (year)
values (2024);

UPDATE courses
SET professor_id = 1  
WHERE course_code = 'COP1035C';

UPDATE courses
SET professor_id = 2 
WHERE course_code = 'CTS1305C';

UPDATE courses
SET professor_id = 1 
WHERE course_code = 'ISM4212';

create table student_schedule(
student_schedule_id int auto_increment primary key not null, 
student_id int not null, 
schedule_id int not null,
foreign key(student_id) references students(student_id),
foreign key(schedule_id) references schedules(schedule_id)
);

-- droping student_id from schedules 
ALTER TABLE schedules DROP FOREIGN KEY schedules_ibfk_3;
ALTER TABLE schedules DROP COLUMN student_id;
-- droping course code from attendence and connecting with schedules
ALTER TABLE attendance DROP FOREIGN KEY attendance_ibfk_2;
ALTER TABLE attendance DROP COLUMN course_code;
-- addinng schedule id int attendance 
ALTER TABLE attendance ADD COLUMN schedule_id INT NOT NULL;
ALTER TABLE attendance ADD CONSTRAINT fk_schedule FOREIGN KEY (schedule_id) REFERENCES schedules(schedule_id);





