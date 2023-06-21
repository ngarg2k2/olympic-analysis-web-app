import streamlit as st
import pandas as pd
import preprocessing,helper
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessing.preprocess(df,region_df)

st.sidebar.title("Olympics Analysis")
st.sidebar.image('https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Olympic_flag.svg/2560px-Olympic_flag.svg.png')
user_menu=st.sidebar.radio(
    'Select an Option',
        ('Medal Tally','Overall Analysis','Country-Wise Analysis','Athlete-Wise Analysis')
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

    st.title("No of Events over time(Every Sports)")
    fig,ax=plt.subplots(figsize=(25,25))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax=sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype('int'),annot=True)

    st.pyplot(fig)

    st.title("Most successful Athletes")
    sport_list=df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport=st.selectbox('Select the sport',sport_list)
    number=[5,10,15,20]
    selected_number=st.selectbox('Select number of top players',number)
    x=helper.most_sucsessful(df,selected_sport,selected_number)
    st.table(x)

if user_menu == 'Country-Wise Analysis':
    st.sidebar.title("Country-wise Analysis")

    country_list=df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country=st.sidebar.selectbox('Select the country',country_list)
    country_df=helper.year_wise_medal_tally(df,selected_country)
    fig=px.line(country_df,x="Year",y="Medal")

    st.title(selected_country+" Medal Tally over the years")
    st.plotly_chart(fig)

    st.title(selected_country+" excels in the following sports")
    pt=helper.country_event_heatmap(df,selected_country)
    fig,ax=plt.subplots(figsize=(25,25))
    ax=sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title("Top 10 athletes of "+selected_country)
    tmp=helper.most_sucsessful_athletes(df,selected_country)
    st.table(tmp)

if user_menu == 'Athlete-Wise Analysis':
    st.title("Distribution of Age")
    athletes_df = df.drop_duplicates(subset=['Name', 'region'])
    # athletes_df
    x1 = athletes_df['Age'].dropna()
    x2 = athletes_df[athletes_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athletes_df[athletes_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athletes_df[athletes_df['Medal'] == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    # it gives 3 graph line hist and rug (but we need only line)
    # athletes_df['Age'].dropna()
    # fig.show()
    # fig.update_layout(autosize=False,width=800,height=600)
    st.plotly_chart(fig)


    # famous_sports = df['Sport'].dropna().unique().tolist()
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    # famous_sports
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    x = []
    name = []
    for sport in famous_sports:
        temp_df = athletes_df[athletes_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)
    # st.table(x)
    # st.table(name)
    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    # fig.update_layout(autosize=False, width=800, height=600)
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df, selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(data=temp_df,x="Weight",y="Height",hue="Medal", style=temp_df['Sex'], s=60)
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male","Female"])
    # fig.update_layout(autosize=False, width=800, height=600)
    st.plotly_chart(fig)

