#Region Preprocessor
#from GameStateBehavior import GameStateBehavior
import  DisplayUtils            as      dsman
from    enum                    import  Enum
from    PPlay.gameimage         import  *
from    PPlay.keyboard          import  *
from    PPlay.mouse             import  *
from    GameStates              import  *
from    Tile                    import  *
#End Region

class GS_GameRunning():
    game_images             = []

    def __init__(self, game_mngr):
        self.game_mngr          = game_mngr
        self.janela             = self.game_mngr.janela
        self.mouse              = self.janela.get_mouse()
        self.teclado            = self.janela.get_keyboard()
        self.set_images()
        self.x_space            = 70
        self.y_space            = 70
        self.top_bar            = 150
        self.linhas             = 6
        self.colunas            = 12
        self.largura_tabuleiro  = self.colunas * self.x_space
        self.create_matrix()
        self.create_enemies_list()
        self.min_time   = 0.5

        return
    
    def on_state_enter(self):
        self.timer              = 0
        self.is_primeiro_click  = False
        return
    
    def on_state_exit(self):
        return

    def process_inputs(self):
        if self.teclado.key_pressed("ESC"): self.game_mngr.change_state(GameStates.Menu)
        return

    def update(self):
        #self.pegar_posicao_primeiro_click()
        #self.pegar_posicao_segundo_click()
        self.change_on_mouse_click()
        return

    def render(self):
        dsman.drawStack(self.game_images)
        for line in self.matrix_parent: dsman.drawStack(line)
        dsman.drawStack(self.enemies_parent)

        self.janela.update()
        return

    def set_images(self):
        bg      = GameImage("Assets/images/bg.png")
        energia = GameImage("Assets/images/energia.png")
        energia.set_position(900,150)
        placar  = GameImage("Assets/images/placar.png")
        placar.set_position(self.janela.width - placar.width, 50)
        self.game_images.append(bg)
        self.game_images.append(energia)
        self.game_images.append(placar)


        self.tile = Tile(self.game_mngr, self.janela.width - 100, 0, "Assets/images/escudo.png")
        self.game_images.append(self.tile.game_image)
        return

    def create_matrix(self):
        
        import random
        random.seed()
        pieces              = dict()
        pieces["escudo"]    = "Assets/images/escudo.png"
        pieces["espada"]    = "Assets/images/espada.png"
        pieces["supla"]     = "Assets/images/espada_dupla.png"
        pieces["machado"]   = "Assets/images/machadinha.png"
        start_x             = 10
        x, y                = start_x, self.top_bar
        self.matrix_parent  = []
        for i in range(self.linhas):
            line    = []
            for j in range(self.colunas):                
                e_type  = random.choice(list(pieces.keys()))
                p       = GameImage(pieces[e_type])
                p.set_position(x, y)
                line.append(p)
                x       += self.x_space
            self.matrix_parent.append(line)
            x       = start_x
            y       += self.y_space
        return

    def create_enemies_list(self):
        
        import random
        random.seed()
        enemies      = dict()
        enemies["1_verde"]  = "Assets/images/Inimigo_1_verde.png"
        enemies["1_verm"]   = "Assets/images/Inimigo_1_verm.png"
        enemies["2"]        = "Assets/images/Inimigo_2.png"
        enemies["3"]        = "Assets/images/Inimigo_3.png"
        start_x             = 10
        x, y                = start_x, 25
        self.enemies_parent = []
        for j in range(12):                
            e_type  = random.choice(list(enemies.keys()))
            e       = GameImage(enemies[e_type])
            e.set_position(x, y)
            self.enemies_parent.append(e)
            x       += self.x_space
        return

    def pegar_posicao_primeiro_click(self):
        if not self.is_primeiro_click:                    
            self.timer  += self.janela.delta_time()
            clicked     = self.mouse.is_button_pressed(1)            
            if self.timer >= self.min_time and clicked:
                self.is_primeiro_click      = True
                self.pos_x1, self.pos_y1    = self.get_x_y()
                self.timer                  = 0

        return
    def pegar_posicao_segundo_click(self):
        self.timer      += self.janela.delta_time()
        clicked         = self.mouse.is_button_pressed(1)
        if self.timer >= self.min_time and clicked and self.is_primeiro_click:
            self.is_primeiro_click      = False
            self.pos_x2, self.pos_y2    = self.get_x_y()
            if abs(self.pos_x2 - self.pos_x1) == 1 or abs(self.pos_y2 - self.pos_y1) == 1:
                self.trocar_posicao()                
            self.timer  = 0
        return
    
    def change_on_mouse_click(self):
        self.timer      += self.janela.delta_time()
        clicked         = self.mouse.is_button_pressed(1)
        if self.timer >= self.min_time and clicked:
            if not self.is_primeiro_click:
                self.pos_x1, self.pos_y1    = self.get_x_y()
                self.is_primeiro_click      = True
            else:
                self.pos_x2, self.pos_y2    = self.get_x_y()
                if (abs(self.pos_x2 - self.pos_x1) == 1 and self.pos_y1 == self.pos_y2) or \
                    (abs(self.pos_y2 - self.pos_y1) == 1 and self.pos_x1 == self.pos_x2) :
                    self.trocar_posicao()
                    self.is_primeiro_click = False
            self.timer = 0
        return

    def get_x_y(self):
        """
        Retorna indices (tupla x, y) de coluna e linha da matriz de pecas, numeros fora de alcance para as comparacoes serem validas
        """
        mouse_x, mouse_y    = self.mouse.get_position()
        if mouse_x > self.largura_tabuleiro or mouse_y < self.top_bar:
            self.is_primeiro_click = False
            return 1000, 1000
        return mouse_x // self.x_space, (mouse_y - self.top_bar ) // self.y_space

    def trocar_posicao(self):
        temp1 = self.matrix_parent[self.pos_y1][self.pos_x1].image_ref
        temp2 = self.matrix_parent[self.pos_y2][self.pos_x2].image_ref
        self.matrix_parent[self.pos_y1][self.pos_x1].set_image(temp2)
        self.matrix_parent[self.pos_y2][self.pos_x2].set_image(temp1)
        return
        #End Region