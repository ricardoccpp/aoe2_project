import cx_Oracle
from sqlalchemy import create_engine
import pandas as pd

from package.aoe2 import get_games, get_labels

players = [{
              'player_id': '76561197988887364',
              'player_name': 'OvelhaDolly'
            },
            {
              'player_id': '76561198116915612',
              'player_name': 'Birigui'
            },
            {
              'player_id': '76561198027946698',
              'player_name': 'caiotakeshi'
            },
            {
              'player_id': '76561198135873187',
              'player_name': 'MarKoLa'
            }]

game_count = 1000

user_db = 'ADMIN'
pass_db = 'Oraclerootdb123'
sid_db = 'dw_high'

engine = create_engine(f'oracle://{user_db}:{pass_db}@{sid_db}')

df = pd.concat([get_games(player_id=player.get('player_id'), num_games=game_count) for player in players], ignore_index=True)
df.drop_duplicates(inplace = True)
all_columns = list(df)
df[all_columns] = df[all_columns].astype(str)
df[:0].to_sql('stg_aoe2_matches', engine, if_exists='replace', index=False, chunksize=100)
print(f'Rows -> {df.count()}')
print('Writing data to database...')
with cx_Oracle.connect(user_db, pass_db, sid_db) as conn:
    cursor = conn.cursor()
    cursor.executemany('''
          INSERT INTO ADMIN.STG_AOE2_MATCHES
          (PROFILE_ID, STEAM_ID, NAME, CLAN, COUNTRY, SLOT, SLOT_TYPE, RATING, RATING_CHANGE, GAMES, WINS, STREAK, DROPS, COLOR, TEAM, CIV, WON, MATCH_ID, OPENED, STARTED, FINISHED, MAP_TYPE, RANKED, MAP_SIZE, LEADERBOARD_ID, RATING_TYPE, ABERTURA, INICIO, FIM)
          VALUES(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14, :15, :16, :17, :18, :19, :20, :21, :22, :23, :24, :25, :26, :27, :28, :29)
          ''', df.to_records(index=False).tolist())
    conn.commit()

subjects = ['civ', 'map_size', 'map_type', 'leaderboard', 'rating_type']
for subject in subjects:
    df = get_labels(subject=subject, language='en')
    df.to_sql(f'stg_aoe2_{subject}', engine, if_exists='replace', index=False)

