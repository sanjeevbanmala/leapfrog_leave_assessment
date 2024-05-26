import sys
import os
import streamlit as st
import plotly.graph_objects as go
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.fetch_data import fetch_data
from utils.logging import get_logger

logger = get_logger("Periodic-trends")

def main():

    st.set_page_config(page_title="Leave Periodic Trends", page_icon="🌍")

    # Fetch data
    try:
        all_data = fetch_data("./sql/employee_all_leave_data.sql")
        st.sidebar.success("Data fetched successfully.")
        logger.info("Data fetched successfully.")
    except Exception as e:
        st.sidebar.error(f"Error fetching data: {e}")
        logger.error(f"Error fetching data: {e}")
        all_data = None

    if all_data is not None:
        # Group DataFrame by month
        grp_by_month = all_data.groupby(by=["hmonth", "year"])

        leave_type = st.sidebar.selectbox(
            "Select the leave type:",
            options=all_data["leave_type"].unique(),
        )

        # Calculate total leave days and leave days for each month
        monthly_leave_data = grp_by_month.agg(
            Total_Leave_Days=("leave_days", "sum"),
            Leave_Days_Type=("leave_days", lambda x: x[all_data["leave_type"] == leave_type].sum()),
        )

        # Calculate percentage of leave days for each month
        monthly_leave_data["Percentage_Leave_Type"] = (
            monthly_leave_data["Leave_Days_Type"] / monthly_leave_data["Total_Leave_Days"]
        ) * 100

        # Select month, year, and leave percentage
        index_monthly_leave_data = monthly_leave_data.reset_index()[
            ["hmonth", "year", "Percentage_Leave_Type"]
        ]

        # Pivot the data to create a matrix suitable for heatmap
        monthly_leave_heatmap_data = index_monthly_leave_data.pivot(
            index="hmonth", columns="year", values="Percentage_Leave_Type"
        ).fillna(0).round(2)

        # Create heatmap
        monthly_fig = go.Figure(
            data=go.Heatmap(
                z=monthly_leave_heatmap_data.values,
                x=monthly_leave_heatmap_data.columns,
                y=monthly_leave_heatmap_data.index,
                hovertemplate="<b>Year:</b> %{x}<br><b>Month:</b> %{y}<br><b>Percentage :</b> %{z:.2f}%<br><extra></extra>",
                colorscale="Viridis",
            )
        )

        # Update layout for better visibility
        monthly_fig.update_layout(
            title="Leave By Month of The Year",
            xaxis_title="Year",
            yaxis_title="Month",
        )

        # Show the plot
        st.plotly_chart(monthly_fig)

        # Group DataFrame by week
        grp_by_week = all_data.groupby(by=["day", "year"])

        # Calculate total leave days and leave days for each week
        weekly_leave_data = grp_by_week.agg(
            Total_Leave_Days=("leave_days", "sum"),
            Leave_Days_Type=("leave_days", lambda x: x[all_data["leave_type"] == leave_type].sum()),
        )

        # Calculate percentage of leave days for each week
        weekly_leave_data["Percentage_Leave_Type"] = (
            weekly_leave_data["Leave_Days_Type"] / weekly_leave_data["Total_Leave_Days"]
        ) * 100

        # Select week, year, and leave percentage
        index_weekly_leave_data = weekly_leave_data.reset_index()[
            ["day", "year", "Percentage_Leave_Type"]
        ]

        # Pivot the data to create a matrix suitable for heatmap
        weekly_leave_data_heatmap = index_weekly_leave_data.pivot(
            index="day", columns="year", values="Percentage_Leave_Type"
        ).fillna(0).round(2)

        # Create heatmap
        weekly_fig = go.Figure(
            data=go.Heatmap(
                z=weekly_leave_data_heatmap.values,
                x=weekly_leave_data_heatmap.columns,
                y=weekly_leave_data_heatmap.index,
                hovertemplate="<b>Year:</b> %{x}<br><b>Week Day:</b> %{y}<br><b>Percentage :</b> %{z:.2f}%<br><extra></extra>",
                colorscale="Viridis",
            )
        )

        # Update layout for better visibility
        weekly_fig.update_layout(
            title="Leave by Week Of The Year",
            xaxis_title="Year",
            yaxis_title="Week Day",
        )

        # Show the plot
        st.plotly_chart(weekly_fig)
        logger.info("Streamlit app executed successfully.")

if __name__ == "__main__":
    main()
