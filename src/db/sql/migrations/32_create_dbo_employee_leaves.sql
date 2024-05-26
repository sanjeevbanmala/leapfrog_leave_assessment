CREATE TABLE IF NOT EXISTS dbo.employee_leaves (
  leave_id INT PRIMARY KEY,
  leave_issuer_id INT,
  leave_type_id INT,
  employee_id INT,
  fiscal_id INT,
  leave_days INT,
  reason TEXT,
  status VARCHAR(100),
  remarks TEXT,
  is_consecutive BOOLEAN,
  start_date DATE,
  end_date DATE,
  created_at DATE,
  updated_at DATE,
  CONSTRAINT employee_leaves_leave_issuer_id_fk FOREIGN KEY (
    leave_issuer_id
  ) REFERENCES dbo.leave_issuer (leave_issuer_id),
  CONSTRAINT employee_leaves_leave_type_id_fk FOREIGN KEY (
    leave_type_id
  ) REFERENCES dbo.leave_types (leave_type_id),
  CONSTRAINT employee_leaves_emp_id_fk FOREIGN KEY (
    employee_id
  ) REFERENCES dbo.employees (employee_id),
  CONSTRAINT employee_leaves_fiscal_id_fk FOREIGN KEY (
    fiscal_id
  ) REFERENCES dbo.fiscal_year (fiscal_id)
);
