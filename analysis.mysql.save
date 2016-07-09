/*# Create table of whose logged on


#select * from auth
#	where srccomputer = 'C1003';
#select * from proc
#	where computer = 'C1003';
#select * from flows
#	where srccomputer = 'C1003';
#select * from dns
#	where srccomputer = 'C1003';

create table aglobal
	#select dstcomputer, count(*) as dstfreq from auth group by dstcomputer
	select authorient, count(*) as orientfreq from auth group by authorient
	select logontype, count(*) as typefreq from auth group by longontype
	select passfail, count(*) as passfailfreq from auth group by passfail;

create table atest
	select dstcomputer, count(*) as dstfreq from authtest group by dstcomputer
	select authorient, count(*) as orientfreq from authtest group by authorient
	select logontype, count(*) as typefreq from authtest group by longontype
	select passfail, count(*) as passfail from authtest group by passfail;

create table pglobal
	select processname, count(*) as freq from proc group by processname;

create table ptest
	select processname, count(*) as freq from proctest group by processname;
*/

alter table auth
add column srcuser varchar(10),
add column srcdomain varchar(20),
add column dstuser varchar(10),
add column dstdomain varchar(20);
/*
alter table proc
add column usr varchar(10),
add column domain varchar(15);
*/
