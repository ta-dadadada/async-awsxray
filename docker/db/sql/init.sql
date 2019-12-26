---- drop ----
DROP TABLE IF EXISTS `test`;

---- create ----
create table IF not exists `test`
(
 `id`               INT(20) AUTO_INCREMENT,
 `name`             VARCHAR(20) NOT NULL,
 PRIMARY KEY (`id`)
) DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

insert into test (name) values ('a'), ('b'), ('c');
