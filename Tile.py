from PPlay.gameimage import *

class Tile:
    """
    Classe dos blocos do jogo
    """
    
    def __init__(self, game, x, y, tipo):
        self.game           = game
        self.current_state  = Tile_Idle(game, self)
        self.tipo           = tipo
        self.caminho        = "Assets/images/"
        self.extensao       = ".png"
        self.sel            = "_selecionado"
        self.game_image     = GameImage(self.caminho + tipo + self.extensao)
        self.game_image.set_position(x, y)
        return

    def update(self):
        self.current_state.do()
        return
    
    def tint_out(self):
        self.game_image.set_image(self.caminho + self.tipo + self.extensao)
        return
    def tint_in(self):
        self.game_image.set_image(self.caminho + self.tipo + self.sel + self.extensao)
        return

class Tile_Idle:
    """
    Estado do tile onde este esta parado
    """

    def __init__(self, game, tile):
        self.game = game
        self.tile = tile

    def do(self):
        return

    def swap(self, novo_tipo, nova_posicao):
        """Troca as imagens do tiles"""
        self.tile.tipo  = novo_tipo
        self.tile.tint_out()
        #self.tile.current_state = Tile_Moving(self.game, self.tile, nova_posicao)
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

    def do(self):
        self.mover()
        return

    def mover(self):
        #print("!")
        if self.dir == 'c':
            self.tile.game_image.y - 1 * self.game.janela.delta_time()
            if self.tile.game_image.y <= self.y_inicial:
                self.tile.game_image.y = self.y_inicial
                self.tile.current_state = Tile_Idle(self.game, self.tile)
            return
        elif self.dir == 'b':
            self.tile.game_image.y + 1 * self.game.janela.delta_time()
            if self.tile.game_image.y >= self.y_inicial:
                self.tile.game_image.y = self.y_inicial
                self.tile.current_state = Tile_Idle(self.game, self.tile)
            return
        elif self.dir == 'e':
            self.tile.game_image.x - 1 * self.game.janela.delta_time()
            if self.tile.game_image.x <= self.x_inicial:
                self.tile.game_image.x = self.x_inicial
                self.tile.current_state = Tile_Idle(self.game, self.tile)
            return
        elif self.dir == 'd':
            self.tile.game_image.x + 1 * self.game.janela.delta_time()
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