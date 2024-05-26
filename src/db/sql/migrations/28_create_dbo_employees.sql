CREATE TABLE IF NOT EXISTS dbo.employees (
  employee_id INT PRIMARY KEY,
  first_name VARCHAR(100),
  middle_name VARCHAR(100),
  last_name VARCHAR(100),
  email VARCHAR(100),
  is_hr BOOLEAN,
  is_supervisor BOOLEAN,
  designation_id INT,
  team_manager_id INT,
  department_id INT,
  CONSTRAINT employee_designation_id_fk FOREIGN KEY (
    designation_id
  ) REFERENCES dbo.designations (designation_id),
  CONSTRAINT employee_team_manager_id_fk FOREIGN KEY (
    team_manager_id
  ) REFERENCES dbo.team_managers (team_manager_id),
  CONSTRAINT employee_department_id_fk FOREIGN KEY (
    department_id
  ) REFERENCES dbo.departments (department_id)
);
