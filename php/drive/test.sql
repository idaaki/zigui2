# show variables like "chara%";
# Edit /etc/my.cnf

# [mysqld]
# ...
# character-set-server=utf8
#
# [client]
# default-character-set=utf8

id       parent   question    answer   explanation image
1        -                                         null
2        -                                         222.jpg
3        -                                         333.jpg
... 

90       -        AAA         -        AAAAAAAAA   AAA.jpg
91       90       AAA1        right
92       90       AAA2        wrong
93       90       AAA3        wrong

94       -        BBB         -        BBBBBBBBB   BBB.jpg
95       94       BBB1        right
96       94       BBB2        wrong
97       94       BBB3        right

CREATE DATABASE IF NOT EXISTS `drv_db`;

CREATE TABLE IF NOT EXISTS `drv_main` (
  `id` int(32) NOT NULL AUTO_INCREMENT,
  `parent` int(32),
  `question` varchar(767),
  `answer` tinyint(1),
  `explanation` varchar(767),
  `image` mediumblob,
  `type` varchar(767),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

# DROP TABLE drv_main;


CREATE TABLE IF NOT EXISTS `drv_semi` (
  `id` int(32) NOT NULL AUTO_INCREMENT,
  `question` varchar(767),
  `answer` tinyint(1),
  `explanation` varchar(767),
  `image` mediumblob,
  `type` varchar(767),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

# DROP TABLE drv_semi;

mysqldump --default-character-set=utf8 -u root -p 'drv_db' > drv_db.sql

mysql -u root -p 'drv_db' < drv_db.sql

