insert_query = """
INSERT INTO raw.imported_leave_information(
                id, userId, empId, teamManagerId, designationId, designationName, firstName, middleName, lastName, email, 
                isHr, isSupervisor, allocations, leaveIssuerId, currentLeaveIssuerId, leaveIssuerFirstName, leaveIssuerLastName, 
                currentLeaveIssuerEmail, departmentDescription, startDate, endDate, leaveDays, reason, status, remarks, leaveTypeId, 
                leaveTypeName, defaultDays, transferableDays, isConsecutive, fiscalId, fiscalStartDate, fiscalEndDate, fiscalIsCurrent, 
                createdAt, updatedAt, isConverted
            ) VALUES (
                $1::int, $2::int, $3::text, $4::int, $5::int, $6::text, $7::text, $8::text, $9::text, $10::text,
                $11::bool, $12::bool, $13::jsonb, $14::int, $15::int, $16::text, $17::text, $18::text, $19::text, $20::text,
                $21::text, $22::int, $23::text, $24::text, $25::text, $26::int, $27::text, $28::int, $29::int, $30::int,
                $31::int, $32::text, $33::text, $34::bool, $35::text, $36::text, $37::int
            );
"""
