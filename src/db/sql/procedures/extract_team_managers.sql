CREATE OR REPLACE PROCEDURE dbo.team_managers()
LANGUAGE SQL
AS $$
insert into dbo.team_managers(team_manager_id) 
select distinct cast(teammanagerid as INT)
from raw.imported_leave_information ili
where cast(teammanagerid as INT) is not null
on conflict (team_manager_id)
do nothing;
$$;
