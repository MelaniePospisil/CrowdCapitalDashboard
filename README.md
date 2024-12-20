# CrowdCapital Investment Dashboard

## 01 token gen
This part of the CrowdCapital Investment Dashboard script is responsible for generating secure JWT (JSON Web Tokens) for user authentication and creating QR codes that embed these tokens. The tokens and QR codes are used to facilitate user access to the platform through a secure and convenient method.

### Functionality
- **Token Generation:** The script generates 350 unique JWTs using a predefined secret key. Each token is valid for a limited time and includes permissions for both reading and writing.
- **CSV Export:** After generating the tokens, they are saved into a CSV file named `tokens.csv` for easy distribution or further processing.
- **QR Code Generation:** For each token, a QR code is generated. These QR codes link to a specified URL with the token as a parameter, allowing users to access the platform by scanning the code.
- **Base64 Encoding:** QR codes are stored as Base64 strings, facilitating their embedding in web pages or other media without the need for additional image files.

## 02 base64 to img 
This portion of the script handles the extraction of QR codes from a CSV file and the storage of these codes as PNG images in a designated folder. This is particularly useful for offline access or physical distribution.

### Functionality

- **CSV Loading:** Loads a CSV file containing encoded QR codes and associated user IDs. The path to the CSV file must be specified.
- **Directory Creation:** Automatically creates a directory to store the QR code images if it doesn't already exist.
- **Image Saving:** Decodes each QR code from Base64 format and saves it as a PNG image file. Each file is named after the corresponding user ID for easy identification.

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
