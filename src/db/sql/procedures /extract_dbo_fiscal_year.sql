CREATE OR REPLACE PROCEDURE dbo.fiscal_year()
LANGUAGE SQL
AS $$
Insert into dbo.fiscal_year 
SELECT 
DISTINCT cast(fiscalId as INT), 
cast(fiscalStartDate as timestamp),
cast(fiscalEndDate as timestamp)  
from raw.imported_leave_information ili
on conflict (fiscal_id)
do nothing;
$$;
