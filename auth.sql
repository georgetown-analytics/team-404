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

LOAD DATA LOCAL INFILE '/media/pcgeller/SharedDrive/auth.txt'
  INTO TABLE auth
  FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n'
  (tstamp, userdomain, srcuser, dstuser, srccomputer, dstcomputer,
  authtype, passfail);

