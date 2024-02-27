
import streamlit as st
import pandas as pd
from Back_Utils import *

# Page configurations
st.set_page_config(page_title="EasyML", page_icon=":bar_chart:")

# Sidebar navigation
page = st.sidebar.radio("Navigation", ["Home", "Manipulate Data", "Build Model", "Visualize Data", "Chat with PY", "Deploy Model"])

parent_data_set = None
# Home page
if "button" not in st.session_state:
        st.session_state.button = {}

def clicked(button):
        st.session_state.button[button] = True

if page == "Home":
    st.markdown('<p style="text-align: center;"><img src="Frontend\Data\logo-black.png" alt="Logo" style="border-radius: 50%; max-width: 200px;"></p>', unsafe_allow_html=True)
    st.title("Welcome to EasyML!")
    st.write("An easy-to-use platform for low-code machine learning and data science.")
    st.write("Explore the features in the sidebar.")
    # st.image("Frontend\Data\logo-black.png", use_column_width=True, output_format="png", channels="BGR", width=200, height=200, caption="EasyML")  # Replace with your logo
    
    if "csv_upload" not in st.session_state.button:
        st.session_state.button["csv_upload"] = False
        
    if "clicked" not in st.session_state.button:
        st.session_state.button["clicked"] = False

    st.button("Let's get started", on_click=clicked, args=["clicked"])
    if st.session_state.button["clicked"]:
        st.header("You are now ready for your machine learning experience")

        # CSV upload button
        uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

        if uploaded_file is not None:
            st.success("CSV file uploaded successfully!")

        try:
            df = pd.read_csv(uploaded_file)
            st.write(df.head())
            st.session_state.button["csv_upload"] = True
            if "data_Set" not in st.session_state:
                st.session_state.data_set = {"parent_Data_set" : df}
            parent_data_set = df

        except:
            if not st.session_state.button["csv_upload"]:
                st.caption("Unable to Read CSV")

    

# Manipulate Data page
elif page == "Manipulate Data":
    st.title("Manipulate Data")
    st.write("Here you can process your data before selecting a training...")
    if "data_set" in st.session_state:
        st.session_state.data_set["manipulated_data"] = st.session_state.data_set["parent_Data_set"]
    manipulated_data = st.session_state.data_set["manipulated_data"]
    selected_operation = st.selectbox("Select the operation", ["None", "drop column","impute"])

    if selected_operation == "drop column":
        if "drop_button" not in st.session_state.button:
            st.session_state.button["drop_button"] = False
        selected_columns = st.multiselect("select columns to drop",list(manipulated_data.columns))
        st.button("drop selected columns", on_click=clicked, args= ["drop_button"])
        if selected_columns and st.session_state.button["drop_button"]:
            data_drop_strategy = drop_column(selected_columns, manipulated_data)
            st.session_state.data_set["manipulated_data"] = data_drop_strategy
            manipulated_data = st.session_state.data_set["manipulated_data"]
            st.write(manipulated_data.head())




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
