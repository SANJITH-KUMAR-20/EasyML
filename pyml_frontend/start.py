import streamlit as st
import pandas as pd

def show():
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