from manim import SVGMobject, VGroup

from manim.mobject.geometry import Rectangle
from manim.mobject.svg.text_mobject import Text

from manim.constants import DOWN, RIGHT

from manim.utils.color import YELLOW

from numpy import ndarray

class Twitter(VGroup):
    _logo_item_ : SVGMobject = None
    _logo_width_ : ndarray = None
    _logo_height_ : ndarray = None

    _border_item_ : Rectangle = None

    _logo_color_ : str = "#1D98F0"

    def __init__(self, color:str = "BLUE", twthandle: str = False, to_corner = DOWN + RIGHT, scale: float = 0.6, remove_logo: bool = False):
        logo_path = "./animation/assets/SVGs/Twitter.svg"
        color_choice = {
            "BLUE": "#1D9BF0",
            "WHITE": "#FFFFFF",
            "BLACK": "#000000"
        }
        self._logo_color_ = color_choice[color] if color in color_choice else color_choice["BLUE"]

        self._logo_item_ = SVGMobject(file_name=logo_path, color=self._logo_color_)
        self._logo_item_.scale_to_fit_height(scale)
        super().__init__(self._logo_item_)

        self._logo_height_ = self[0].get_height()
        self._logo_width_ = self[0].get_width()
        
        self._border_item_ = self.logo_border()
        self.add(self._border_item_)

        if twthandle:
            self.with_handle(twthandle=twthandle)

        if to_corner.any():
            self.to_corner(to_corner)
        
        if remove_logo:
            self.remove(self._logo_item_)
        

    def logo_border(self):
        """
        Twitter has specified that at least 150% of the logo width should be empty. I apply the same for the height
        """
        border = Rectangle(width=self._logo_width_*1.5, height=self._logo_height_*1.5, stroke_opacity=0)
        border.move_to(self._logo_item_.get_center())
        return border

    def with_handle(self, twthandle: str ="Thaza_Kun"):
        at_twthandle: str = "@" + twthandle
        Handle = Text(at_twthandle, height=self._logo_height_, font="Helvetica Neue")
        Handle.next_to(self, RIGHT, buff=0)
        super().add(Handle)
        return self