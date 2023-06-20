import  numpy as np
def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',ascending=False).reset_index()
    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    return medal_tally

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years,country


def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    # x['Gold'] = x['Gold'].astype('int')
    # x['Silver'] = x['Silver'].astype('int')
    # x['Bronze'] = x['Bronze'].astype('int')
    # x['total'] = x['total'].astype('int')

    return x

def nations_over_time(df,type):
    # now we need to plot a graph between year and no of participated nation
    nation_over_time = df.drop_duplicates(['Year', type])['Year'].value_counts().reset_index().sort_values('Year')
    nation_over_time = nation_over_time.rename(columns={'Year': 'Editions', 'count': type})

    return nation_over_time

# now we need to make a function in which when we pass the sports it will tell the most succesfull person in that sports
def most_sucsessful(df,sport,number):
    # we have some NA values in df but we dont need that so we delete them first
    temp_df=df.dropna(subset='Medal')

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x=temp_df['Name'].value_counts().reset_index().head(number).merge(df,left_on='Name',right_on='Name',how='left')[['Name','count','Sport','region']].drop_duplicates('Name')
    x=x.rename(columns={'count':'Medals'})
    return x