
use `12306-train`;

drop table if exists `train_stations`;

create table `train_stations` (
    `name` varchar(20) primary key,
    `code` varchar(6) not null
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

drop table if exists `train_tickets`;

create table `train_tickets` (
    `train_no` varchar(20) not null,
    `start` varchar(15) not null,
    `end` varchar(15) not null,
    `swz` smallint,
    `tz` smallint,
    `zy` smallint,
    `ze` smallint,
    `gr` smallint,
    `rw` smallint,
    `yw` smallint,
    `rz` smallint,
    `yz` smallint,
    `wz` smallint,
    `qt` smallint,
    primary key (`train_no`, `start`, `end`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

alter table `train_briefs` add column `seat_type` varchar(20) default null;
