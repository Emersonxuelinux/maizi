
use `12306-train`;

drop table if exists `agencys`;

create table `agencys` (
    `id` int primary key auto_increment,
    `province` varchar(10) not null,
    `city` varchar(15) not null,
    `county` varchar(15) not null,
    `address` varchar(50) not null,
    `name` varchar(50) not null,
    `windows` int,
    `start` time,
    `end` time
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

