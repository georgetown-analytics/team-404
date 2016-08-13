/*
create index dnssrccomputer on dns (srccomputer);
create index dnscptresolved on dns (computerresolved);

create index flowssrccomputer on flows (srccomputer);
create index flowsdstcomputer on flows (dstcomputer);

create index redteamsrc on redteam (src);
create index redteamdst on redteam (dst);
create index redteamusr on redteam (usr);
create index redteamdomain on redteam (domain);

create index proccomputer on proc (computer);
create index procprocessname on proc (processname);
create index procusr on proc (usr);
create index procdomain on proc (domain);
*/
/*
create index authsrccomp on auth (srccomputer);
create index authdstcomp on auth (dstcomputer);
create index authsrcuser on auth (srcuser);
create index authdstuser on auth (dstuser);
create index authsrcdomain on auth (srcdomain);
create index authdstdomain on auth (dstdomain);
*/
/*
CREATE INDEX tstamp ON auth(srccomputer);
*/
/*
CREATE INDEX proctstamp on proc(tstamp);
CREATE INDEX flowststamp on flows(tstamp);
CREATE INDEX dnststamp on dns(tstamp);
*/
CREATE INDEX authid on auth(id);
CREATE INDEX typeauth on auth(authtype);
CREATE INDEX logontype on auth(logontype);
CREATE INDEX orientauth on auth(authorient);
CREATE INDEX pfauth on auth(passfail);
CREATE INDEX rtauth on auth(redteam);
