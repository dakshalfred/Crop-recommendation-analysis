# -*- coding: utf-8 -*-
"""Crop_Recommendation

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1canoNUY0f0finuyqQzXf88hdWWqEQHr5
"""

# Description or Title
st.markdown(
    """
    <h1 style="color:white;text-align:center;font-size:25px;padding:20px;background:rgba(0,0,0,0);">
        Welcome to the Crop Recommendation Analysis tool! 🌾  
    This app helps you determine the best crops for specific regions and seasons based on historical data.
    </h1>
    """,
    unsafe_allow_html=True,
)

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io
import requests

import warnings
warnings.filterwarnings("ignore", message="missing ScriptRunContext!")

# Function to load data from Google Drive link
def load_data_from_drive(link):
    # Extracting file ID from Google Drive URL
    file_id = link.split('/')[-2]
    url = f'https://drive.google.com/uc?id=1XYvWxsYyEKkFt7VH1roZuBMtQHH8MnvG'
    response = requests.get(url)
    return pd.read_csv(io.StringIO(response.text))

# Streamlit Interface
st.title("Crop Recommendation System")

# Option selection for the user
option = st.selectbox("Choose an option", ["Get Crop Information", "Get Region Information"])

# Load dataset from Google Drive (use the actual Google Drive link here)
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
        fig, ax = plt.subplots()
        sns.barplot(data=filtered_data_region, x="Crop", y="Area", ax=ax)
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
            st.subheader("Graphical Representation")
            fig, ax = plt.subplots()
            sns.barplot(data=filtered_data_crop, x="District", y="Area", ax=ax)
            st.pyplot(fig)

    else:
        # Show data for all states for the selected crop
        st.subheader(f"Data for {crop} in All States")
        filtered_data_crop_all = data[data['Crop'] == crop]
        st.dataframe(filtered_data_crop_all)

        # Option to switch between tabular and graphical format
        show_graph_crop_all = st.checkbox("Show Graph")
        if show_graph_crop_all:
            st.subheader("Graphical Representation")
            fig, ax = plt.subplots()
            sns.barplot(data=filtered_data_crop_all, x="State", y="Area", ax=ax)
            st.pyplot(fig)

# Displaying message if data is not available for selected options
st.write("Note: If you select a region or crop with missing data, the system will show 'Data not available'.")


import streamlit as st
from streamlit.components.v1 import html

# Slideshow images
images = [
    "https://drive.google.com/file/d/1m7SMWjsST26U2pbz84TJ8SfTtC-3GrkP/view?usp=drive_link",  # Replace with your image URLs
    "https://drive.google.com/file/d/1GYJzuUbH7-_R8B8z6CGhyxSHISH4Hapl/view?usp=drive_link",
    "https://drive.google.com/file/d/1SNgVLNTH8o9qvT-_O4NI2QGQxNNd6H5x/view?usp=drive_link",
    "https://drive.google.com/file/d/1uzESAjpQ86bQmreq0A8TQY1j2jGh4LUb/view?usp=drive_link",
    "https://drive.google.com/file/d/1kOaD8pUB7-dLTYNXATO8a1FvFyLUeNFY/view?usp=drive_link",
]

# HTML and CSS for slideshow
slideshow_html = f"""
<style>
    body {{
        margin: 0;
        overflow: hidden;
    }}
    .slideshow {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        overflow: hidden;
    }}
    .slideshow img {{
        position: absolute;
        width: 100%;
        height: 100%;
        object-fit: cover;
        animation: fade 30s infinite;
    }}
    @keyframes fade {{
        {''.join([f'{i*100/len(images)}% {{ opacity: 0; }} {((i+1)*100/len(images))-5}% {{ opacity: 1; }} ' for i in range(len(images))])}
    }}
</style>
<div class="slideshow">
    {"".join([f'<img src="{img}" style="animation-delay: {i*5}s;">' for i, img in enumerate(images)])}
</div>
"""

# Render slideshow background
html(slideshow_html, height=0)


