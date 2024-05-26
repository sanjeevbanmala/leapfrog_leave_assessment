CREATE TABLE IF NOT EXISTS dbo.leave_types (
  leave_type_id INT PRIMARY KEY,
  leave_type VARCHAR(100),
  default_days INT,
  transferrable_days INT
);
