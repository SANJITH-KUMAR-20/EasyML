
import streamlit as st
import pandas as pd
from Back_Utils import *

# Page configurations
st.set_page_config(page_title="EasyML", page_icon=":bar_chart:")

# Sidebar navigation
page = st.sidebar.radio("Navigation", ["Home", "Manipulate Data", "Build Model", "Visualize Data", "Chat with PY", "Deploy Model"])

parent_data_set = None
# Home page
if page == "Home":
    st.markdown('<p style="text-align: center;"><img src="Frontend\Data\logo-black.png" alt="Logo" style="border-radius: 50%; max-width: 200px;"></p>', unsafe_allow_html=True)
    st.title("Welcome to EasyML!")
    st.write("An easy-to-use platform for low-code machine learning and data science.")
    st.write("Explore the features in the sidebar.")
    # st.image("Frontend\Data\logo-black.png", use_column_width=True, output_format="png", channels="BGR", width=200, height=200, caption="EasyML")  # Replace with your logo
    
    if "csv_clicked" not in st.session_state:
        st.session_state.csv_clicked = {1:False}
        st.session_state.clm_selected = {1 : False}

    def clicked(button):
        st.session_state.csv_clicked[button] = True

    st.button("Let's get started", on_click=clicked, args=[1])
    if st.session_state.csv_clicked[1]:
        st.header("You are now ready for your machine learning experience")

        # CSV upload button
        uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

        if uploaded_file is not None:
            st.success("CSV file uploaded successfully!")

        try:
            df = pd.read_csv(uploaded_file)
            st.write(df.head())
            parent_data_set = df

        except:
            st.caption("Unable to Read CSV")

    

# Manipulate Data page
elif page == "Manipulate Data":
    st.title("Manipulate Data")
    st.write("Here you can process your data before selecting a training...")
    manipulated_data = parent_data_set
    selected_operation = st.selectbox("Select the operation", ["None", "drop column","impute"])

    if selected_operation == "drop column":
        selected_columns = st.multiselect("select columns to drop",list(manipulated_data.columns))

        data_drop_strategy = drop_column(selected_columns, manipulated_data)




    # Add your code for data manipulation here

# Build Model page
elif page == "Build Model":
    st.title("Build Model")

    # Add your code for model building here

# Visualize Data page
elif page == "Visualize Data":
    st.title("Visualize Data")

    # Add your code for data visualization here

# Chat with PY page
elif page == "Chat with PY":
    st.title("Chat with PY")

    # Add your code for interacting with Python here

# Deploy Model page
elif page == "Deploy Model":
    st.title("Deploy Model")

    # Add your code for model deployment here
