import streamlit as st
from wordcloud import WordCloud
from pages.Leave_Trends import all_data

leave_reason_columns= all_data[['reason', 'leave_type', 'status']]

leave_type = st.sidebar.selectbox(
    "Select the leave type:",
    options=leave_reason_columns["leave_type"].unique(),
)

df_selection = leave_reason_columns.query(
    "@leave_type== leave_type"
)



st.title("Leave Reasons Word Cloud")


# Create the word cloud with the logo mask
wordcloud = WordCloud(background_color = '#00172B', contour_color = 'white', colormap = 'copper',).generate(df_selection['reason'].to_string())

# Display the word cloud
st.image(wordcloud.to_array(), caption="Leave Reason", use_column_width=True)

df_selection['reason']
