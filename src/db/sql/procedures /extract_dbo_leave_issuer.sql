CREATE OR REPLACE PROCEDURE dbo.leave_issuer()
LANGUAGE SQL
AS $$
-- Case 1: selecting distinct leave issuers whose default leave issuer id and current leave issuer id are same
insert into dbo.leave_issuer 
select distinct
cast(currentleaveissuerid as INT), 
leaveissuerfirstname, 
leaveissuerlastname, 
currentleaveissueremail 
from raw.imported_leave_information ili
where cast(currentleaveissuerid as INT)= cast(leaveissuerid  as INT)
on conflict (leave_issuer_id)
do nothing;
-- CASE 2: Selecting distinct default leave issuers who are not the current leave issuers
insert into dbo.leave_issuer 
select distinct
cast(ili.leaveissuerid as int), 
ili.leaveissuerfirstname, 
ili.leaveissuerlastname, 
ili2.currentleaveissueremail 
from raw.imported_leave_information ili
left join raw.imported_leave_information ili2 
on ili.leaveissuerid= ili2.currentleaveissuerid 
where ili.leaveissuerid <> ili.currentleaveissuerid
on conflict (leave_issuer_id)
do nothing;
-- CASE 3 : Selecting distinct current leave issuers who are not the default leave issuers 
insert into dbo.leave_issuer(leave_issuer_id,email)
select distinct
cast(ili.currentleaveissuerid as int),
ili.currentleaveissueremail 
from raw.imported_leave_information ili
where ili.leaveissuerid <> ili.currentleaveissuerid
on conflict (leave_issuer_id)
do nothing;
$$;
