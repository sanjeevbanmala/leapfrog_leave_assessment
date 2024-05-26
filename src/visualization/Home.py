import logging
import streamlit as st
import pandas as pd
import plotly.express as px
from viz_utils import fetch_data

# Configure logging
logging.basicConfig(filename='streamlit.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def generate_visualizations(all_data):
    try:
        # Group data for visualizations
        monthly_leaves_columns = all_data[["month_number", "month", "leave_days"]]
        group_monthly_leaves = monthly_leaves_columns.groupby(by=["month_number", "month"])["leave_days"].sum()
        unique_monthly_leaves = group_monthly_leaves.reset_index()

        department_wise_leave = all_data[["employee_department", "leave_days"]].groupby(by=["employee_department"])["leave_days"].sum()

        leave_type_wise_leave = all_data[["leave_type", "leave_days"]].groupby(by=["leave_type"])["leave_days"].sum()

        designation_wise_leave = all_data[["employee_designation", "leave_days"]].groupby(by=["employee_designation"])["leave_days"].sum()

        # Create Plotly figures
        fig_monthly_sales = px.line(unique_monthly_leaves, x="month", y="leave_days",
                                     title=f"<b>Total Leaves: {all_data['leave_days'].sum()} </b>",
                                     color_discrete_sequence=["#0083B8"] * len(unique_monthly_leaves),
                                     template="plotly_white")

        fig_dept_wise_leave = px.bar(department_wise_leave, x=department_wise_leave.index, y="leave_days",
                                      title=f"<b>Total Leaves by Department </b>",
                                      color_discrete_sequence=["#0083B8"] * len(department_wise_leave),
                                      template="plotly_white")

        fig_leave_type_wise_leave = px.bar(leave_type_wise_leave, x=leave_type_wise_leave.index, y="leave_days",
                                           title="<b>Total Leaves by Leave Type</b>",
                                           color_discrete_sequence=["#0083B8"] * len(leave_type_wise_leave),
                                           template="plotly_white")

        fig_designation_wise_leave = px.bar(designation_wise_leave, x=designation_wise_leave.index, y="leave_days",
                                            title="<b>Designation wise Total Leave</b>",
                                            color_discrete_sequence=["#0083B8"] * len(designation_wise_leave),
                                            template="plotly_white")

        logging.info('Visualizations generated successfully')
        return fig_monthly_sales, fig_dept_wise_leave, fig_leave_type_wise_leave, fig_designation_wise_leave
    except Exception as e:
        logging.error(f"Error generating visualizations: {e}")
        return None, None, None, None

def main():
    st.set_page_config(page_title="Home", page_icon="🌍")
    st.title("Vyagyta Leave Visualization")

    # Fetch data
    all_data = fetch_data("sql/employee_all_leave_data.sql")
    if all_data is not None:
        # Generate visualizations
        fig_monthly_sales, fig_dept_wise_leave, fig_leave_type_wise_leave, fig_designation_wise_leave = generate_visualizations(all_data)

        # Display visualizations
        if all(fig is not None for fig in [fig_monthly_sales, fig_dept_wise_leave, fig_leave_type_wise_leave, fig_designation_wise_leave]):
            first, second = st.columns(2)
            first.plotly_chart(fig_monthly_sales, use_container_width=True)
            second.plotly_chart(fig_dept_wise_leave, use_container_width=True)

            third, fourth = st.columns(2)
            third.plotly_chart(fig_leave_type_wise_leave, use_container_width=True)
            fourth.plotly_chart(fig_designation_wise_leave, use_container_width=True)

            logging.info('Visualizations displayed successfully')
        else:
            st.error("An error occurred while generating visualizations. Please check the logs for details.")

# Run the app
if __name__ == "__main__":
    main()

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
