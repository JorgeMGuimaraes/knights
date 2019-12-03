#Region Preprocessor
import  DisplayUtils    as      dsman
from    enum            import  Enum
from    PPlay.gameimage import  *
from    PPlay.keyboard  import  *
from    PPlay.mouse     import  *
from    GameStates      import  *

#End Region
class Button():
    #Region Fields
    #image       = None
    #hover       = None
    #game_image  = None
    #x           = 0
    #y           = 0
    is_hover    = False
    #End Region
    #Region Constructors
    def __init__(self, image, hover, x, y, state):
        self.image      = image
        self.hover      = hover
        self.game_image = GameImage(self.image)
        self.game_image.set_position(x - (self.game_image.width * 0.5), y - (self.game_image.height * 0.5))
        self.x_min      = self.game_image.x
        self.x_max      = self.game_image.x + self.game_image.width
        self.y_min      = self.game_image.y
        self.y_max      = self.game_image.y + self.game_image.height
        self.state      = state
        return
    #End Region
    #Region Methods
    def toggle_image(self):
        if self.is_hover    : self.game_image.set_image(self.hover)
        else                : self.game_image.set_image(self.image)
        return
    def on_mouse_over(self, mouse_pos):
        tmp_mouse_over = (self.x_min <=  mouse_pos[0] <= self.x_max) and (self.y_min <=  mouse_pos[1] <= self.y_max)
        if tmp_mouse_over == self.is_hover: return
        else:
            self.is_hover = tmp_mouse_over
            self.toggle_image()
        return

    def on_mouse_click(self, mouse_clicked):
        if self.is_hover and mouse_clicked: return self.state
        #print("click")
        return None
    #End Region