import psycopg2
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px


st.set_page_config(page_title="Leave Trends", page_icon="🌍")


conn = psycopg2.connect(
    dbname="vyaguta_db",
    user="postgres",
    password="admin@123",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()
# sql = '''
# select To_char(created_at, 'mm') as mm,To_char(created_at, 'Month') as date, count(leave_days) as leave_days
# from dbo.employee_leaves
# where status ='APPROVED'
# group by mm,date
# order by To_char(created_at, 'Month');
# '''

sql='''
SELECT
e.employee_id,
e.first_name as employee_first_name,
e.middle_name as employee_middle_name, 
e.last_name as employee_last_name,
e.first_name || ' ' || e.last_name as full_name,
e.email as employee_email,
e.is_hr as employee_is_hr,
e.is_supervisor as employee_is_supv,
e.team_manager_id as employee_team_manager,
d.designation_id,
d.designation_name as employee_designation,
d2.department_id,
d2.department_name as employee_department,
li.leave_issuer_id,
li.first_name as leave_issuer_first_name,
li.last_name as leave_issuer_last_name,
li.email as leave_issuer_email,
el.leave_days,
lt.leave_type,
lt.default_days,
lt.transferrable_days,
el.leave_id,
LEFT(cast(fy.start_date as VARCHAR), 4) ||'/'|| LEFT(cast(fy.end_date as VARCHAR), 4) as fiscal_date,
el.status,
el.reason,
el.remarks,
el.is_consecutive,
el.start_date,
el.end_date,
el.created_at,
To_char(created_at, 'YYYY') as year,
To_char(created_at, 'Mon') as hmonth,
To_char(created_at, 'MonDD') as month,
To_char(created_at, 'DY') as day,
To_char(created_at, 'MM') as month_number,
el.updated_at
from dbo.employee_leaves el
inner join dbo.employees e on e.employee_id =el.employee_id 
inner join dbo.designations d on e.designation_id =d.designation_id
inner join dbo.leave_types lt on lt.leave_type_id = el.leave_type_id  
full join dbo.team_managers tm on tm.team_manager_id=e.team_manager_id
inner join dbo.departments d2 on d2.department_id = e.department_id
inner join dbo.leave_issuer li on li.leave_issuer_id = el.leave_issuer_id
inner join dbo.fiscal_year fy on fy.fiscal_id = el.fiscal_id; 
'''

all_data=pd.read_sql(sql,conn)

# My filers are fiscal_id, department, designation, leave type



st.sidebar.header("Please filter here")
fiscal_id = st.sidebar.multiselect(
    "Select the Fiscal Date:",
    options=all_data["fiscal_date"].unique(),
    default=all_data["fiscal_date"].unique()
)

department = st.sidebar.multiselect(
    "Select the department:",
    options=all_data["employee_department"].unique(),
    default=all_data["employee_department"].unique()
)

designation = st.sidebar.multiselect(
    "Select the designation:",
    options=all_data["employee_designation"].unique(),
    default=all_data["employee_designation"].unique()
)

leave_type = st.sidebar.multiselect(
    "Select the leave type:",
    options=all_data["leave_type"].unique(),
    default=all_data["leave_type"].unique()
)

df_selection = all_data.query(
    "fiscal_date == @fiscal_id & employee_department ==@department & employee_designation == @designation & @leave_type== leave_type"
)


####################### Month and Day wise Leave Trend################################

monthly_leaves_columns = df_selection[['month_number', 'month', 'leave_days']]
group_monthly_leaves = monthly_leaves_columns.groupby(by=['month_number','month'])['leave_days'].sum()
unique_monthly_leaves= group_monthly_leaves.to_frame()
# After performing the groupby operation
unique_monthly_leaves.reset_index(inplace=True)

# Selecting only 'month' and 'leave_days' columns
final_monthly_leave_columns = unique_monthly_leaves[['month', 'leave_days']]


# Leaves BY MOnth [BAR CHART]

fig_monthly_sales = px.line(
    final_monthly_leave_columns,
    x=final_monthly_leave_columns["month"],
    y="leave_days",
    title="<b>Leaves by Month</b>",
    color_discrete_sequence=["#0083B8"] * len(final_monthly_leave_columns),
    template="plotly_white",
)
fig_monthly_sales.update_layout(
    xaxis=dict(tickmode="auto"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)


###################### EMPLOYEE WISE LEAVE TREND ############################
employee_leave_columns = df_selection.groupby(by =['employee_first_name'])['leave_days'].sum()


# Leaves BY MOnth [BAR CHART]

fig_employee_leaves = px.bar(
    employee_leave_columns,
    x=employee_leave_columns.index,
    y="leave_days",
    title="<b>Leaves by Employee</b>",
    color_discrete_sequence=["#0083B8"] * len(final_monthly_leave_columns),
    template="plotly_white",
)
fig_employee_leaves.update_layout(
    xaxis=dict(tickmode="auto"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

st.plotly_chart(fig_monthly_sales, use_container_width=True)
st.plotly_chart(fig_employee_leaves, use_container_width=True)
