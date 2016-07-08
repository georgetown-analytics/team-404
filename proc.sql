CREATE TABLE proc (id SERIAL,
  tstamp integer,
  userdomain varchar,
  computer varchar,
  processname varchar,
  startend varchar,
  usr varchar,
  domain varchar,
  redteam varchar);

\COPY proc(tstamp,userdomain,computer,processname,startend) FROM '/home/pcgeller/weirdo/data/proc.txt' DELIMITER ',' CSV;
