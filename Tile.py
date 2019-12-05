from PPlay.gameimage import *

class Tile:
    """
    Classe dos blocos do jogo
    """
    
    def __init__(self, game, x, y, path, path_selecionado):
        self.game           = game
        self.current_state  = Tile_Idle(game, self)
        self.path = path
        self.selecionado = path_selecionado
        self.game_image     = GameImage(self.path)
        self.game_image.set_position(x, y)
        return

    def update(self):
        current_state.do()
        return
    
    def tint_out(self):
        self.game_image.set_image(self.path)
        return
    def tint_in(self):
        self.game_image.set_image(self.selecionado)
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

    