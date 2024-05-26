select
    e.employee_id,
    e.first_name,
    e.middle_name,
    e.last_name,
    e.email,
    d.department_name,
    d2.designation_name,
    e.first_name || ' ' || e.last_name as full_name
from dbo.employees as e
inner join dbo.departments as d on e.department_id = d.department_id
inner join dbo.designations as d2 on e.designation_id = d2.designation_id;
