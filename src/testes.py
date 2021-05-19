import cx_Oracle
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

with cx_Oracle.connect(user_db, pass_db, sid_db) as conn:
    cursor = conn.cursor()
    cursor.executemany()
    conn.commit()