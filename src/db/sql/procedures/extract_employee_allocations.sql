CREATE OR REPLACE PROCEDURE dbo.employee_allocations()
LANGUAGE SQL
AS $$
INSERT INTO dbo.employee_allocations
SELECT 
distinct
    cast(empid as INT),
    (data->>'id')::INT AS allocation_id
FROM (
    select empid,jsonb_array_elements(allocations) AS data
    FROM raw.imported_leave_information 
) AS allocations
on conflict (employee_id,allocation_id)
do nothing;
$$;
