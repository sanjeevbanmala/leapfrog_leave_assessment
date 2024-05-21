CREATE OR REPLACE PROCEDURE dbo.employee_leave_issuer()
LANGUAGE SQL
AS $$
insert  into dbo.employee_leave_issuer 
select distinct cast(empid as INT),cast(currentleaveissuerid as INT), true as is_current_leave_issuer 
from raw.imported_leave_information ili 
where leaveissuerid = currentleaveissuerid
union 
select distinct cast(empid as INT),cast(leaveissuerid as INT), false as is_current_leave_issuer 
from raw.imported_leave_information ili 
where leaveissuerid <> currentleaveissuerid
union
select distinct cast(empid as INT),cast(currentleaveissuerid as INT), true as is_current_leave_issuer 
from raw.imported_leave_information ili 
where leaveissuerid <> currentleaveissuerid
on conflict (employee_id, leave_issuer_id)
do nothing;
$$;
