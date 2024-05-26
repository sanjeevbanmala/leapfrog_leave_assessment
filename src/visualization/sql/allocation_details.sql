select distinct
    e.employee_id,
    a.allocation_id,
    a."name",
    a.type
from dbo.employees as e
inner join dbo.employee_allocations as ea on e.employee_id = ea.employee_id
inner join dbo.allocations as a on ea.allocation_id = a.allocation_id;
