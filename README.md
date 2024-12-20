# CrowdCapital Investment Dashboard

## Overview
This Python application is designed to provide a dynamic dashboard for visualizing investments and other key performance indicators for our START Munich investment app for pitching events using Streamlit. The app fetches the data from NocoDB, processes it, and visualizes it using Matplotlib and Streamlit.

## Prerequisites
- Python 3.6 or higher
- Streamlit
- Requests
- Pandas
- Matplotlib

## Configuration
Before running the application, update the `api_urls` dictionary and `api_key` in the script to match your actual API endpoint and credentials.

## Features
- **Dynamic Updates:** The dashboard updates periodically (every 5sec) to display the latest data.
- **Interactive Visuals:** Utilizes Streamlit for an interactive web application experience.
- **KPI Tracking:** Calculates and displays KPIs such as total active users, market size, total invested, and total not invested.

## Custom Styles
The app includes a custom CSS for styling, which is applied globally to enhance the visual appeal of the dashboard and to make sure that the graphs have the correct background color to be seamlessly pasted into the presentation.

## Functionality
The application is structured into several functions:
- **Data Fetching:** Functions to fetch data from the API with and without pagination.
- **Data Processing:** Functions to compute KPIs and prepare data for visualization.
- **Visualization:** Functions to generate matplotlib figures for investment distributions and KPIs.
- **Page Layout:** Uses Streamlit to layout the page dynamically.

## Limitations
- The application assumes specific JSON structure from the API responses.
- It is dependent on the availability and response format of the NocoDB API.

## Future Improvements
- Include more detailed analytics.
- Realtime updates instead of every five seconds 
- Upgrade to a more interactive front-end

## Author
Melanie Pospisil
