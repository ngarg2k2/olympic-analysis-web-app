import streamlit as st
import pandas as pd
import preprocessing,helper
import numpy as np
import plotly.express as px

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessing.preprocess(df,region_df)

st.sidebar.title("Olympics Analysis")
user_menu=st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-Wise Analysis','Athete-Wise Analysis')
)

# st.dataframe(df)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " performance in " + str(selected_year) + " Olympics")
    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    # st.sidebar.header("Overall Analysis")
    # edition=df['Year'].unique().shape[0]-1
    edition=len(df['Year'].unique())-1
    cities=len(df['City'].unique())
    sports=len(df['Sport'].unique())
    events=len(df['Event'].unique())
    athletes=len(df['Name'].unique())
    nations=len(df['region'].unique())

    st.title("Top Statistics")
    col1,col2,col3=st.columns(3)
    with col1:
        st.header("Editions")
        st.title(edition)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nation")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    nation_over_time=helper.nations_over_time(df,'region')
    fig = px.line(nation_over_time, x="Editions", y="region")
    st.title("Participating Nations over the year")
    st.plotly_chart(fig)

    nation_over_time=helper.nations_over_time(df, 'Event')
    fig = px.line(nation_over_time, x="Editions", y="Event")
    st.title("Events over the year")
    st.plotly_chart(fig)

    nation_over_time=helper.nations_over_time(df, 'Name')
    fig = px.line(nation_over_time, x="Editions", y="Name")
    st.title("Atheletes over the year")
    st.plotly_chart(fig)
    # st.dataframe(df)
