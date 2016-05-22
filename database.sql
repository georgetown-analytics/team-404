#mysql -v -h team404.czuxenny2zus.us-east-1.rds.amazonaws.com -P 3306 -u pcgeller -p

#setup redteam
CREATE TABLE redteam (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
tstamp VARCHAR(30),
userdomain VARCHAR(30),
src VARCHAR(20),
dst VARCHAR(20));

LOAD DATA LOCAL INFILE '/home/pcgeller/weirdo/data/redteam.txt'
  INTO TABLE redteam
    FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n'
    (tstamp, userdomain, src, dst);
/*
#setup auth
CREATE TABLE auth (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  tstamp INTEGER(0),
  userdomain VARCHAR(20),
  srcuser VARCHAR(20),
  dstuser VARCHAR(20),
  srccomputer VARCHAR(20),
  dstcomputer VARCHAR(20),
  authtype VARCHAR (20),
  passfail VARCHAR (15));
LOAD DATA LOCAL INFILE '/home/pcgeller/weirdo/data/auth.txt'
  INTO TABLE auth
  FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n'
  (tstamp, userdomain, srcuser, dstuser, srccomputer, dstcomputer,
  authtype, passfail);
*/
#setup proc
CREATE TABLE proc (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  tstamp integer(0),
  userdomain varchar(20),
  computer varchar(20),
  processname varchar(20),
  startend varchar(20));

load data local infile '/home/pcgeller/weirdo/data/proc.txt'
  into table proc
  fields terminated by ',' lines terminated by '\n'
  (tstamp, userdomain,  computer, processname, startend);

#setup flows
CREATE TABLE flows (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  tstamp integer(0),
  duration integer(15),
  srcomputer varchar(20),
  srcport varchar(20),
  dstcomputer varchar(20),
  dstport varchar(20),
  protocol varchar(20),
  packetcnt varchar(20),
  bytecnt varchar(20));

load data local infile '/home/pcgeller/weirdo/data/flows.txt'
  into table flows
  fields terminated by ',' lines terminated by '\n'
  (tstamp, duration, srccomputer, srcport, dstcomputer, dstport,
    protocol, packetcnt, bytecnt);

#setup dns
CREATE TABLE dns (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  tstamp INTEGER(0),
  srccomputer VARCHAR(20),
  computerresolved VARCHAR(20));

LOAD DATA LOCAL INFILE '/home/pcgeller/weirdo/data/dns.txt'
  INTO TABLE dns
  FIELDS TERMINATED BY ',' LINES TEMINATED BY '\n'
  (tstamp, srccomputer, computerresolved);
