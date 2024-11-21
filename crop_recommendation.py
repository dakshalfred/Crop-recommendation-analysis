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
st.title("Crop Recommendation System")

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
    /* Ensure the background image covers the entire viewport */
    .stApp {
        background-image: url('https://github.com/dakshalfred/Crop-recommendation-analysis/raw/main/images/specialization(2).jpg');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
        height: 100vh; /* Ensure full height */
    }

    /* Semi-transparent overlay behind the text */
    .stApp::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);  /* Black with 50% transparency */
        z-index: -1;  /* Ensure the overlay is behind the text */
    }

    /* Ensure the text content appears above the overlay */
    .main-content {
        position: relative;
        z-index: 1;
        color: white;
        padding: 20px;
        border-radius: 10px;
    }

    /* Adjust the content position */
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
data.dropna(subset=['Crop', 'Production', 'Area'], inplace=True)  # Removing NaN values in important columns

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
        st.subheader("Graphical Representation")
        fig, ax = plt.subplots(figsize=(9 * 0.6, 6 * 0.6))  # Resize chart to 60% of original size
        sns.barplot(data=filtered_data_region, x="Crop", y="Area", ax=ax)
        
        # Rotate x-axis labels to prevent overlap
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()  # Adjust layout for better spacing

        st.pyplot(fig)

# Option 2: Get Crop Information (Crop -> State -> District -> Season)
if option == "Get Crop Information":
    # Crop selection
    crops = data['Crop'].unique()
    crop = st.selectbox("Choose Crop", crops)

    # State selection based on crop
    states_for_crop = data[data['Crop'] == crop]['State'].unique()
    state_for_crop = st.selectbox("Choose State", states_for_crop)

    # District selection based on state
    districts_for_crop = data[data['State'] == state_for_crop]['District'].unique()
    district_for_crop = st.selectbox("Choose District", districts_for_crop)

    # Season selection based on district
    seasons_for_crop = data[(data['State'] == state_for_crop) & (data['District'] == district_for_crop)]['Season'].unique()
    season_for_crop = st.selectbox("Select Season", seasons_for_crop)

    # Filter data based on the selected crop, state, district, and season
    filtered_data_crop = data[(data['Crop'] == crop) & 
                               (data['State'] == state_for_crop) & 
                               (data['District'] == district_for_crop) & 
                               (data['Season'] == season_for_crop)]

    # Display data in tabular format
    st.subheader("Crops Information for the selected Crop, State, District, and Season")
    st.dataframe(filtered_data_crop)

    # Option to switch between tabular and graphical format
    show_graph_crop = st.checkbox("Show Graph")
    if show_graph_crop:
        st.subheader("Graphical Representation")
        fig, ax = plt.subplots(figsize=(9 * 0.6, 6 * 0.6))  # Resize chart to 60% of original size
        sns.barplot(data=filtered_data_crop, x="District", y="Area", ax=ax)
        
        # Rotate x-axis labels to prevent overlap
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()  # Adjust layout for better spacing

        st.pyplot(fig)

# End the main content wrapper
st.markdown('</div>', unsafe_allow_html=True)
