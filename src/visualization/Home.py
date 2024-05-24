import streamlit as st
import plotly.express as px
from pages.Leave_Trends import all_data

st.set_page_config(page_title="Home", page_icon="🌍")
st.title("Vyagyta Leave Visualization")



monthly_leaves_columns = all_data[['month_number', 'month', 'leave_days']]
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
    title=f"<b>Total Leaves: {all_data['leave_days'].sum()} </b>",
    color_discrete_sequence=["#0083B8"] * len(final_monthly_leave_columns),
    template="plotly_white",
)
fig_monthly_sales.update_layout(
    xaxis=dict(tickmode="auto"),
    xaxis_title ="Date",
    yaxis_title ="Total Leave Till Date",
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

department_wise_leave = all_data[["employee_department", "leave_days"]]
group_department_wise_leave = department_wise_leave.groupby(by=['employee_department'])['leave_days'].sum()

fig_dept_wise_leave = px.bar(
    group_department_wise_leave,
    x=group_department_wise_leave.index,
    y="leave_days",
    title=f"<b>Total Leaves by Department </b>",
    color_discrete_sequence=["#0083B8"] * len(group_department_wise_leave),
    template="plotly_white",
)
fig_dept_wise_leave.update_layout(
    xaxis=dict(tickmode="auto"),
    xaxis_title ="Department",
    yaxis_title ="Total Leave",
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)


leave_type_wise_leave = all_data[["leave_type", "leave_days"]]
group_leave_type_wise_leave = leave_type_wise_leave.groupby(by=['leave_type'])['leave_days'].sum()

fig_leave_type_wise_leave = px.bar(
    group_leave_type_wise_leave,
    x=group_leave_type_wise_leave.index,
    y="leave_days",
    title="<b>Total Leaves by Leave Type</b>",
    color_discrete_sequence=["#0083B8"] * len(group_leave_type_wise_leave),
    template="plotly_white",
)
fig_leave_type_wise_leave.update_layout(
    xaxis=dict(tickmode="auto"),
    xaxis_title ="Employee Designations",
    yaxis_title ="Total Leave",
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)


designation_wise_leave = all_data[["employee_designation", "leave_days"]]
group_designation_wise_leave = designation_wise_leave.groupby(by=['employee_designation'])['leave_days'].sum()

fig_designation_wise_leave = px.bar(
    group_leave_type_wise_leave,
    x=group_leave_type_wise_leave.index,
    y="leave_days",
    title="<b>Designation wise Total Leave</b>",
    color_discrete_sequence=["#0083B8"] * len(group_leave_type_wise_leave),
    template="plotly_white",
)
fig_designation_wise_leave.update_layout(
    xaxis=dict(tickmode="auto"),
    xaxis_title ="Leave Type",
    yaxis_title ="Total Leave",
    plot_bgcolor="rgba(0,0,0,0)",
   yaxis=(dict(showgrid=False)),
)
first, second = st.columns(2)
first.plotly_chart(fig_monthly_sales, use_container_width=True)
second.plotly_chart(fig_dept_wise_leave, use_container_width=True)

third, fourth = st.columns(2)
third.plotly_chart(fig_leave_type_wise_leave, use_container_width=True)
fourth.plotly_chart(fig_designation_wise_leave, use_container_width=True)


