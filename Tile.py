from PPlay.gameimage import *

class Tile:
    """
    Classe dos blocos do jogo
    """
    
    def __init__(self, game, x, y, path, path_selecionado):
        self.game           = game
        self.current_state  = Tile_Idle(game, self)
        self.path           = path
        self.selecionado    = path_selecionado
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

    def swap(self, novo_path, novo_sel, nova_posicao):
        self.tile.path          = novo_path
        self.tile.selecionado   = novo_sel
        return

class Tile_Moving:
    """
    Estado do tile trocando de posicao (swap)
    """
    def __init__(self, game, tile, pos):
        self.game   = game
        self.tile   = tile
        self.dir    = pos
        self.x_inicial  =self.tile.game_image.x
        self.y_inicial  =self.tile.game_image.y
        self.nova_posicao()
        return

    def do():
        self.mover()
        return

    def mover(self):
        print("!")
        if self.dir == 'c':
            self.tile.game_image.y - 10 * self.game.janela.delta_time()
            if self.tile.game_image.y <= self.y_inicial:
                self.tile.game_image.y = self.y_inicial
                self.tile.current_state = Tile_Idle(self.game, self.tile)
            return
        elif self.dir == 'b':
            self.tile.game_image.y + 10 * self.game.janela.delta_time()
            if self.tile.game_image.y >= self.y_inicial:
                self.tile.game_image.y = self.y_inicial
                self.tile.current_state = Tile_Idle(self.game, self.tile)
            return
        elif self.dir == 'e':
            self.tile.game_image.x - 10 * self.game.janela.delta_time()
            if self.tile.game_image.x <= self.x_inicial:
                self.tile.game_image.x = self.x_inicial
                self.tile.current_state = Tile_Idle(self.game, self.tile)
            return
        elif self.dir == 'd':
            self.tile.game_image.x + 10 * self.game.janela.delta_time()
            if self.tile.game_image.x >= self.x_inicial:
                self.tile.game_image.x = self.x_inicial
                self.tile.current_state = Tile_Idle(self.game, self.tile)
            return

    def nova_posicao(self):
        if self.dir == 'c':
            self.tile.game_image.set_position(self.tile.game_image.x, self.tile.game_image.y + self.tile.game_image.height)
            return
        elif self.dir == 'b':
            self.tile.game_image.set_position(self.tile.game_image.x, self.tile.game_image.y - self.tile.game_image.height)
            return
        elif self.dir == 'e':
            self.tile.game_image.set_position(self.tile.game_image.x + self.tile.game_image.width, self.tile.game_image.y)
            return
        elif self.dir == 'd':
            self.tile.game_image.set_position(self.tile.game_image.x - self.tile.game_image.width, self.tile.game_image.y)
            return