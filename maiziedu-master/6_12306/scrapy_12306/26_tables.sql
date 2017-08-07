
use `12306-train`;

create table if not exists `train_briefs` (
    `code` varchar(10) primary key,
    `train_no` varchar(20) not null,
    `start` varchar(10) not null,
    `end` varchar(10) not null
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table if not exists `train_infos` (
    `train_no` varchar(20) not null,
    `no` tinyint not null,
    `station` varchar(15) not null,
    `type` tinyint not null,
    `start_time` time,
    `arrive_time` time,
    `stopover_time` time,
    primary key (`train_no`, `no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8

