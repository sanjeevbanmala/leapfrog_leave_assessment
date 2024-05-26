WITH all_combinations AS (
    SELECT
        e.employee_id,
        lt.leave_type,
        lt.default_days,
        fiscal_dates.fiscal_date
    FROM
        dbo.employees AS e
    CROSS JOIN
        dbo.leave_types AS lt
    CROSS JOIN (
        SELECT DISTINCT LEFT(CAST(start_date AS VARCHAR), 4) || '/' || LEFT(CAST(end_date AS VARCHAR), 4) AS fiscal_date
        FROM dbo.fiscal_year
    ) AS fiscal_dates
)
, leave_data AS (
    SELECT
        e.employee_id,
        lt.leave_type,
        lt.default_days,
        LEFT(CAST(fy.start_date AS VARCHAR), 4) || '/' || LEFT(CAST(fy.end_date AS VARCHAR), 4) AS fiscal_date,
        COALESCE(SUM(CASE WHEN el.leave_type_id = lt.leave_type_id THEN el.leave_days ELSE 0 END), 0) AS total
    FROM
        dbo.employees AS e
    INNER JOIN
        dbo.leave_types AS lt ON lt.leave_type IN (SELECT DISTINCT leave_type FROM dbo.leave_types)
    INNER JOIN
        dbo.fiscal_year AS fy ON fy.fiscal_id = (SELECT fiscal_id FROM dbo.employee_leaves LIMIT 1)
    LEFT JOIN
        dbo.employee_leaves AS el ON e.employee_id = el.employee_id AND lt.leave_type_id = el.leave_type_id
    GROUP BY
        e.employee_id, fiscal_date, lt.leave_type, lt.default_days
)
SELECT
    ac.employee_id,
    ac.leave_type,
    ac.default_days,
    ac.fiscal_date,
    COALESCE(ld.total, 0) AS total
FROM
    all_combinations AS ac
LEFT JOIN
    leave_data AS ld ON ld.employee_id = ac.employee_id AND ld.leave_type = ac.leave_type AND ld.fiscal_date = ac.fiscal_date;