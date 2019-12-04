from PPlay.gameimage import *

class Enemy:
    """
    Inimigo exibido no top da tela, que serve como pontuacao
    """
    
    def __init__(self, game, x, y, path):
        self.game           = game
        self.current_state  = Enemy_Idle(game, self)
        self.game_image     = GameImage(path)
        self.game_image.set_position(x, y)
        return

    def update(self):
        current_state.do()
        return

class Enemy_Idle:
    """
    Estado do inimigo onde este esta parado
    """

    def __init__(self, game, enemy):
        self.game = game
        self.enemy = enemy

    def do():
        return