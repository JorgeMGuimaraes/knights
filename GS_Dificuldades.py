#Region Preprocessor
#from GameStateBehavior import GameStateBehavior
import  DisplayUtils    as      dsman
from    enum            import  Enum
from    PPlay.gameimage import  *
from    PPlay.keyboard  import  *
from    PPlay.mouse     import  *
from    GameStates      import  *
from    Button          import  *
from    Dificuldades    import  *
#End Region
class GS_Dificuldades():
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
        #self.set_menu_images()
        #self.set_menu_buttons()
        self.timer = 0.0
        return
    
    def on_state_exit(self):
        #self.buttons.clear()
        return

    def process_inputs(self):
        #if self.teclado.key_pressed("ESC"): self.game_mngr.is_playing = False
        return

    def update(self):
        self.timer  += self.janela.delta_time()
        clicked     = self.mouse.is_button_pressed(1)
        for btn in self.buttons.values():
            btn.on_mouse_over(self.mouse.get_position())
            if self.timer >= self.min_time:
                dificuldade = btn.on_mouse_click(clicked)
                if dificuldade is not None:
                    self.timer = 0
                    if dificuldade == Dificuldades.Back:
                        self.game_mngr.change_state(GameStates.Menu)
                        print("Debug: Back")
                        return
                    else:
                        self.game_mngr.change_difficulty(dificuldade)
                        self.game_mngr.change_state(GameStates.Menu)
                        print("Debug: Dificuldade %s selecionada"%str(dificuldade))
        return

    def render(self):
        dsman.drawStack(self.game_images)
        self.janela.update()
        return
    
    def set_menu_images(self):
        bg     = GameImage("Assets/images/bg.png")
        logo   = GameImage("Assets/logo.png")
        logo.x = (self.janela.width / 2) - (logo. width / 2)
        logo.y = 25.0
        self.game_images.append(bg)
        self.game_images.append(logo)
        return 
    
    def set_menu_buttons(self):
        x_tela                              = self.janela.width * 0.5
        y_tela                              = self.janela.height * 0.5
        dist_btn                            = 70
        self.buttons[Dificuldades.Easy]     = Button("Assets/images/btn_dificuldades_easy.png", "Assets/images/btn_dificuldades_easy_hover.png", x_tela, y_tela, Dificuldades.Easy)
        y_tela                              += dist_btn
        self.buttons[Dificuldades.Normal]   = Button("Assets/images/btn_dificuldades_normal.png", "Assets/images/btn_dificuldades_normal_hover.png", x_tela, y_tela, Dificuldades.Normal)
        y_tela                              += dist_btn
        self.buttons[Dificuldades.Hard]     = Button("Assets/images/btn_dificuldades_hard.png", "Assets/images/btn_dificuldades_hard_hover.png", x_tela, y_tela, Dificuldades.Hard)
        y_tela                              += dist_btn
        self.buttons[Dificuldades.Hell]     = Button("Assets/images/btn_dificuldades_hell.png", "Assets/images/btn_dificuldades_hell_hover.png", x_tela, y_tela, Dificuldades.Hell)
        y_tela                              += dist_btn
        self.buttons[Dificuldades.Back]     = Button("Assets/images/btn_dificuldades_back.png", "Assets/images/btn_dificuldades_back_hover.png", x_tela, y_tela, Dificuldades.Back)
        y_tela                              += dist_btn

        self.game_images.append(self.buttons[Dificuldades.Easy].game_image)
        self.game_images.append(self.buttons[Dificuldades.Normal].game_image)
        self.game_images.append(self.buttons[Dificuldades.Hard].game_image)
        self.game_images.append(self.buttons[Dificuldades.Hell].game_image)        
        self.game_images.append(self.buttons[Dificuldades.Back].game_image)        
        return
    #End Region