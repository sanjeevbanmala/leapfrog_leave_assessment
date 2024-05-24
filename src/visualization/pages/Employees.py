import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pages.Leave_Trends import conn

sql= '''select e.employee_id, e.first_name|| ' ' || e.last_name as full_name,e.first_name, e.middle_name, e.last_name, e.email, d.department_name, d2.designation_name  
from dbo.employees e 
inner join dbo.departments d on d.department_id = e.department_id 
inner join dbo.designations d2 on d2.designation_id = e.designation_id ;
'''

alloc_sql= '''
select distinct e.employee_id, a.allocation_id, a."name", a.type  
from dbo.employees e 
inner join dbo.employee_allocations ea on ea.employee_id =e.employee_id 
inner join dbo.allocations a on a.allocation_id =ea.allocation_id ;
'''
leave_balance_sql='''
select e.employee_id,
LEFT(cast(fy.start_date as VARCHAR), 4) ||'/'|| LEFT(cast(fy.end_date as VARCHAR), 4) as fiscal_date,
lt.leave_type, sum(el.leave_days) as total, lt.default_days 
from dbo.employee_leaves el 
inner join dbo.employees e  on e.employee_id = el.employee_id
inner join dbo.leave_types lt on el.leave_type_id= lt.leave_type_id 
inner join dbo.fiscal_year fy on fy.fiscal_id =el.fiscal_id 
where lt.leave_type  in('Paternity','Annual','Sick','Menstruation','Discretionary', 'Bereavement')
group by e.employee_id, fiscal_date, lt.leave_type,  lt.default_days ; 
'''

st.subheader("Employee Details")

data = pd.read_sql(sql,conn)
alloc_data = pd.read_sql(alloc_sql, conn)
leave_data = pd.read_sql(leave_balance_sql, conn)

# Convert two columns of DataFrame into dictionary
result_dict = dict(zip(data['full_name'], data['employee_id']))

# Select box
selected_display_value = st.sidebar.selectbox('Select an option:', sorted(list(result_dict.keys())))

# Retrieve the associated variable based on the selected display value
selected_associated_variable = result_dict[selected_display_value]

emp_details= data.query(
    "employee_id == @selected_associated_variable"
)

alloc_data= alloc_data.query(
    "employee_id == @selected_associated_variable"
)


emp_details=emp_details[['first_name', 'last_name', 'email', 'department_name', 'designation_name']]
alloc_details = alloc_data[['allocation_id', 'name', 'type']]

st.write(emp_details.style.set_table_attributes('style="width:100%"'))
st.subheader("Allocation Details")

st.write(alloc_details.style.set_table_attributes('style="width:500%"'))




st.subheader("Used Leave vs Balance")

fiscal_id = st.selectbox(
    "Select the Fiscal Date:",
    options=leave_data["fiscal_date"].unique()
)
# Define the number of columns you want
num_columns = 2  # You can change this based on your preference

# Initialize Streamlit columns
columns = st.columns(num_columns)

# Counter to keep track of figures
figure_counter = 0

leave_details = leave_data.query(
    "employee_id == @selected_associated_variable & fiscal_date == @fiscal_id"
)

for index, row in leave_details.iterrows():

    value= row['total']
    # Create the gauge chart
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        title = {'text': row['leave_type'] +' Default: ' + str(row['default_days'])},
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {'axis': {'range': [None, row['default_days']]}}
    ))
    
    # Update the layout to remove axis ticks and labels
    fig.update_layout(
        xaxis = {'showticklabels': False},
        yaxis = {'showticklabels': False}
    )
    # Show the chart in a column
    columns[figure_counter % num_columns].plotly_chart(fig,use_container_width=True, height=100)
    figure_counter += 1
    
    