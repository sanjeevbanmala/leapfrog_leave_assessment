import sys
import os
import streamlit as st
import plotly.graph_objects as go

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.fetch_data import fetch_data
from utils.logging import get_logger

logger = get_logger("Leave-trends")


def main():

    st.set_page_config(page_title="Leave Trends", page_icon="🌍")

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
        st.sidebar.header("Please filter here")
        fiscal_id = st.sidebar.multiselect(
            "Select the Fiscal Date:",
            options=all_data["fiscal_date"].unique(),
            default=all_data["fiscal_date"].unique(),
        )

        department = st.sidebar.multiselect(
            "Select the department:",
            options=all_data["employee_department"].unique(),
            default=all_data["employee_department"].unique(),
        )

        designation = st.sidebar.multiselect(
            "Select the designation:",
            options=all_data["employee_designation"].unique(),
            default=all_data["employee_designation"].unique(),
        )

        leave_type = st.sidebar.multiselect(
            "Select the leave type:",
            options=all_data["leave_type"].unique(),
            default=all_data["leave_type"].unique(),
        )

        df_selection = all_data.query(
            "fiscal_date == @fiscal_id & employee_department == @department & employee_designation == @designation & leave_type == @leave_type"
        )

        ####################### Month and Day wise Leave Trend################################

        monthly_leaves_columns = (
            df_selection.groupby(by=["month_number", "month"])["leave_days"]
            .sum()
            .reset_index()
        )

        # Leaves BY Month [BAR CHART]
        fig_monthly_sales = px.line(
            monthly_leaves_columns,
            x="month",
            y="leave_days",
            title="<b>Leaves by Month</b>",
            color_discrete_sequence=["#0083B8"] * len(monthly_leaves_columns),
            template="plotly_white",
        )
        fig_monthly_sales.update_layout(
            xaxis=dict(tickmode="auto"),
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=(dict(showgrid=False)),
        )

        ###################### EMPLOYEE WISE LEAVE TREND ############################
        employee_leave_columns = (
            df_selection.groupby(by=["employee_first_name"])["leave_days"]
            .sum()
            .reset_index()
        )

        # Leaves BY Month [BAR CHART]
        fig_employee_leaves = px.bar(
            employee_leave_columns,
            x="employee_first_name",
            y="leave_days",
            title="<b>Leaves by Employee</b>",
            color_discrete_sequence=["#0083B8"] * len(employee_leave_columns),
            template="plotly_white",
        )
        fig_employee_leaves.update_layout(
            xaxis=dict(tickmode="auto"),
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=(dict(showgrid=False)),
        )

        st.plotly_chart(fig_monthly_sales, use_container_width=True)
        st.plotly_chart(fig_employee_leaves, use_container_width=True)
        logger.info("Streamlit app executed successfully.")


if __name__ == "__main__":
    main()
