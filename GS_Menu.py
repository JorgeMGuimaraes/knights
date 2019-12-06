#Region Preprocessor
#from GameStateBehavior import GameStateBehavior
import  DisplayUtils    as      dsman
from    enum            import  Enum
from    PPlay.gameimage import  *
from    PPlay.keyboard  import  *
from    PPlay.mouse     import  *
from    GameStates      import  *
from    Button          import  *
from PPlay.sound    import *
#End Region

class SubMenus(Enum):
    NewGame         = 1
    MainMenu        = 2
    Dificuldades    = 4
    Rankings        = 8
    Exit            = 512

class GS_Menu():
    #Region Fields
    game_images = []
    buttons     = dict()
    #End Region
    #Region Constructors
    def __init__(self, game_mngr):
        self.game_mngr  = game_mngr
        self.janela     = self.game_mngr.janela
        self.mouse      = self.janela.get_mouse()
        self.teclado    = self.janela.get_keyboard()
        self.min_time   = 0.5

        self.set_menu_images()
        self.set_menu_buttons()
        return
    #End Region
    #Region Methods
    def on_state_enter(self):
        self.timer = 0
        return
    
    def on_state_exit(self):
        return

    def process_inputs(self):
        return

    def update(self):
        self.timer  += self.janela.delta_time()
        clicked     = self.mouse.is_button_pressed(1)
        for btn in self.buttons.values():
            btn.on_mouse_over(self.mouse.get_position())
            if self.timer >= self.min_time:
                tmp_state = btn.on_mouse_click(clicked)
                if tmp_state is not None:
                    self.game_mngr.change_state(tmp_state)
        return

    def render(self):
        dsman.drawStack(self.game_images)
        self.janela.update()
        return
    
    def set_menu_images(self):
        bg     = GameImage("Assets/images/menu_bg.png")
        self.game_images.append(bg)
        return 
    
    def set_menu_buttons(self):
        x_tela                              = self.janela.width * 0.5
        y_tela                              = self.janela.height * 0.5
        dist_btn                            = 70
        self.buttons[SubMenus.NewGame]      = Button("Assets/images/Btn_01.png", "Assets/images/Btn_hover_01.png", x_tela, y_tela, GameStates.Running)
        #y_tela                              += dist_btn
        #self.buttons[SubMenus.Dificuldades] = Button("Assets/images/Btn_03.png", "Assets/images/Btn_hover_03.png", x_tela, y_tela, GameStates.Dificuldades)
        #y_tela                              += dist_btn
        #self.buttons[SubMenus.Rankings]     = Button("Assets/images/Btn_05.png", "Assets/images/Btn_hover_05.png", x_tela, y_tela, GameStates.Ranking)
        y_tela                              += dist_btn
        self.buttons[SubMenus.Exit]         = Button("Assets/images/Btn_07.png", "Assets/images/Btn_hover_07.png", x_tela, y_tela, GameStates.Exit)
        self.game_images.append(self.buttons[SubMenus.NewGame].game_image)
        #self.game_images.append(self.buttons[SubMenus.Dificuldades].game_image)
        #self.game_images.append(self.buttons[SubMenus.Rankings].game_image)
        self.game_images.append(self.buttons[SubMenus.Exit].game_image)        
        return
    #End Region