#mysql -v -h team404.czuxenny2zus.us-east-1.rds.amazonaws.com -P 3306 -u pcgeller -p

# make red team table
CREATE TABLE redteam (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
tstamp VARCHAR(30),
userdomain VARCHAR(30),
source VARCHAR(20),
destination VARCHAR(20));

LOAD DATA LOCAL INFILE '/home/pcgeller/weirdo/data/redteam.txt'
  INTO TABLE redteam
    FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n'
    (tstamp, userdomain, source, destination);
