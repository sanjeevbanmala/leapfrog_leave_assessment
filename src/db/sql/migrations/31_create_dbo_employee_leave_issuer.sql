CREATE TABLE IF NOT EXISTS dbo.employee_leave_issuer (
  employee_id INT,
  leave_issuer_id INT,
  is_current_leave_issuer BOOLEAN,
  CONSTRAINT pk_emp_lv_isuer_id PRIMARY KEY (
    employee_id, leave_issuer_id
  ),
  CONSTRAINT employee_leave_issuer_emp_id_fk FOREIGN KEY (
    employee_id
  ) REFERENCES dbo.employees (employee_id),
  CONSTRAINT employee_leave_issuer_leave_issuer_id_fk FOREIGN KEY (
    leave_issuer_id
  ) REFERENCES dbo.leave_issuer (leave_issuer_id)
);
