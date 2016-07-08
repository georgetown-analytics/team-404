--split up user@domain into two seperate fields

/*UPDATE redteam 
SET usr = sq.usr,
domain = sq.domain
FROM (SELECT userdomain, split_part(userdomain, '@', 1) as usr,
split_part(userdomain,'@',2) as domain FROM redteam) as sq
*/

UPDATE proc
SET usr = sq.usr,
domain = sq.domain
FROM (SELECT userdomain, split_part(userdomain,'@',1) as usr,
split_part(userdomain,'@',2) as domain FROM proc) as sq

UPDATE auth
SET usr = sq.usr,
domain = sq.domain
FROM (SELECT userdomain, split_part(userdomain,'@',1) as usr,
split_part(userdomain,'@',2) as domain FROM auth) as sq
