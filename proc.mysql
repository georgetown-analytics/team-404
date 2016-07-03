CREATE TABLE proc (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  tstamp integer(0),
  userdomain varchar(20),
  computer varchar(20),
  processname varchar(20),
  startend varchar(20),
  usr varchar(15),
  domain varchar(20),
  redteam varchar(5));

load data local infile '/home/pcgeller/weirdo/data/proc.txt'
  into table proc
  fields terminated by ',' lines terminated by '\n'
  (tstamp, userdomain,  computer, processname, startend);
