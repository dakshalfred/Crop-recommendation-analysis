# -*- coding: utf-8 -*-
"""Crop_Recommendation

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1canoNUY0f0finuyqQzXf88hdWWqEQHr5
"""

import streamlit as st
import requests
import pandas as pd
import io
import matplotlib.pyplot as plt
import seaborn as sns

# Title of the app
st.title("AgriSmart")

# Add custom HTML for title and description
st.markdown(
    """
    <h1 style="text-align:center;font-size:25px;padding:20px;">
        Welcome to the Crop Recommendation Analysis tool! 🌾  
    This app helps you determine the best crops for specific regions and seasons based on historical data.
    </h1>
    """,
    unsafe_allow_html=True,
)

# Add background image and semi-transparent overlay behind the text
st.markdown(
    """
    <style>
    /* Background image settings */
    .stApp {
        background-image: url('https://github.com/dakshalfred/Crop-recommendation-analysis/raw/main/images/specialization(2).jpg');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
        height: 100vh;  /* Ensure full height */
    }

    /* Semi-transparent overlay behind the text */
    .stApp::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(255, 255, 255, 0.3);  /* Black with 10% transparency */
        z-index: 0;  /* Ensure the overlay is behind the text */
    }

    /* Ensure text content appears above the overlay */
    .main-content {
        position: relative;
        z-index: 1;
        color: white;
        padding: 20px;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Add the main content wrapper
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Dropdowns and other inputs
option = st.selectbox("Choose an option", ["Get Crop Information", "Get Region Information"])
st.write("Your selected option is:", option)

# Function to load data from Google Drive link
def load_data_from_drive(link):
    # Extracting file ID from Google Drive URL
    file_id = link.split('/')[-2]
    url = f'https://drive.google.com/uc?id={file_id}'
    response = requests.get(url)
    return pd.read_csv(io.StringIO(response.text))

# Load dataset from Google Drive
data_url = 'https://drive.google.com/file/d/1XYvWxsYyEKkFt7VH1roZuBMtQHH8MnvG/view?usp=drive_link'  # Replace with your Google Drive link
data = load_data_from_drive(data_url)

# Data Preprocessing
# Data Preprocessing
if 'Crop' in data.columns and 'Production' in data.columns and 'Area' in data.columns:
    data.dropna(subset=['Crop', 'Production', 'Area'], inplace=True)  # Removing NaN values in important columns
else:
    st.warning("Columns 'Crop', 'Production', or 'Area' are missing from the dataset.")

# Option 1: Get Region Information (State -> District -> Season)
if option == "Get Region Information":
    # State selection
    states = data['State'].unique()
    state = st.selectbox("Choose State", states)

    # District selection based on state
    districts = data[data['State'] == state]['District'].unique()
    district = st.selectbox("Choose District", districts)

    # Season selection based on district
    seasons = data[(data['State'] == state) & (data['District'] == district)]['Season'].unique()
    season = st.selectbox("Select Season", seasons)

    # Filter data based on the selected state, district, and season
    filtered_data_region = data[(data['State'] == state) & 
                                 (data['District'] == district) & 
                                 (data['Season'] == season)]

    # Display data in tabular format
    st.subheader("Crops Information for the selected Region and Season")
    st.dataframe(filtered_data_region)

    # Option to switch between tabular and graphical format
    show_graph = st.checkbox("Show Graph")
    if show_graph:
        # Limit number of crops to display using a slider
        num_crops_to_display = st.slider('Select the number of crops to display', min_value=5, max_value=50, step=5)
        filtered_data_region_limited = filtered_data_region.head(num_crops_to_display)

        st.subheader(f"Top {num_crops_to_display} Crops Information for the selected Region and Season")
        st.dataframe(filtered_data_region_limited)

        # Create the barplot with rotated labels
        st.subheader("Graphical Representation")
        fig, ax = plt.subplots(figsize=(12, 8))  # Increase the figure size for better readability
        sns.barplot(data=filtered_data_region_limited, x="Crop", y="Area", ax=ax)

        # Rotate x-axis labels for better readability
        plt.xticks(rotation=90)
        st.pyplot(fig)

# Option 2: Get Crop Information (Crop -> State)
elif option == "Get Crop Information":
    # Crop selection
    crops = data['Crop'].unique()
    crop = st.selectbox("Choose Crop", crops)

    # State selection based on crop
    states_for_crop = data[data['Crop'] == crop]['State'].unique()
    state_for_crop = st.selectbox("Choose State", states_for_crop.tolist() + ["All of the above"])

    if state_for_crop != "All of the above":
        # Filter data based on the selected crop and state
        filtered_data_crop = data[(data['Crop'] == crop) & (data['State'] == state_for_crop)]

        # Display data in tabular format
        st.subheader(f"Data for {crop} in {state_for_crop}")
        st.dataframe(filtered_data_crop)

        # Option to switch between tabular and graphical format
        show_graph_crop = st.checkbox("Show Graph")
        if show_graph_crop:
            # Limit number of crops to display using a slider
            num_crops_to_display_crop = st.slider('Select the number of crops to display', min_value=5, max_value=50, step=5)
            filtered_data_crop_limited = filtered_data_crop.head(num_crops_to_display_crop)

            st.subheader(f"Top {num_crops_to_display_crop} Data for {crop} in {state_for_crop}")
            st.dataframe(filtered_data_crop_limited)

            # Create the barplot with rotated labels
            st.subheader("Graphical Representation")
            fig, ax = plt.subplots(figsize=(12, 8))  # Increase the figure size for better readability
            sns.barplot(data=filtered_data_crop_limited, x="District", y="Area", ax=ax)

            # Rotate x-axis labels for better readability
            plt.xticks(rotation=90)
            st.pyplot(fig)

    else:
        # Filter data for all states for the selected crop
        filtered_data_crop_all_states = data[data['Crop'] == crop]

        # Display data in tabular format
        st.subheader(f"Data for {crop} across all states")
        st.dataframe(filtered_data_crop_all_states)

        # Option to switch between tabular and graphical format
        show_graph_crop_all_states = st.checkbox("Show Graph for All States")
        if show_graph_crop_all_states:
            # Limit number of crops to display using a slider
            num_crops_to_display_crop_all_states = st.slider('Select the number of crops to display', min_value=5, max_value=50, step=5)
            filtered_data_crop_all_states_limited = filtered_data_crop_all_states.head(num_crops_to_display_crop_all_states)

            st.subheader(f"Top {num_crops_to_display_crop_all_states} Data for {crop} across all states")
            st.dataframe(filtered_data_crop_all_states_limited)

            # Create the barplot with rotated labels
            st.subheader("Graphical Representation")
            fig, ax = plt.subplots(figsize=(12, 8))  # Increase the figure size for better readability
            sns.barplot(data=filtered_data_crop_all_states_limited, x="State", y="Area", ax=ax)

            # Rotate x-axis labels for better readability
            plt.xticks(rotation=90)
            st.pyplot(fig)
