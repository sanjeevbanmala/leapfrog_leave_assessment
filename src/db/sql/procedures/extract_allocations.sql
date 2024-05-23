CREATE OR REPLACE PROCEDURE dbo.allocations()
LANGUAGE SQL
AS $$
INSERT INTO dbo.allocations
SELECT 
distinct
    (data->>'id')::INT AS allocation_id,
    data->>'name' AS name,
    data->>'type' AS type
FROM (
    select jsonb_array_elements(allocations) AS data
    FROM raw.imported_leave_information 
) AS allocations
on conflict (allocation_id)
do nothing;
$$;
