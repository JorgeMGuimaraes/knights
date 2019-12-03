#Region Preprocessor
import  DisplayUtils     as dsman
#End Region
class GameStateBehavior:
    #Region Fields
    janela      = None
    game_images = []
    #End Region
    #Region Constructors
    def __init__(self, janela):
        self.janela = janela
        return
    #End Region
    #Region Methods
    def on_state_enter(self):
        return
    
    def on_state_exit(self):
        return

    def process_inputs(self):
        return

    def update(self):
        return

    def render(self):
        dsman.render(self.janela)
        return
    
    #End Region