CREATE OR REPLACE PROCEDURE dbo.extract_leave_types()
LANGUAGE SQL
AS $$
INSERT INTO dbo.leave_types 
select 
distinct cast(leaveTypeId as INT), 
leaveTypeName,
cast(defaultDays as INT), 
cast(transferableDays as INT)  
from raw.imported_leave_information ili
on conflict (leave_type_id)
do nothing;
$$;
