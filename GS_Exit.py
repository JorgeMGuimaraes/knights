#Region Preprocessor
#from GameStateBehavior import GameStateBehavior
import  DisplayUtils    as      dsman
from    enum            import  Enum
from    PPlay.gameimage import  *
from    PPlay.keyboard  import  *
from    PPlay.mouse     import  *
from    GameStates      import  *
#End Region

class GS_Exit():

    def __init__(self, game_mngr):
        self.game_mngr  = game_mngr
        self.janela     = self.game_mngr.janela
        self.mouse      = self.janela.get_mouse()
        self.teclado    = self.janela.get_keyboard()
        return

    def on_state_enter(self):
        self.janela.close()
        return
    
    def on_state_exit(self):
        return

    def process_inputs(self):
        return

    def update(self):
        self.janela.close()
        exit()
