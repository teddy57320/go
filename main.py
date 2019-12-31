import yaml
from src.board import Board
from src.game import GameUI

def main(config):
    game = GameUI(config)
    game.play()

if __name__ == '__main__':

    config = None
    with open('config.yaml', 'r') as f:
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f'Error: {e}')

    if config is not None:
        main(config)
