
use `12306-train`;

drop table if exists `stations`;

create table `stations` (
    `bureau` varchar(10) not null,
    `station` boolean not null,
    `name` varchar(15) not null,
    `address` varchar(50) not null,
    `passenger` boolean not null,
    `luggage` boolean not null,
    `package` boolean not null,
    primary key(`bureau`, `station`, `name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

