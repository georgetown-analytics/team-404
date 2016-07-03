--setup auth
CREATE TABLE auth (id SERIAL,
  tstamp integer,
  srcuserdomain VARCHAR,
  dstuserdomain VARCHAR,
  srccomputer VARCHAR,
  dstcomputer VARCHAR,
  authtype VARCHAR,
  logontype VARCHAR,
  authorient VARCHAR,
  passfail VARCHAR,
  srcusr VARCHAR,
  srcdomain VARCHAR,
  dstusr VARCHAR,
  dstdomain VARCHAR,
  redteam VARCHAR;

\COPY auth(tstamp,srcuserdomain,dstuserdomain,srccomputer,dstcomputer,authtype,logontype,authorient,passfail) FROM '/home/pcgeller/weirdo/data/auth.txt' DELIMITER ',' CSV;
