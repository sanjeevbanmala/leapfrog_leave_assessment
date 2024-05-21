CREATE OR REPLACE PROCEDURE dbo.designations()
LANGUAGE SQL
AS $$
insert into dbo.designations 
select distinct cast(designationid as INT),designationname  
from raw.imported_leave_information ili
on conflict (designation_id)
do nothing;
$$;
