import argparse
import cx_Oracle
from sqlalchemy import create_engine
import pandas as pd
import keyring

from package.aoe2 import get_games, get_labels


def parse_args():
    """Parse argument values from command-line"""

    parser = argparse.ArgumentParser(description='Arguments requiridos para o script.')
    parser.add_argument('--matches-count', default=7, type=int, help='Quantidade de partidas para extração')
    parser.add_argument('--string-tables', default='N', choices=['N', 'Y'], help='[OPCIONAL] Extração das tabelas de string')
    
    args = parser.parse_args()
    return args


def get_oracle_engine():
    user_db = keyring.get_password('aoe2_project', 'user_db')
    pass_db = keyring.get_password('aoe2_project', 'pass_db')
    sid_db = keyring.get_password('aoe2_project', 'sid_db')
    return create_engine(f'oracle://{user_db}:{pass_db}@{sid_db}')


def load_string_tables():
    subjects = ['civ', 'map_size', 'map_type', 'leaderboard', 'rating_type']
    for subject in subjects:
        df = get_labels(subject=subject, language='en')
        df.to_sql(f'stg_aoe2_{subject}', get_oracle_engine(), if_exists='replace', index=False)


def load_matches_table(game_count=1000):
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

    df = pd.concat([get_games(player_id=player.get('player_id'), num_games=game_count) for player in players], ignore_index=True)
    df.drop_duplicates(inplace = True)
    all_columns = list(df)
    df[all_columns] = df[all_columns].astype(str)
    df[:0].to_sql('stg_aoe2_matches', get_oracle_engine(), if_exists='replace', index=False, chunksize=100)
    print(f'Rows -> {df.count()}')
    print('Writing data to database...')
    user_db = keyring.get_password('aoe2_project', 'user_db')
    pass_db = keyring.get_password('aoe2_project', 'pass_db')
    sid_db = keyring.get_password('aoe2_project', 'sid_db')
    with cx_Oracle.connect(user_db, pass_db, sid_db) as conn:
        cursor = conn.cursor()
        cursor.executemany('''
        INSERT INTO ADMIN.STG_AOE2_MATCHES
        (PROFILE_ID, STEAM_ID, NAME, CLAN, COUNTRY, SLOT, SLOT_TYPE, RATING, RATING_CHANGE, GAMES, WINS, STREAK, DROPS, COLOR, TEAM, CIV, WON, MATCH_ID, OPENED, STARTED, FINISHED, MAP_TYPE, RANKED, MAP_SIZE, LEADERBOARD_ID, RATING_TYPE, ABERTURA, INICIO, FIM)
        VALUES(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14, :15, :16, :17, :18, :19, :20, :21, :22, :23, :24, :25, :26, :27, :28, :29)
        ''', df.to_records(index=False).tolist())
        conn.commit()


def main():
    args = parse_args()
    print(f'Argumentos')
    print(f'matches-count -> {args.matches_count}')
    print(f'string-tables -> {args.string_tables}')

    if args.string_tables == 'Y':
        load_string_tables()
    
    load_matches_table(args.matches_count)


if __name__ == '__main__':
    main()

