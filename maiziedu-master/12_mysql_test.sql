-- 设计一个学生成绩数据库，该库包含学生，老师，课程和成绩等信息并完成后面的练习(注意主外键关系)。
CREATE DATABASE IF NOT EXISTS `Study` DEFAULT CHARACTER SET 'UTF8';
USE `Study`;

-- 学生表students：
--学号（SNO）
--姓名(SNAME)
--性别(SSEX)
--生日(SBIRTHDAY )
--所属班级(CLASS )
CREATE TABLE IF NOT EXISTS `students`(
sno SMALLINT,
sname VARCHAR(20),
sex ENUM('男','女','保密'),
sbirthday YEAR,
class TINYINT(1) COMMENT '一共有6个班'
)ENGINE=INNODB CHARSET=UTF8;
--忘记添加主键了，加入sno为主键
ALTER TABLE students ADD PRIMARY KEY(sno);
-- 课程：courses
--课程编号(CNO)
--课程名(CNAME
--授课老师(TNO)
CREATE TABLE IF NOT EXISTS `courses`(
cno SMALLINT PRIMARY KEY,
cname VARCHAR(20),
tno TINYINT(1) COMMENT '一共有8个老师'
)ENGINE=INNODB CHARSET=UTF8;
-- 成绩：SCORE
-- 学号(SNO)
-- 课程编号(CNO)
-- 得分(DEGREE)
CREATE TABLE IF NOT EXISTS `score`(
sno SMALLINT,
cno VARCHAR(20),
degree TINYINT(1) COMMENT '满分100'
)ENGINE=INNODB CHARSET=UTF8;
-- 老师：teachers
-- 教师编号(TNO)
-- 教师姓名(TNAME)
-- 性别(TSSEX)
-- 生日(TBIRTHDAY)
-- 职称(TITLE)
-- 单位科室（DEPART）
CREATE TABLE IF NOT EXISTS `teachers`(
tno SMALLINT  PRIMARY KEY,
tname VARCHAR(20),
tsex ENUM('男','女'),
tbirthday YEAR,
title VARCHAR(20),
depart TINYINT(1) 
)ENGINE=INNODB CHARSET=UTF8;



--要求：
-- 一、每张表使用sql语句插入至少10条数据
-- 学生插入12条信息
INSERT students VALUES
(6,'李明','男','2005',1),
(7,'张一','男','2004',2),
(9,'刘欢','男','2006',2),
(11,'王丽','女','2003',3),
(13,'徐起','男','2007',3),
(45,'严嫣','女','2006',2),
(78,'赵丽颖','女','2005',4),
(90,'何馨','女','2006',5),
(23,'王齐','男','2004',5),
(19,'徐明','男','2006',6),
(80,'陈松','男','2005',6),
(17,'杨桦','女','2005',4);

-- 课程添加十条信息
INSERT courses VALUES
(1,'语文',1),
(2,'数学',2),
(3,'英语',3),
(4,'历史',4),
(5,'地理',5),
(6,'生物',6),
(7,'化学',7),
(8,'物理',8),
(9,'政治',9),
(10,'体育',10);

-- 成绩添加20条记录
INSERT score VALUES
(6,1,95),
(6,2,88),
(13,2,92),
(45,5,78),
(78,8,85),
(90,9,92),
(23,10,85),
(19,3,87),
(80,8,88),
(17,4,89),
(7,5,94),
(9,7,97),
(11,6,75),
(13,8,90),
(45,9,94),
(78,4,84),
(19,8,58),
(80,10,89),
(17,4,47),
(23,3,32);

-- 教师添加10条记录
--还要将部门字段改为字符类型
ALTER TABLE teachers MODIFY depart VARCHAR(30);
INSERT teachers VALUES
(12,'王军','男',1985,'教师','教学部'),
(22,'李琴','女',1982,'教师','教学部'),
(42,'陈球','男',1984,'教师','教学部'),
(23,'张蓉','女',1975,'主任','教学部'),
(56,'郭芳','女',1965,'部长','教务部'),
(78,'刘萍','女',1989,'教师','教学部'),
(26,'秦进','男',1993,'助教','教学部'),
(89,'王凯','男',1983,'主任','教务部'),
(34,'赵建','男',1987,'教师','教学部'),
(19,'陈明','男',1981,'助教','教学部');




--二、完成以下查询题目：
--1、 查询Student表中的所有记录的Sname、Ssex和Class列。
SELECT sname,sex,class FROM students; 
--2、 查询教师所有的单位即不重复的Depart列。
SELECT distinct depart FROM teachers; 
--3、 查询Student表的所有记录。
SELECT * FROM students;
--4、 查询Score表中成绩在60到80之间的所有记录。
SELECT * FROM score WHERE degree BETWEEN 60 AND 80;
--5、 查询Score表中成绩为85，86或88的记录。
SELECT * FROM score WHERE degree IN (85,86,88);
-- 6、 查询Student表中“5”班或性别为“女”的同学记录。
SELECT * FROM students WHERE class = 5 OR sex = '女';
-- 7、 以Class降序查询Student表的所有记录。
SELECT * FROM students ORDER BY class DESC;
--8、 以Cno升序、Degree降序查询Score表的所有记录。
SELECT * FROM score ORDER BY cno,degree DESC;
-- 9、 查询“1”班的学生人数。
SELECT COUNT(*) FROM students WHERE class = 1;
-- 10、查询Score表中的最高分的学生学号和课程号。
SELECT sno,cno FROM score WHERE degree = (SELECT MAX(degree) FROM score);
--11、查询‘3-105’号课程的平均分。
SELECT AVG(degree) FROM score WHERE cno BETWEEN 3 AND 105;
-- 12、查询Score表中至少有3名学生考试的并且编号以3开头的课程的平均分数。
SELECT cno,AVG(degree) FROM score WHERE cno like '3%' group by cno having COUNT(*)>3;
-- 13、查询所有学生的Sname、Cno和Degree列。
SELECT sname, cno , degree FROM students,score WHERE students.sno = score.sno;
-- 14、查询“3”班所选课程的平均分。
SELECT AVG(degree) FROM score , students WHERE score.sno = students.sno AND students.class = 3;
SELECT AVG(score.degree) FROM score JOIN students ON score.sno = students.sno WHERE students.class = 3;
-- 15、假设使用如下命令建立了一个grade表：
create table grade(low int,upp int,rank char(1));
insert into grade values(90,100,'A');
insert into grade values(80,89,'B');
insert into grade values(70,79,'C');
insert into grade values(60,69,'D');
insert into grade values(0,59,'E');
commit;
-- 前面教师表编号没有和课程对应起来，这里修改一下课程表
UPDATE courses SET tno=12 WHERE cno=1;
UPDATE courses SET tno=22 WHERE cno=2;
UPDATE courses SET tno=42 WHERE cno=3;
UPDATE courses SET tno=78 WHERE cno=4;
UPDATE courses SET tno=19 WHERE cno=5;
UPDATE courses SET tno=34 WHERE cno=6;
UPDATE courses SET tno=89 WHERE cno=7;
UPDATE courses SET tno=56 WHERE cno=8;
UPDATE courses SET tno=23 WHERE cno=9;
UPDATE courses SET tno=34 WHERE cno=10;
--现查询所有同学的Sno、Cno和rank列。
-- 16、查询"赵建"教师任课的学生成绩。
SELECT degree from score,teachers,courses 
WHERE tname like '赵建' 
and score.cno = courses.cno 
and courses.tno = teachers.tno; 
--17、查询选修某课程的同学人数多于2人的教师姓名。
SELECT tname FROM courses,score,teachers
WHERE courses.tno = teachers.tno 
and score.cno = courses.cno
GROUP By tname 
HAVING COUNT(*)>2;
--18、查询所有教师和同学的name、sex和birthday.
SELECT tname,tsex,tbirthday FROM teachers
UNION
SELECT sname,sex,sbirthday FROM students; 

SELECT tname,tsex,tbirthday FROM teachers
UNION ALL
SELECT sname,sex,sbirthday FROM students; 
--19 查询所有未讲课的教师的Tname和Depart.
SELECT distinct tname,depart FROM teachers,courses 
WHERE teachers.tno NOT IN (SELECT tno from courses);
-- 20、查询至少有2名男生的班号。
SELECT class FROM students
WHERE sex like '男'
GROUP BY class
HAVING COUNT(sex)>1;
--21、查询Student表中不姓“王”的同学记录。
SELECT * FROM students
WHERE sname NOT LIKE '王%';
22、查询所有选修“语文”课程的“男”同学的成绩表。
SELECT degree FROM students,courses,score
WHERE courses.cname LIKE '语文' 
and students.sex = '男' 
AND students.sno = score.sno
AND courses.cno = score.cno;















