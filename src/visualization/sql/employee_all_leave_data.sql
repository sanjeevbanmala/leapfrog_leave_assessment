SELECT
    e.employee_id,
    e.first_name AS employee_first_name,
    e.middle_name AS employee_middle_name,
    e.last_name AS employee_last_name,
    e.email AS employee_email,
    e.is_hr AS employee_is_hr,
    e.is_supervisor AS employee_is_supv,
    e.team_manager_id AS employee_team_manager,
    d.designation_id,
    d.designation_name AS employee_designation,
    d2.department_id,
    d2.department_name AS employee_department,
    li.leave_issuer_id,
    li.first_name AS leave_issuer_first_name,
    li.last_name AS leave_issuer_last_name,
    li.email AS leave_issuer_email,
    el.leave_days,
    lt.leave_type,
    lt.default_days,
    lt.transferrable_days,
    el.leave_id,
    el.status,
    el.reason,
    el.remarks,
    el.is_consecutive,
    el.start_date,
    el.end_date,
    el.created_at,
    el.updated_at,
    e.first_name || ' ' || e.last_name AS full_name,
    LEFT(CAST(fy.start_date AS VARCHAR), 4)
    || '/'
    || LEFT(CAST(fy.end_date AS VARCHAR), 4) AS fiscal_date,
    TO_CHAR(created_at, 'YYYY') AS year,
    TO_CHAR(created_at, 'Mon') AS hmonth,
    TO_CHAR(created_at, 'MonDD') AS month,
    TO_CHAR(created_at, 'DY') AS day,
    TO_CHAR(created_at, 'MM') AS month_number
FROM dbo.employee_leaves AS el
INNER JOIN dbo.employees AS e ON el.employee_id = e.employee_id
INNER JOIN dbo.designations AS d ON e.designation_id = d.designation_id
INNER JOIN dbo.leave_types AS lt ON el.leave_type_id = lt.leave_type_id
FULL JOIN dbo.team_managers AS tm ON e.team_manager_id = tm.team_manager_id
INNER JOIN dbo.departments AS d2 ON e.department_id = d2.department_id
INNER JOIN dbo.leave_issuer AS li ON el.leave_issuer_id = li.leave_issuer_id
INNER JOIN dbo.fiscal_year AS fy ON el.fiscal_id = fy.fiscal_id;
