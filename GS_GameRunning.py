#Region Preprocessor
#from GameStateBehavior import GameStateBehavior
import  DisplayUtils            as      dsman
from    enum                    import  Enum
from    PPlay.gameimage         import  *
from    PPlay.keyboard          import  *
from    PPlay.mouse             import  *
from    GameStates              import  *
from    Tile                    import  *
from    Enemy                   import  *
#End Region

class GS_GameRunning():
    

    def __init__(self, game_mngr):
        """
        Estado do jogo enquando a partida acontece
        """
        self.game               = game_mngr
        self.janela             = self.game.janela
        self.mouse              = self.janela.get_mouse()
        self.teclado            = self.janela.get_keyboard()
        self.game_images        = []
        #self.set_images()
        self.x_space            = 70
        self.y_space            = 70
        self.top_bar            = 150
        self.linhas             = 6
        self.colunas            = 12
        self.largura_tabuleiro  = self.colunas * self.x_space
        self.tabuleiro          = []
        self.inimigos           = []
        self.min_time           = 0.5
        self.current_state      = Running_Start(self.game, self)
        return
    
    def on_state_enter(self):
        self.timer              = 0
        self.is_primeiro_click  = False
        return
    
    def on_state_exit(self):
        return

    def process_inputs(self):
        if self.teclado.key_pressed("ESC"): self.game.change_state(GameStates.Menu)
        return

    def update(self):
        self.change_on_mouse_click()
        return

    def render(self):
        dsman.drawStack(self.game_images)
        #for line in self.matrix_parent: dsman.drawStack(line)
        #dsman.drawStack(self.enemies_parent)

        self.janela.update()
        return

    #def set_images(self):
    #    bg      = GameImage("Assets/images/bg.png")
    #    energia = GameImage("Assets/images/energia.png")
    #    energia.set_position(900,150)
    #    placar  = GameImage("Assets/images/placar.png")
    #    placar.set_position(self.janela.width - placar.width, 50)
    #    self.game_images.append(bg)
    #    self.game_images.append(energia)
    #    self.game_images.append(placar)
    #    return

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

class Running_Start():

    def __init__(self, game, running):
        """
        Subestado inicial do estado Running. Inicia o tabuleiro e confere se esta tudo ok
        """
        self.game       = game
        self.running    = running
        self.set_images()
        self.create_matrix()
        self.create_enemies_list()
        return

    def do(self):
        return
    
    def set_images(self):
        bg      = GameImage("Assets/images/bg.png")
        energia = GameImage("Assets/images/energia.png")
        energia.set_position(900,150)
        placar  = GameImage("Assets/images/placar.png")
        placar.set_position(self.game.janela.width - placar.width, 50)
        self.running.game_images.append(bg)
        self.running.game_images.append(energia)
        self.running.game_images.append(placar)
        return

    def create_matrix(self):
        """
        Cria a matriz de pecas do tabuleiro
        """
        import random
        random.seed()
        #TODO: ver se eh possivel remover dicionario e ser somente lista
        pecas_disponiveis   = {"escudo":"Assets/images/escudo.png", "espada":"Assets/images/espada.png", "dupla":"Assets/images/espada_dupla.png", "machado":"Assets/images/machadinha.png"}
        x_start, y_start    = 10, self.running.top_bar
        x, y                = x_start, y_start
        anterior_esq        = [None] * self.running.linhas
        anterior_acima      = None

        for i in range(self.running.colunas):
            coluna  = []
            for j in range(self.running.linhas):
                possiveis_escolhas = list(pecas_disponiveis.values())
                if possiveis_escolhas.count(anterior_esq[j]) > 0: possiveis_escolhas.remove(anterior_esq[j])
                if possiveis_escolhas.count(anterior_acima) > 0: possiveis_escolhas.remove(anterior_acima)
            
                e_type          = random.choice(possiveis_escolhas)
                tile            = Tile(self.game, x, y, e_type)
                coluna.append(tile)
                self.running.game_images.append(tile.game_image)
                y               += self.running.y_space
                anterior_esq[j] = e_type
                anterior_acima  = e_type
            self.running.tabuleiro.append(coluna)
            x       += self.running.x_space
            y       = y_start
        return

    def create_enemies_list(self):
        """
        Cria lista de inimigos e os posiciona na tela
        """
        import random
        random.seed()
        enemies             = ["Assets/images/Inimigo_1_verde.png", "Assets/images/Inimigo_1_verm.png", "Assets/images/Inimigo_2.png", "Assets/images/Inimigo_3.png"]
        start_x, start_y    = 10, 25
        x, y                = start_x, start_y
        for j in range(self.running.colunas):                
            e_type  = random.choice(enemies)
            enemy   = Enemy(self.game, x, y, e_type)
            self.running.inimigos.append(enemy)
            self.running.game_images.append(enemy.game_image)
            x       += self.running.x_space
        return
