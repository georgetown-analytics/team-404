#setup flows
CREATE TABLE flows (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  tstamp integer(0),
  duration integer(15),
  srccomputer varchar(20),
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
