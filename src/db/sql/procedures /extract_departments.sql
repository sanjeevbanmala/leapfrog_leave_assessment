CREATE OR REPLACE PROCEDURE dbo.departments()
LANGUAGE SQL
AS $$
insert into dbo.departments(department_name)  
select distinct departmentDescription
from raw.imported_leave_information ili
on conflict (department_id)
do nothing;
$$;
