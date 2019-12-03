from PPlay.gameimage import *

class Tile:
    """
    Classe dos blocos do jogo
    """
    
    def __init__(self, game, x, y, path):
        self.game           = game
        self.current_state  = Tile_Idle(game, self)
        self.game_image     = GameImage(path)
        self.game_image.set_position(x, y)
        return

    def update(self):
        current_state.do()
        return

class Tile_Idle:
    """
    Estado do tile onde este esta parado
    """

    def __init__(self, game, tile):
        self.game = game
        self.tile = tile

    def do():
        return