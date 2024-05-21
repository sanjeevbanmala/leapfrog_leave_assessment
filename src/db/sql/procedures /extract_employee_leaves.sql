CREATE OR REPLACE PROCEDURE dbo.employee_leaves()
LANGUAGE SQL
AS $$
insert into dbo.employee_leaves 
select cast(id as int),
case 
	when (leaveissuerid is null or (leaveissuerid <> currentleaveissuerid))  
	then cast(currentleaveissuerid as INT)
	else cast(leaveissuerid as INt)
end,
cast(leavetypeid as int),
cast(empid as InT),
cast(fiscalid as int),
cast(leavedays as int),
reason,
status,
remarks,
cast (isconsecutive as boolean),
cast(startdate as timestamp),
cast(enddate as timestamp),
cast(createdat as timestamp),
cast(updatedat as timestamp) 
from raw.imported_leave_information ili
on conflict (leave_id)
do nothing;
$$;
