
use `12306-train`;

drop table if exists `turns`;

create table `turns` (
    `id` integer primary key,
    `mark_time` timestamp not null
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

drop table if exists `train_briefs`;

create table `train_briefs` (
    `code` varchar(10),
    `train_no` varchar(20) not null,
    `start` varchar(10) not null,
    `end` varchar(10) not null,
    `turn` integer not null,
    primary key(`code`, `turn`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

drop table if exists `train_infos`;

create table `train_infos` (
    `train_no` varchar(20) not null,
    `no` tinyint not null,
    `station` varchar(15) not null,
    `start_time` time,
    `arrive_time` time,
    `stopover_time` time,
    `seat_type` varchar(20) default null,
    `turn` integer not null,
    primary key (`train_no`, `no`, `turn`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8

