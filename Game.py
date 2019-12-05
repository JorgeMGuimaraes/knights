#Region Preprocessor
import  DisplayUtils    as      dsman
from    GS_Menu         import  *
from    GameStates      import  *
from    GS_GameRunning  import  *
from    GS_Dificuldades import  *
#End Region
class Game():
    #Region Fields
    is_playing      = True
    janela          = dsman.iniciarJanela()
    game_states     = dict()
    difficulty      = Dificuldades.Normal
    #End Region
    #Region Constructors
    def __init__(self):
        self.current_state = None
        self.change_state(GameStates.Menu)
        return
    #End Region
    #Region Methods
    def run(self):
        print("Entrando no jogo")
        while self.is_playing:
            self.current_state.process_inputs()
            self.current_state.update()
            self.current_state.render()
        return
    
    def change_state(self, new_state):
        print("Debug: Mudar state para %s"%str(new_state))
        if self.current_state is not None:          self.current_state.on_state_exit()
        if new_state == GameStates.Menu:            self.current_state = GS_Menu(self)
        if new_state == GameStates.Running:         self.current_state = GS_GameRunning(self)
        if new_state == GameStates.Dificuldades:    self.current_state = GS_Dificuldades(self)
        self.current_state.on_state_enter()
        return
    
    def change_difficulty(self, difficulty):
        self.difficulty = difficulty
        return
    #End Region