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
        self.x_space            = 70
        self.y_space            = 70
        self.top_bar            = 150
        self.linhas             = 6
        self.colunas            = 12
        self.largura_tabuleiro  = self.colunas * self.x_space
        self.tabuleiro          = []
        self.inimigos           = []
        self.primeiro_tile      = None
        self.segundo_tile       = None
        self.primeiro_tile_     = None
        self.segundo_tile_      = None
        return
    
    def on_state_enter(self):
        self.current_state      = Running_Start(self.game, self)
        return
    
    def on_state_exit(self):
        return

    def process_inputs(self):
        if self.teclado.key_pressed("ESC"): self.game.change_state(GameStates.Menu)
        return

    def update(self):
        self.current_state.do()
        for coluna in self.tabuleiro:
            for tile in coluna:
                tile.update()
        return

    def render(self):
        dsman.drawStack(self.game_images)
        self.janela.update()
        return
    #End Region

class Running_Start():
    """
    Subestado inicial do estado Running. Inicia o tabuleiro, inimigos e outros elementos do jogo
    """
    def __init__(self, game, running):
        self.game       = game
        self.running    = running
        self.set_images()
        self.create_matrix()
        self.create_enemies_list()
        return

    def do(self):
        self.running.current_state = Running_No_Select(self.game, self.running)
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
        #caminho = "Assets/images/"
        #extensao = ".png"
        #sel = "_selecionado"
        pecas_disponiveis   = ["escudo", "espada", "espada_dupla", "machadinha", "flecha", "adaga", "punhais"]
        x_start, y_start    = 10, self.running.top_bar
        x, y                = x_start, y_start
        anterior_esq        = [None] * self.running.linhas
        anterior_acima      = None

        for i in range(self.running.colunas):
            coluna  = []
            for j in range(self.running.linhas):
                #possiveis_escolhas = list(pecas_disponiveis.values())
                possiveis_escolhas = pecas_disponiveis.copy()
                if possiveis_escolhas.count(anterior_esq[j]) > 0: possiveis_escolhas.remove(anterior_esq[j])
                if possiveis_escolhas.count(anterior_acima) > 0 : possiveis_escolhas.remove(anterior_acima)
            
                e_type          = random.choice(possiveis_escolhas)
                #tile            = Tile(self.game, x, y, caminho + e_type + extensao, caminho + e_type + sel + extensao)
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

