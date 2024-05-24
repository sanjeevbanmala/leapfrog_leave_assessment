import streamlit as st
import plotly.express as px
from pages.Leave_Trends import all_data
import plotly.graph_objects as go

st.set_page_config(page_title="Leave Periodic Trends", page_icon="🌍")


############################## HEATMAP FOR PERCENTAGE OF A LEAVE TYPE IN A MONTH IN A YEAR WITH TOTAL LEAVE COUNT ####################################################
# Group DataFrame by month
grp_by_month = all_data.groupby(by =['hmonth', 'year'])

leave_type = st.sidebar.selectbox(
    "Select the leave type:",
    options=all_data["leave_type"].unique(),
)

# Calculate total leave days and sick leave days for each month
monthly_leave_data = grp_by_month.agg(
    Total_Leave_Days=('leave_days', 'sum'),
    Leave_Type_Days=('leave_days', lambda x: x[all_data['leave_type'] == leave_type].sum())
)

# Calculate percentage of sick leave days for each month
monthly_leave_data['Percentage_Leave_Type'] = (monthly_leave_data['Leave_Type_Days'] / monthly_leave_data['Total_Leave_Days']) * 100
# Select month, year, and sick leave percentage
index_monthly_leave_data = monthly_leave_data.reset_index()[['hmonth', 'year', 'Percentage_Leave_Type']]

# Pivot the data to create a matrix suitable for heatmap
monthly_leave_heatmap_data = index_monthly_leave_data.pivot(index='hmonth', columns='year', values='Percentage_Leave_Type')

# Round off the values to desired precision (e.g., 2 decimal places)
monthly_leave_heatmap_data_rounded = monthly_leave_heatmap_data.round(2)

# Replace NaN values with 0
monthly_leave_heatmap_data_rounded.fillna(0, inplace=True)

monthly_leave_hover_template= """
<b>Year:</b> %{x}<br>
<b>Month:</b> %{y}<br>
<b>Percentage :</b> %{z:.2f}%<br><extra></extra>
"""

# Create heatmap
monthly_fig = go.Figure(data=go.Heatmap(
                   z=monthly_leave_heatmap_data_rounded,
                   x=monthly_leave_heatmap_data_rounded.columns,
                   y=monthly_leave_heatmap_data_rounded.index,
                   hovertemplate=monthly_leave_hover_template,
                   colorscale='Viridis'))

# Update layout for better visibility
monthly_fig.update_layout(
    title="Leave By Month of The Year",
    xaxis_title="Year",
    yaxis_title="Month",
)

# Show the plot
st.plotly_chart(monthly_fig)


############################## HEATMAP FOR PERCENTAGE OF A LEAVE TYPE IN A WEEK IN A YEAR WITH TOTAL LEAVE COUNT ####################################################
# Group DataFrame by week
grp_by_week = all_data.groupby(by =['day', 'year'])

# Calculate total leave days and leave days for each week
weekly_leave_data = grp_by_week.agg(
    Total_Leave_Days=('leave_days', 'sum'),
    Leave_Days_Type=('leave_days', lambda x: x[all_data['leave_type'] == leave_type].sum())
)

# Calculate percentage of  leave days for each week
weekly_leave_data['Percentage_Leave_Type'] = (weekly_leave_data['Leave_Days_Type'] / weekly_leave_data['Total_Leave_Days']) * 100
# Select week, year, and leave percentage
index_weekly_leave_data = weekly_leave_data.reset_index()[['day', 'year', 'Percentage_Leave_Type']]


# Pivot the data to create a matrix suitable for heatmap
weekly_leave_data_heatmap = index_weekly_leave_data.pivot(index='day', columns='year', values='Percentage_Leave_Type')

# Round off the values to desired precision (e.g., 2 decimal places)
weekly_leave_data_heatmap_rounded = weekly_leave_data_heatmap.round(2)

# Replace NaN values with 0
weekly_leave_data_heatmap_rounded.fillna(0, inplace=True)

weekly_leave_data_hover_template = """
<b>Year:</b> %{x}<br>
<b>Week Day:</b> %{y}<br>
<b>Percentage :</b> %{z:.2f}%<br><extra></extra>
"""

# Create heatmap
weekly_fig = go.Figure(data=go.Heatmap(
                   z=weekly_leave_data_heatmap_rounded,
                   x=weekly_leave_data_heatmap_rounded.columns,
                   y=weekly_leave_data_heatmap_rounded.index,
                   colorscale='Viridis',
                   hovertemplate=weekly_leave_data_hover_template))

# Update layout for better visibility
weekly_fig.update_layout(
    title="Leave by Week Of The Year",
    xaxis_title="Year",
    yaxis_title="Week Day",
)

# Show the plot
st.plotly_chart(weekly_fig)
