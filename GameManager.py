class GameManager():
    #Region Fields
    max_placar  = 5
    pontos_1    = 0
    pontos_2    = 0
    #End Region
    #Region Constructors
    def __init__(self, max_placar):
        if max_placar != 0: self.max_placar = max_placar
        return
    #End Region
    #Region Methods
    def controlar_placar(self, pontuacao):
        if pontuacao == 0   : return
        if pontuacao == 1   : self.pontos_1 += 1
        else                : self.pontos_2 += 1
        if self.pontos_1 >= self.max_placar:
            self.game_over()
            return
        if self.pontos_2 >= self.max_placar:
            self.game_over()
            return
        return
    
    def game_over(self):
        return self.pontos_1 == self.max_placar or self.pontos_2 == self.max_placar
    #End Region
