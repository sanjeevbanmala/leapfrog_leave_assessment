CREATE OR REPLACE PROCEDURE dbo.employees()
LANGUAGE SQL
AS $$
insert into dbo.employees 
select distinct cast(ili.empid as INT), ili.firstname, ili.middlename, ili.lastname, ili.email, cast(ili.ishr as boolean), cast(ili.issupervisor as boolean),cast(ili.designationid as INT), cast(ili.teammanagerid as INT), d.department_id  
from raw.imported_leave_information ili 
inner join dbo.departments d  on d.department_name= ili.departmentdescription
on conflict (employee_id)
do nothing;
$$;
