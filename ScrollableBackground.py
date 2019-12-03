from PPlay.gameimage import *
import math
# Classe base do jogador
class ScrollableBackground():
    #Region Fields
    #End Region
    #Region Constructors
    def __init__(self, game, path, velocity):
        self.game           = game
        self.janela         = game.janela
        self.game_image     = GameImage(path)
        self.copy           = GameImage(path)
        self.game.game_images.append(self.game_image)
        self.game.game_images.append(self.copy)
        self.velocity       = velocity
        self.copy.set_position(0, -self.game_image.height)
        return
    #End Region
    #Region Methods
    def update(self):
        y_gi = self.game_image.y + self.velocity * self.janela.delta_time()
        self.game_image.set_position(0, y_gi)
        self.copy.set_position(0, self.game_image.y - self.game_image.height)
        if self.game_image.y >= self.janela.height:
            self.game_image.set_position(0, 0)
            self.copy.set_position(0, -self.game_image.height)
        return
    #End Region