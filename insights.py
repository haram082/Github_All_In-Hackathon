
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.endpoints import playerestimatedmetrics
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
player_dict = players.get_players()

def get_2024_gamelog(player_id):
    gamelog = playergamelog.PlayerGameLog(player_id=player_id, season = 2023)
    df = gamelog.get_data_frames()[0]
    df['GAME_DATE'] = pd.to_datetime(df['GAME_DATE'])
    df.sort_values(by=['GAME_DATE'], inplace=True, ascending=True)
    df.reset_index(drop=True, inplace=True)
    df['HOME_AWAY'] = df['MATCHUP'].apply(lambda x: 'AWAY' if "@" in x else 'HOME')
    return df




def games_against(rival_team, player_id):
    last_6_seasons = ['2018-19', '2019-20', '2020-21', '2021-22', '2022-23', '2023-24']
    game_logs = []
    for season in last_6_seasons:
        game_log = playergamelog.PlayerGameLog(player_id=player_id, season=season)
        game_logs.append(game_log.get_data_frames()[0])

    # Concatenate all game logs into a single DataFrame
    df_last_6_seasons = pd.concat(game_logs, ignore_index=True)
    df_last_6_seasons['TEAM_AGAINST'] = df_last_6_seasons['MATCHUP'].str.extract(r'([A-Z]{3})$')
    return df_last_6_seasons[df_last_6_seasons['TEAM_AGAINST'] == rival_team]


