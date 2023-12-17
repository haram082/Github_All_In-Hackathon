import streamlit as st
import pandas as pd
import numpy as np
import numpy as np
import seaborn as sns
from insights import get_2024_gamelog, games_against
from shot_charts import get_player_shotchartdetail, shot_chart
from nba_api.stats.static import players
player_dict = players.get_players()

player= None

st.title('NBA Sports Betting Explorer')
st.markdown("""
            This interactive web application enables users to explore NBA player statistics to gain insights for sports betting decisions. Users can input an NBA player name and a rival team, then view visualizations of that player's recent performance trends overall and specifically when playing against the selected rival team.

The app retrieves NBA player data from the [NBA API](https://github.com/swar/nba_api). It allows selecting a player like LeBron James and a rival team like the Celtics. The user can choose which stats categories to visualize like points, rebounds, blocks etc.

Interactive visualizations are then generated such as:

Line plots showing the player's selected stat totals over recent games this season.
Bar charts summarizing the player's average statistical outputs from their last 5 games.
Shot charts indicating the player's shooting percentages from different court locations.
Comparison line plots contrasting the player's stats when playing the rival team vs their season averages.
            
These visualizations enable quickly identifying performance trends, hot/cold streaks, potential matchup weaknesses, scoring efficiency by shot location, and more useful insights. The app provides an intuitive interface to access rich NBA data analytics for gaining an information edge when sports betting. Users can leverage the tool to determine strategic wagers based on visualized player vs opponent statistical profiles and trends.

The code demonstrates integrating the NBA API, Pandas, Matplotlib, Seaborn, and Plotly to build a practical data visualization web application with Streamlit in Python. """)

st.sidebar.header('User Input Features')
# creata an input for the user to enter a player name
player_name = st.sidebar.text_input('Enter a player name', 'LeBron James')

# create an input of a list of nba team to choose from
rival_team = st.sidebar.selectbox('Select a team', ['BOS', 'BRK', 'NYK', 'PHI', 'TOR', 'CHI', 'CLE', 'DET', 'IND', 'MIL', 'ATL', 'CHA', 'MIA', 'ORL', 'WAS', 'DEN', 'MIN', 'OKC', 'POR', 'UTA', 'GSW', 'LAC', 'LAL', 'PHX', 'SAC', 'DAL', 'HOU', 'MEM', 'NOP', 'SAS'])
# create an input of a list of different stats to choose from where you can choose multiple
selected_stats = st.sidebar.multiselect('Select stats', ['PTS', 'REB', 'AST', 'BLK', 'STL', 'TOV', 'FGA', 'FGM', 'FG3A', 'FG3M', 'FTA', 'FTM'])

# add an enter button
if st.sidebar.button('Enter'):
    st.write('You entered:', player_name)
    st. write('You selected:', rival_team)
    player = [player for player in player_dict if player['full_name'] == player_name][0]
    if len(player) == 0:
        st.write('No player found')
    else:
        st.image(f"https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/{player['id']}.png")




if player:
    last_games = get_2024_gamelog(player['id'])
    against_rival_team = games_against(rival_team,player['id'])

    # create a line graph for selected stats
    import plotly.graph_objects as go
    fig = go.Figure()
    for stat in selected_stats:
        fig.add_trace(go.Scatter(x=last_games['GAME_DATE'], y=last_games[stat], mode='lines+markers', name=stat))
    fig.update_layout(title=f'{player_name} Stats This Year', xaxis_title='Date', yaxis_title='Stats')
    st.plotly_chart(fig, use_container_width=True)

    # create a bar graph showing last 5 game trends
    last_5_games = last_games.tail(5)
    mean_dict = {i: last_5_games[i].mean() for i in last_5_games.columns[7:26]}
    del mean_dict['FG_PCT']
    del mean_dict['FG3_PCT']
    del mean_dict['FT_PCT']
    sns.set_theme(style="whitegrid")
    sns.set(rc={'figure.figsize':(11.7,8.27)})
    sns.set(font_scale=1.5)
    ax = sns.barplot(x=list(mean_dict.keys()), y=list(mean_dict.values()))
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
    ax.set_title(f'{player_name} Last 5 Games')
    st.pyplot(ax.figure)

    # create a scatter plot for going against rival team
    opposing_team = go.Figure()
    for stat in selected_stats:
        opposing_team.add_trace(go.Scatter(x=last_games['GAME_DATE'], y=last_games[stat], mode='lines+markers', name=stat))
    opposing_team.update_layout(title=f'{player_name} Stats vs {rival_team}', xaxis_title='Date', yaxis_title='Stats')
    st.plotly_chart(opposing_team)


    # shot chart
    title = player["full_name"] + " 2023 Shot Chart " 
    player_shotchart_df, league_avg = get_player_shotchartdetail(player["full_name"], "2023-24")
    chart = shot_chart(player_shotchart_df, title=title)
    st.pyplot(chart.figure)

   