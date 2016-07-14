--setup flows
CREATE TABLE flows (id SERIAL,
  tstamp integer,
  duration integer,
  srccomputer varchar,
  srcport varchar,
  dstcomputer varchar,
  dstport varchar,
  protocol varchar,
  packetcnt varchar,
  bytecnt varchar,
  redteam VARCHAR);

\COPY flows(tstamp,duration,srccomputer,srcport,dstcomputer,dstport,protocol,packetcnt,bytecnt) FROM '/home/pcgeller/weirdo/data/flows.txt' DELIMITER ',' CSV;
