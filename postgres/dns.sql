/*
--setup dns
CREATE TABLE dns (id SERIAL,
  tstamp INTEGER,
  srccomputer VARCHAR,
  computerresolved VARCHAR,
  redteam VARCHAR);

\COPY dns(tstamp,srccomputer,computerresolved) FROM '/home/pcgeller/weirdo/data/dns.txt' DELIMITER ',' CSV;
*/
--setup redteam
CREATE TABLE redteam (id SERIAL,
tstamp VARCHAR,
userdomain VARCHAR,
src VARCHAR,
dst VARCHAR,
usr VARCHAR,
domain VARCHAR,
redteam VARCHAR);

\COPY redteam(tstamp,userdomain,src,dst) FROM '/home/pcgeller/weirdo/data/redteam.txt' DELIMITER ',' CSV;
