import json
import pandas as pd
import urllib.request as request
from datetime import datetime


def get_games(player_id=76561198116915612, num_games=100):
    print(f'Getting match data from {player_id}')
    url = f'https://aoe2.net/api/player/matches?game=aoe2de&steam_id={player_id}&count={num_games}'
    with request.urlopen(url) as response:
        data = json.loads(response.read())
    df = pd.json_normalize(data, 'players', ['match_id', 'opened', 'started', 'finished', 'map_type', 'ranked', 'map_size', 'leaderboard_id', 'rating_type'])
    df['abertura'] = df['opened'].apply(lambda x: datetime.fromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'))
    df['inicio'] = df['started'].apply(lambda x: datetime.fromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'))
    df['fim'] = df['finished'].apply(lambda x: datetime.fromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'))
    return df

def get_labels(subject='civ', language='en'):
    '''
        Subject options: age, civ, game_type, leaderboard, map_size, map_type, rating_type, resources, speed, victory, visibility
        Language options: en, de, el, es, es-MX, fr, hi, it, ja, ko, ms, nl, pt, ru, tr, vi, zh, zh-TW
    '''
    print(f'Getting label da from {subject} in {language}')
    url = f'https://aoe2.net/api/strings?game=aoe2de&language={language}'
    with request.urlopen(url) as response:
        data = json.loads(response.read())
    return pd.DataFrame(data.get(subject))