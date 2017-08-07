create database if not exists `12306-train`;

grant usage on *.* to '12306'@'localhost';
drop user '12306'@'localhost';

create user '12306'@'localhost' identified by '12306'; 
grant all privileges on `12306-train`.* to '12306'@'localhost';

use `12306-train`;

drop table if exists `example`;

create table `example` (
    `code` varchar(6) primary key,
    `start` varchar(6) not null,
    `end` varchar(6) not null
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

insert ignore into `example` values ('G308', '成都', '北京'), ('G101', '北京', '上海'), ('D352', '上海', '成都');