class Running_No_Select():
    def __init__(self, game, running):
        self.game       = game
        self.running    = running
        self.timer      = 0
        self.min_time   = 0.5
        self.mouse      = self.game.janela.get_mouse()
        return

    def do(self):
        self.primeiro_click()
        return

    def primeiro_click(self):
        """
        Define se o primeiro click eh valido, e seleciona uma peca
        """
        self.timer += self.game.janela.delta_time()
        clicked         = self.mouse.is_button_pressed(1)
        if self.timer >= self.min_time and clicked:
            mouse_x, mouse_y    = self.mouse.get_position()
            if mouse_x > self.running.largura_tabuleiro or mouse_y < self.running.top_bar: return
            self.selecionar(mouse_x, mouse_y)
            self.running.current_state = Running_Select_2(self.game, self.running)
        return

    def selecionar(self, col, lin):
        self.running.primeiro_tile_ = [col // self.running.x_space, (lin - self.running.top_bar ) // self.running.y_space]
        self.running.tabuleiro[self.running.primeiro_tile_[0]][self.running.primeiro_tile_[1]].tint_in()
        return

class Running_Select_2():

    def __init__(self, game, running):
        self.game       = game
        self.running    = running
        self.timer      = 0
        self.min_time   = 0.5
        self.mouse      = self.game.janela.get_mouse()
        return

    def do(self):
        self.segundo_click()
        return

    def segundo_click(self):
        """
        Define se o segundo click eh valido, e seleciona uma peca e/ou deseleciona a anterior
        """
        self.timer      += self.game.janela.delta_time()
        clicked         = self.mouse.is_button_pressed(1)
        if self.timer >= self.min_time and clicked:
            self.timer                  = 0
            mouse_x, mouse_y            = self.mouse.get_position()
            if mouse_x > self.running.largura_tabuleiro or mouse_y < self.running.top_bar:
                self.deselecionar()
                self.running.current_state = Running_No_Select(self.game, self.running)
                return
            self.running.segundo_tile_  = [mouse_x // self.running.x_space, (mouse_y - self.running.top_bar ) // self.running.y_space]
            if self.running.primeiro_tile_ == self.running.segundo_tile_:
                self.deselecionar()
                self.running.current_state = Running_No_Select(self.game, self.running)
                return
            vizinhos                    = self.lista_de_vizinhos(self.running.primeiro_tile_)
            for v in vizinhos:
                if self.running.segundo_tile_ == v:
                    self.swap()
                    return
            self.selecionar()
        return

    def selecionar(self):
        self.running.tabuleiro[self.running.primeiro_tile_[0]][self.running.primeiro_tile_[1]].tint_out()
        self.running.primeiro_tile_ = self.running.segundo_tile_
        self.running.segundo_tile_  = None
        self.running.tabuleiro[self.running.primeiro_tile_[0]][self.running.primeiro_tile_[1]].tint_in()
        return

    def deselecionar(self):
        self.running.tabuleiro[self.running.primeiro_tile_[0]][self.running.primeiro_tile_[1]].tint_out()
        self.running.primeiro_tile_  = None
        self.running.segundo_tile_   = None
        return

    def lista_de_vizinhos(self, atual):
        posicoes = [[0,1],[1,0],[0,-1], [-1,0]]
        vizinhos = []
        for i in range(len(posicoes)):
            if (0 <= atual[0] + posicoes[i][0] < self.running.colunas) and (0 <= atual[1] + posicoes[i][1] <  self.running.linhas):
                vizinhos.append([atual[0] + posicoes[i][0], atual[1] + posicoes[i][1]])
        #print(atual)
        #print(vizinhos)
        return vizinhos

    def swap(self):
        tmp_tipo1                   = self.running.tabuleiro[self.running.primeiro_tile_[0]][self.running.primeiro_tile_[1]].tipo
        d1, d2                      = self.direcao()
        self.running.tabuleiro[self.running.primeiro_tile_[0]][self.running.primeiro_tile_[1]].current_state.swap(self.running.tabuleiro[self.running.segundo_tile_[0]][self.running.segundo_tile_[1]].tipo, d1)
        self.running.tabuleiro[self.running.segundo_tile_[0]][self.running.segundo_tile_[1]].current_state.swap(tmp_tipo1, d2)
        self.running.current_state  = Running_Match(self.game, self.running)
        return

    def direcao(self):
        if self.running.primeiro_tile_[0] == self.running.segundo_tile_[0]: return ('c', 'b') if self.running.primeiro_tile_[1] > self.running.segundo_tile_[1] else ('b', 'c')
        else:                                                               return ('d', 'e') if self.running.primeiro_tile_[0] > self.running.segundo_tile_[0] else ('e', 'd')

class Running_Match():

    def __init__(self, game, running):
        self.game       = game
        self.running    = running
        self.timer      = 0
        self.min_time   = 0.5
        self.match      = False
        return

    def do(self):
        for col in range(self.running.colunas):
            for lin in range(self.running.linhas):
                self.limpar_todos([col, lin])
        if self.match:
            self.match                  = False
            self.atacar_inimigo()
            self.running.current_state  = Running_Refill(self.game, self.running)
            return
        self.swap_back()
        self.running.current_state  = Running_No_Select(self.game, self.running)
        return

    def limpar_todos(self, elemento):
        horizontal                  = [[0, -1], [0, 1]]
        vertical                    = [[-1, 0], [1, 0]]
        limpar                      = []
        limpar.extend(self.marcar(elemento, horizontal))
        limpar.extend(self.marcar(elemento, vertical))
        if self.match:
            for tile in limpar:
                self.running.tabuleiro[tile[0]][tile[1]].tipo = "None"
                self.running.tabuleiro[tile[0]][tile[1]].tint_out()
            return
        return
            
    def marcar(self, elemento, direcoes):
        matches = []
        for i in range(len(direcoes)): matches.extend(self.encontrar_semelhantes(elemento, direcoes[i]))
        if len(matches) > 1:
            self.match = True
            matches.append(elemento)
            return matches
        return []

    def encontrar_semelhantes(self, elemento, direcao):
        lista_semelhantes   = []
        tipo                = self.running.tabuleiro[elemento[0]][elemento[1]].tipo
        proximo             = [elemento[0] + direcao[0], elemento[1] + direcao[1]]
        while  (0 <= proximo[0] < self.running.colunas) and (0 <= proximo[1] <  self.running.linhas):
            if self.running.tabuleiro[proximo[0]][proximo[1]].tipo == tipo:
                #print("Semelhante: %d,%d"%(proximo[0], proximo[1]))
                lista_semelhantes.append(proximo)
                proximo = [proximo[0] + direcao[0], proximo[1] + direcao[1]]
            else: return lista_semelhantes
        return lista_semelhantes

    def swap_back(self):
        if self.running.primeiro_tile_ == None or self.running.segundo_tile_ == None: return
        tmp_tipo1                   = self.running.tabuleiro[self.running.primeiro_tile_[0]][self.running.primeiro_tile_[1]].tipo
        d1, d2                      = 'e', 'd'
        self.running.tabuleiro[self.running.primeiro_tile_[0]][self.running.primeiro_tile_[1]].current_state.swap(self.running.tabuleiro[self.running.segundo_tile_[0]][self.running.segundo_tile_[1]].tipo, d1)
        self.running.tabuleiro[self.running.segundo_tile_[0]][self.running.segundo_tile_[1]].current_state.swap(tmp_tipo1, d2)
        self.running.current_state  = Running_No_Select(self.game, self.running)
        return

    def atacar_inimigo(self):
        l = len(self.running.inimigos)
        if l > 0:
            e = self.running.inimigos.pop(l - 1)
            self.running.game_images.remove(e.game_image)
        else: print("Fim de fase")
        return

class Running_Refill():
    def __init__(self, game, running):
        self.game       = game
        self.running    = running
        self.timer      = 0
        self.min_time   = 0.1
        self.running.primeiro_tile_ = None
        self.running.segundo_tile_ = None
        #print("Entra Refill")
        return

    def do(self):
        self.timer += self.game.janela.delta_time()
        if self.timer >= self.min_time:
            self.timer = 0
            self.escanear_colunas()
        return

    def escanear_colunas(self):
        #print("Escaneando")
        for coluna in self.running.tabuleiro:
            for i in range(len(coluna)):
                if coluna[i].tipo == "None":
                    if i == 0:
                        coluna[i].tipo  = self.novo_sprite()
                        coluna[i].tint_out()
                        return
                    coluna[i].tipo      = coluna[i - 1].tipo
                    coluna[i - 1].tipo  = "None"
                    coluna[i].tint_out()
                    coluna[i - 1].tint_out()
                    return
        self.running.current_state = Running_Match(self.game, self.running)

    def novo_sprite(self):
        import random
        random.seed()
        pecas_disponiveis   = ["escudo", "espada", "espada_dupla", "machadinha", "flecha", "adaga", "punhais"]
        tipo = random.choice(pecas_disponiveis)
        return tipo