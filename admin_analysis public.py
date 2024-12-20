import requests
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import time

#fixed global settings ########################################################################################################################################################
################################################################################################################################################################################

# design and color stuff ######################################################################################################################################################################
st.set_page_config(page_title="CrowdCapital", layout="wide")
with open("static/style.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)
plt.rcParams.update({
    'axes.facecolor': '#00002C',  # Background color of the plot area
    'axes.edgecolor': '#FFFFFF',  # Color of the axes border
    'xtick.color': '#FFFFFF',     # X-axis tick color
    'ytick.color': '#FFFFFF',     # Y-axis tick color
    'text.color': '#FFFFFF',      # General text color
    'axes.labelcolor': '#FFFFFF', # Axis label color
    'axes.titlecolor': '#FFFFFF'  # Title color
})

# API stuff ######################################################################################################################################################################
api_urls = {
    "start_ups": "link/to/nocodb/table",
    "users": "link/to/nocodb/table",
    "investments": "link/to/nocodb/table"
}
api_key = "***"

headers = {
    "accept": "application/json",
    "xc-token": api_key
}
pageInfo = {
        "pageSize": 400
    }
#functions ########################################################################################################################################################
######################################################################################################################################################################

# api call to get the data ###########################################################################################################################################
def fetch_data_to_dataframe(api_url):
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        # Annahme: Die Datensätze befinden sich unter 'list' oder 'records'
        return pd.DataFrame(data.get("list", []))
    else:
        print(f"Fehler beim Abrufen von {api_url}: {response.status_code}, {response.text}")
        return pd.DataFrame()
    
def fetch_data_to_dataframe_with_pagination(api_url):
    all_records = []
    offset = 0
    limit = 1000  

    while True:
        params = {"limit": limit, "offset": offset}
        response = requests.get(api_url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            records = data.get("list", [])
            all_records.extend(records)

            if len(records) < limit:
                # If fewer records than the limit are returned, we've reached the end
                break

            offset += limit
        else:
            print(f"Error fetching data from {api_url}: {response.status_code}, {response.text}")
            break

    return pd.DataFrame(all_records)

# dataframes ###########################################################################################################################################
def make_dfs(api_urls):

    df_start_ups = fetch_data_to_dataframe(api_urls["start_ups"])
    df_users = fetch_data_to_dataframe(api_urls["users"])
    df_investments = fetch_data_to_dataframe_with_pagination(api_urls["investments"])

    return df_start_ups, df_users, df_investments

# KPIs ###########################################################################################################################################
def calc_KPIs(df_users, df_investments):
    # read out how much capital is currently handed out (Talk to Khadim how this works)
    active_total = sum(df_users['active'])

    available_total_string = df_users.loc[df_users['active'] == 1, 'budget'].sum()

    if pd.isna(available_total_string):  # Check if the value is NaN
        available_total = 0
    else:
        available_total = int(available_total_string)

    invested_total = sum(df_users["invested"])
    not_invested_total = available_total - invested_total

    return active_total, available_total, invested_total, not_invested_total

# make fig 2 ###########################################################################################################################################
# make fig 2 ###########################################################################################################################################
def make_fig2_market(invested_total, not_invested_total):
    # Ensure values are numeric and non-negative
    invested_total = max(0, pd.to_numeric(invested_total, errors='coerce') if pd.notna(invested_total) else 0)
    not_invested_total = max(0, pd.to_numeric(not_invested_total, errors='coerce') if pd.notna(not_invested_total) else 0)

    # If both values are zero, avoid plotting an empty pie chart
    if invested_total == 0 and not_invested_total == 0:
        print("Warning: Both values are zero. Adjusting to dummy values.")
        invested_total, not_invested_total = 1, 1  # Prevent empty pie chart
    
    def make_autopct(values):
        def my_autopct(pct):
            total = sum(values)
            val = ((pct*total/100000000.0))
            return f'{pct:.1f}%\n({val:.2f}m€)'  # Format here can be adjusted as needed
        return my_autopct

    # Data for the pie chart
    labels = ['Invested', 'Not Invested']
    variables = [invested_total, not_invested_total]
    colors = ["#CA1551", "#D3D3D3"]

    fig2, ax = plt.subplots(figsize=(6, 4))
    wedges, texts, autotexts = ax.pie(
        variables,
        labels=labels,
        autopct=make_autopct(variables),  # Use custom function
        startangle=90,
        colors=colors,
        textprops={'color': "#FFFFFF", 'fontweight': 'bold', "size": 12},
        labeldistance=1.5,
        wedgeprops={'edgecolor': '#FFFFFF', 'linewidth': 2}
    )

    for autotext in autotexts:
        autotext.set_position((2.2 * autotext.get_position()[0], 2.2 * autotext.get_position()[1]))  # Adjust label positions
        autotext.set_color("#FFFFFF")
        autotext.set_fontsize(11)
        autotext.set_fontweight("normal")

    fig2.patch.set_facecolor('#00002C')
    ax.set_facecolor('#00002C')
    plt.tight_layout(pad=0)
    ax.axis('equal')
    return fig2



def make_fig1_invested_per_su(df_start_ups, df_investments):
    invested_per_su = []
    for su in df_start_ups["start_up_id"]:
        sum = 0
        for _, row in df_investments.iterrows():
            if row["start_up_id"]==su:
                sum += int(row["investment"])
        invested_per_su.append(sum)

    df_start_ups["investment_overall"] = invested_per_su
    df_start_ups = df_start_ups.sort_values(by="investment_overall", ascending=False).reset_index(drop=True)
        # create a bar-chart with the logos and names of the startups
    fig1, ax2 = plt.subplots(figsize=(8, 6))
    bars = ax2.bar(
        df_start_ups["name"], 
        df_start_ups["investment_overall"]/1000, 
        color=df_start_ups["color_HEX"], 
        edgecolor="#FFFFFF",  # White outline for bars
        linewidth=2  # Thickness of the outline
    )
    ax2.set_ylabel("Investment Amount (in 1000€)", fontsize=12, color="#FFFFFF", weight="bold")
    ax2.tick_params(axis="x", rotation=45)
    ax2.spines['bottom'].set_color('#FFFFFF')  # X-axis border
    ax2.spines['bottom'].set_linewidth(2) 
    ax2.spines['left'].set_color('#FFFFFF')    # Y-axis border
    ax2.spines['left'].set_linewidth(2) 
    ax2.spines['top'].set_color('#00002C')     # Optional top border
    ax2.spines['right'].set_color('#00002C') 

    fig1.patch.set_facecolor('#00002C')  # Set figure background to match the theme
    ax2.set_facecolor('#00002C')     

    # Adding labels to each bar
    for bar in bars:
        yval = int(bar.get_height())  # Get the height of the bar
        ax2.text(bar.get_x() + bar.get_width()/2, yval, f'{yval}k', ha='center', va='bottom', 
                fontsize=10, fontweight="bold",
                color='#FFFFFF')
    return fig1

#create the page ########################################################################################################################################################
################################################################################################################################################################################

def create_dynamic_page(api_urls):
    placeholder = st.empty()  # Platzhalter für dynamische Inhalte

    while True:
        # Daten abrufen
        df_start_ups, df_users, df_investments = make_dfs(api_urls)
        active_total, available_total, invested_total, not_invested_total = calc_KPIs(df_users, df_investments)

        # Diagramme aktualisieren
        fig1 = make_fig1_invested_per_su(df_start_ups, df_investments)
        fig2 = make_fig2_market(invested_total, not_invested_total)

        # Seite innerhalb des Platzhalters aktualisieren
        with placeholder.container():
            st.title("CrowdCapital Investment Dashboard")
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Investment per Start-Up")
                st.pyplot(fig1)
                plt.close(fig1)  
            with col2:
                st.subheader(f"Overall available")
                st.pyplot(fig2)
                plt.close(fig2)  

            # Tabellen
            st.text("") 
            st.header("Detailed Overview")
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Investment per Start-up")
                df_start_ups = df_start_ups.sort_values(by="investment_overall", ascending=False)
                st.table(df_start_ups[["name", "investment_overall"]])
            with col2:
                st.subheader(f"KPIs")
                data = {
                    "Description": ["Active Users", "Market Size", "Invested", "Not Invested"],
                    "Value": [active_total, available_total, invested_total, not_invested_total]
                }
                df = pd.DataFrame(data)
                st.table(df)

        # Warte 10 Sekunden vor der nächsten Aktualisierung
        time.sleep(5)


# Hauptlogik ####################################################################################################################
create_dynamic_page(api_urls)


