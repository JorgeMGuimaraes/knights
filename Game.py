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
    current_state   = None
    difficulty      = Dificuldades.Normal
    #End Region
    #Region Constructors
    def __init__(self):
        self.game_states[GameStates.Menu]           = GS_Menu(self)
        self.game_states[GameStates.Running]        = GS_GameRunning(self)
        self.game_states[GameStates.Dificuldades]   = GS_Dificuldades(self)
        self.change_state(GameStates.Menu)
        return
    #End Region
    #Region Methods
    def run(self):
        print("Entrando no jogo")
        while self.is_playing:
            self.game_states[self.current_state].process_inputs()
            self.game_states[self.current_state].update()
            self.game_states[self.current_state].render()
        return
    
    def change_state(self, new_state):
        print("Debug: Mudar state para %s"%str(new_state))
        if self.current_state is not None: self.game_states[self.current_state].on_state_exit()
        self.current_state = new_state
        self.game_states[self.current_state].on_state_enter()
        return
    
    def change_difficulty(self, difficulty):
        self.difficulty = difficulty
        return
    #End Region