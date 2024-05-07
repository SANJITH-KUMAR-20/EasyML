
import streamlit as st
import pandas as pd
from ml_backend.Back_Utils import *

# Page configurations
st.set_page_config(page_title="EasyML", page_icon=":bar_chart:")

# Sidebar navigation
page = st.sidebar.radio("Navigation", ["Home", "Manipulate Data", "Build Model", "Visualize Data", "Chat with PY", "Deploy Model"])

parent_data_set = None
global g_current_state 

#GLOBAL_SESSION_STATES
if "button" not in st.session_state:
    st.session_state.button = {}

if "impute" not in st.session_state:
    st.session_state.impute = {}

# Home page

def clicked(button : str, nested : bool = False, nested_key : str = None, strategy : str = None):
    if not nested:
        st.session_state.button[button] = True
    else:
        if strategy == "impute":
            st.session_state.impute[button][nested_key] = True

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
            if "data_set" in st.session_state:
                st.session_state.data_set["current_state"] = st.session_state.data_set["parent_Data_set"]

        except:
            if not st.session_state.button["csv_upload"]:
                st.caption("Unable to Read CSV")

    

# Manipulate Data page
elif page == "Manipulate Data":
    st.title("Manipulate Data")
    st.write("Here you can process your data before selecting a training...")
    # if "data_set" in st.session_state:
    #     st.session_state.data_set["current_state"] = st.session_state.data_set["parent_Data_set"]
    current_state = st.session_state.data_set["current_state"]
    selected_operation = st.selectbox("Select the operation", ["None", "Drop Column","Impute","Standardize","Encode"])

    if selected_operation == "Drop Column":
        if "drop_button" not in st.session_state.button:
            st.session_state.button["drop_button"] = False
        selected_columns = st.multiselect("select columns to drop",list(current_state.columns))
        st.button("drop selected columns", on_click=clicked, args= ["drop_button"])
        if selected_columns and st.session_state.button["drop_button"]:
            data_drop_strategy = drop_column(selected_columns, current_state)
            st.session_state.data_set["current_state"] = data_drop_strategy
        current_state = st.session_state.data_set["current_state"]
        g_current_state = current_state
        st.write(current_state.head())
        st.session_state.button["drop_button"] = False

    if selected_operation == "Impute":
        if "impute_button" not in st.session_state.button:
            st.session_state.button["impute_button"] = False
        # st.session_state.button["impute_button"] = False
        impute_strategies = st.multiselect("Select the impute strategy", ["Simple Imputer", "KNN Imputer"])
        
        for impute_strategy in impute_strategies:
            if impute_strategy == "Simple Imputer":
                if "Simple Imputer" not in st.session_state.impute:
                    st.session_state.impute["Simple Imputer"] = {"set_params" : False, "columns" : [], "strategy" : "mean", "fill_value" : None, "impute" : False, "n_nearest_neigbours" : 3}
                # st.session_state.impute["Simple Imputer"]["set_params"] = False
                st.button(f"Set Parameters for {impute_strategy}", on_click= clicked, args= [impute_strategy, True,"set_params", "impute"])

                if st.session_state.impute["Simple Imputer"]["set_params"]:

                    strat = st.selectbox("Impute strategy", ["mean","median","constant"])
                    affected_columns = st.multiselect("Columns to be imputed", list(st.session_state.data_set["current_state"].columns), key =1)
                    st.session_state.impute["Simple Imputer"]["strategy"] = strat
                    if strat == "constant":
                        fill_val = st.number_input("Enter Fill_value")
                        st.session_state.impute["Simple Imputer"]["fill_value"] = fill_val

                    st.button("Impute",on_click=clicked,args=[impute_strategy, True,"impute", "impute"],  key = 2)
                    if st.session_state.impute["Simple Imputer"]["impute"]:
                        st.session_state.data_set["current_state"] = impute_columns(affected_columns, st.session_state.data_set["current_state"], "Simple_Imputer", st.session_state.impute["Simple Imputer"])
                    g_current_state = st.session_state.data_set["current_state"]
                    st.write(st.session_state.data_set["current_state"])


            if impute_strategy == "KNN Imputer":
                if "KNN Imputer" not in st.session_state.impute:
                    st.session_state.impute["KNN Imputer"] = {"set_params" : False, "columns" : [], "n_nearest_neigbours" : 3, "impute" : False,"strategy" : "mean", "fill_value" : None}
                # st.session_state.impute["KNN Imputer"]["set_params"] = False
                st.button(f"Set Parameters for {impute_strategy}", on_click= clicked, args= [impute_strategy, True,"set_params", "impute"])

                if st.session_state.impute["KNN Imputer"]["set_params"]:

                    n_nearest_neigbours = st.number_input("Enter the N Nearest Neighbours")
                    affected_columns = st.multiselect("Columns to be imputed", list(st.session_state.data_set["current_state"].columns), key = 3)
                    st.session_state.impute["KNN Imputer"]["n_nearest_neigbours"] = n_nearest_neigbours

                    st.button("Impute",on_click=clicked,args=[impute_strategy, True,"impute", "impute"], key =4)
                    if st.session_state.button["impute_button"]:
                        st.session_state.data_set["current_state"] = impute_columns(affected_columns, st.session_state.data_set["current_state"], "KNN_Imputer", st.session_state.impute["KNN Imputer"])
                    g_current_state = st.session_state.data_set["current_state"]
                    st.write(st.session_state.data_set["current_state"])
    if selected_operation == "Standardize":
        if "standardize_button" not in st.session_state.button:
            st.session_state.button["standardize_button"] = False
        # st.session_state.button["impute_button"] = False
        scaling_strategies = st.multiselect("Select the Scaling Strategy", ["MinMax Scaler", "Standard Scaler"])

        for strategy in scaling_strategies:

            if strategy == "MinMax Scaler":
                data = st.session_state.data_set["current_state"]
                columns_to_scale = st.multiselect("Select the columns to Scale", data.columns)
                if "minscale" not in st.session_state.button:
                    st.session_state.button["minscale"] = False
                st.button("Scale", on_click=clicked, args=["minscale"])
                if st.session_state.button["minscale"]:
                    st.session_state.data_set["current_state"] = standardize(list(columns_to_scale),data,strategy)
                    st.write(st.session_state.data_set["current_state"])

            if strategy == "Standard Scaler":
                data = st.session_state.data_set["current_state"]
                columns_to_scale = st.multiselect("Select the columns to Scale", data.columns)
                if "stdscale" not in st.session_state.button:
                    st.session_state.button["stdscale"] = False
                st.button("Scale", on_click=clicked, args=["stdscale"])
                if st.session_state.button["stdscale"]:
                    st.session_state.data_set["current_state"] = standardize(list(columns_to_scale),data,strategy)
                    st.write(st.session_state.data_set["current_state"])




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
