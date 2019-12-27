import yaml
from src.board import Board
from src.game import Game

def main(config):
    print(config)

if __name__ == '__main__':

    config = None
    with open('config.yaml', 'r') as f:
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print(f'Error: ')

    if config is not None:
        main(config)
