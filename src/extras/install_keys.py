import argparse
import keyring
from keyrings.alt.file import PlaintextKeyring


def parse_args():
    """Parse argument values from command-line"""

    parser = argparse.ArgumentParser(description='Arguments requiridos para o script.')
    parser.add_argument('--subject', default='user_db', choices=['user_db', 'pass_db', 'sid_db'])
    parser.add_argument('--secret', default='')
    
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    
    keyring.set_keyring(PlaintextKeyring())
    keyring.set_password('aoe2_project', args.subject, args.secret)

main()