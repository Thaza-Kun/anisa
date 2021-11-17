"""
Author  : Murthadza bin Aznam
Date    : 2021-11-16
"""

from manim import *
from numpy import ndarray
from typing import List, Dict

# Global Values
# =============

VALX = ValueTracker(1)
VALB = ValueTracker(1.5)

COLX = BLUE
COLB = YELLOW
COLC = GREEN

COLSQR = RED
COLHALFB = ORANGE

COLC_OPACITY = 0.6

STROKE_WIDTH = DEFAULT_STROKE_WIDTH*2

dGAP = 0.037

# Object Classes
# ==============

class XSquare(Square):
    def __init__(self, VALX: ValueTracker, move_to: ndarray = ORIGIN, update_size: bool = True):
        super().__init__(
            side_length=VALX.get_value(),
            color= COLC,
            stroke_width = STROKE_WIDTH,
            stroke_color = COLX,
            fill_opacity = 0
        )
        self.move_to(move_to)
        if update_size:
            self.update_size(VALX)

    def update_size(self, VALX: ValueTracker):
        self.add_updater(lambda sqr: sqr.stretch_to_fit_height(VALX.get_value()))
        self.add_updater(lambda sqr: sqr.stretch_to_fit_width(VALX.get_value()))
        return self

    def make_opague(self):
        self.set_opacity(COLC_OPACITY)
        return self

class BXRect(VGroup):
    def __init__(self, VALX: ValueTracker, VALB: ValueTracker, move_to: ndarray = ORIGIN, width_proportion: float = 1, update_size: bool = True, show_color: bool =False):
        self.width_proportion = width_proportion
        if show_color:
            opacity = COLC_OPACITY
        else:
            opacity = 0
        self.main_rect = Rectangle(
            height          = VALX.get_value(),
            width           = self.width_proportion*VALB.get_value(),
            color           = COLC,
            stroke_width    = STROKE_WIDTH,
            stroke_color    = COLB,
            fill_opacity    = opacity
        )
        super().__init__(self.main_rect)
        self.add(*[self.color_vert_side(side) for side in (LEFT, RIGHT)])
        self.add(*[self.color_hori_side(side) for side in (UP, DOWN)])
        self.move_to(move_to)
        if update_size:
            self.update_size()

    def color_vert_side(self, side: ndarray):
        GAP = [0, dGAP, 0]
        vert = always_redraw(lambda:
            Line(
                    start   = self.main_rect.get_corner(side + UP) + GAP,
                    end     = self.main_rect.get_corner(side + DOWN) - GAP,
                    color   = COLX,
                    stroke_width = STROKE_WIDTH
                )
        )
        return vert

    def color_hori_side(self, side: ndarray):
        GAP = [dGAP, 0, 0]
        hori = always_redraw(lambda:
            Line(
                    start   = self.main_rect.get_corner(LEFT + side) - GAP,
                    end     = self.main_rect.get_corner(RIGHT + side) + GAP,
                    color   = COLB,
                    stroke_width = STROKE_WIDTH
            )
        )
        return hori
    
    def update_size(self):
        self.main_rect.add_updater(lambda rect: rect.stretch_to_fit_height(VALX.get_value()))
        self.main_rect.add_updater(lambda rect: rect.stretch_to_fit_width(self.width_proportion*VALB.get_value()))
        return self

class HalfBRect(BXRect):
    def __init__(self, VALX: ValueTracker, VALB: ValueTracker, move_to: ndarray = ORIGIN,width_ratio: float = 0.5):
        super().__init__(VALX, VALB, move_to=move_to, width_proportion=width_ratio, show_color=True)

class CRect(Rectangle):
    def __init__(self, VALX: ValueTracker, VALB: ValueTracker, move_to: ndarray = ORIGIN, update_size: bool = True):
        super().__init__(
            height          = VALX.get_value(),
            width           = VALX.get_value() + VALB.get_value(),
            color           = COLC,
            fill_opacity    = COLC_OPACITY,
            stroke_width    = 0
        )
        self.move_to(move_to)
        if update_size:
            self.update_size(VALX, VALB)

    def update_size(self, VALX: ValueTracker, VALB: ValueTracker):
        self.add_updater(lambda rect: rect.stretch_to_fit_height(VALX.get_value()))
        self.add_updater(lambda rect: rect.stretch_to_fit_width(VALX.get_value() + VALB.get_value()))
        return self

class HalfBSquare(Square):
    def __init__(self, VALB: ValueTracker, move_to: ndarray = ORIGIN, update_size: bool = True):
        super().__init__(
            side_length     = 0.5*VALB.get_value(),
            color           = COLHALFB,
            stroke_width    = STROKE_WIDTH,
            stroke_color    = COLB,
            fill_opacity    = 1
        )
        self.move_to(move_to)
        if update_size:
            self.update_size(VALB)

    def update_size(self, VALB: ValueTracker):
        self.add_updater(lambda sqr: sqr.stretch_to_fit_height(0.5*VALB.get_value()))
        self.add_updater(lambda sqr: sqr.stretch_to_fit_width(0.5*VALB.get_value()))
        return self

class TitleGroup(VGroup):
    def __init__(self, subtitle: str):
        self.title(subtitle)
        super().__init__(self.TITLE, self.SUBTITLE)
        self.scale(0.5)

    def title(self, subtitle: str):
        self.TITLE = Text("Penyempurnaan Kuasa Dua Al-Khawarizmi").to_edge(UP)
        self.SUBTITLE = Text(subtitle).next_to(self.TITLE, DOWN)
        return self

class PersAwal(MathTex):
    equations: Dict[int, Dict[str, int]] = {
        1: {"X": 0, "B":2, "C":4},
        2: {"X": 0, "B":4, "C":2},
        3: {"X": 0, "B":2, "C":4}
    }
    def __init__(self, eq_num: int):
        if eq_num == 1:
            equation = [r"x^2", "+", "bx",  "=", "c"]
        elif eq_num == 2:
            equation = [r"x^2", "+", "c", "=" ,"bx"]
        elif eq_num == 3:
            equation = [r"x^2", "=", "bx",  "+", "c"]
        else:
            equation = [""]
        idx = self.equations[eq_num]
        super().__init__(*equation)
        self.scale(2)
        self[idx["X"]].set_color(COLX)
        self[idx["B"]][0].set_color(COLB)
        self[idx["B"]][1].set_color(COLX)
        self[idx["C"]].set_color(COLC)

class PersAkhir(MathTex):
    def __init__(self, eq_num: int, move_to: ndarray = ORIGIN):
        if eq_num == 1:
            equation = [r"(x + b)^2", "=", r"c + \frac{1}{2}b"]
            equation_ = {
                "x": equation[0][1],
                "b": equation[0][3],
                "c": equation[2][0],
                "halfb": equation[2][2:]
            }
        elif eq_num == 2:
            equation = [""]
        elif eq_num == 3:
            equation = [""]
        else:
            equation = [""]

        super().__init__(*equation)
        if eq_num == 1:
            equation_ = {
                "x": self[0][1],
                "b": self[0][3],
                "c": self[2][0],
                "halfb": self[2][2:]
            }
        elif eq_num == 2:
            equation = [""]
        elif eq_num == 3:
            equation = [""]
        else:
            equation = [""]
        equation_["x"].set_color(COLX)
        equation_["b"].set_color(COLB)
        equation_["c"].set_color(COLC)
        equation_["halfb"].set_color(COLHALFB)
        self.equation_ = equation_
        self.move_to(move_to)

    def get_parts(self):
        return self.equation_


# Animation Classes
# =================
class PenyelesaianKhawarizmiPertama(Scene):
    def construct(self):
        Title = self.add_title()
        persAwal = self.fade_in_equation()
        KhawaSqrGroup = self.eq_to_geometry(persAwal, XSquare(VALX, move_to=DOWN*2+LEFT*2.5), BXRect(VALX, VALB, move_to=DOWN*2))
        self.reposition_items(persAwal, KhawaSqrGroup, Title)
        self.divide_b_rect(KhawaSqrGroup[1])
        self.reveal_halved_b_rects(KhawaSqrGroup)
        self.solve_geometry(KhawaSqrGroup)
        self.complete_the_square(KhawaSqrGroup)
        self.geometry_to_eq(KhawaSqrGroup, PersAkhir(1, move_to=RIGHT*3 + UP*0.5))
        self.solve_final_eq()
        self.wait(3)

    def add_title(self):
        title = TitleGroup("Kaedah Pertama")
        self.add(title)
        return title

    def fade_in_equation(self):
        equation = PersAwal(1)
        self.play(FadeIn(equation))
        return equation

    def eq_to_geometry(self, equation, x_sqr, BRectGroup):
        self.play(Transform(equation[0].copy(), x_sqr, replace_mobject_with_target_in_scene=True))
        self.play(Transform(equation[2][0].copy(), BRectGroup - BRectGroup[3:], replace_mobject_with_target_in_scene=True),
            Transform(equation[2][1].copy(), BRectGroup[3:], replace_mobject_with_target_in_scene=True))
        self.play(x_sqr.animate.move_to(DOWN*2 + LEFT*0.625 + LEFT*0.1435), BRectGroup.animate.move_to(DOWN*2 + RIGHT*0.625 + LEFT*0.1435))
        
        self.play(Transform(equation[4].copy(), c:= CRect(VALX, VALB, move_to=DOWN*2), replace_mobject_with_target_in_scene=True))
        x_sqr.set_opacity(COLC_OPACITY)
        BRectGroup[0].set_opacity(COLC_OPACITY)
        self.remove(c)
        KhawaSqrGroup = VGroup(x_sqr, BRectGroup)
        return KhawaSqrGroup

    def reposition_items(self, equation: MathTex, KhawaSqrGroup: VGroup, Title: VGroup):
        x_square, BRectGroup = KhawaSqrGroup
        x_square.add_updater(lambda sqr: sqr.next_to(BRectGroup, LEFT, buff=0))
        self.play(equation.animate.scale(0.5),
                VALX.animate.set_value(2),
                VALB.animate.set_value(2.5),
                BRectGroup[0].animate.move_to(DOWN*2 + RIGHT*2*0.625 + LEFT*2*0.1435)
                )
        *others , follow_rect = x_square.get_updaters() 
        x_square.remove_updater(follow_rect)
        self.play(equation.animate.next_to(Title, DOWN),
                KhawaSqrGroup.animate.move_to(ORIGIN + DOWN))

    def divide_b_rect(self, BRectGroup):
        dividerDash = DashedLine(
                    start=BRectGroup[3].get_midpoint() + dGAP*UP,
                    end=BRectGroup[4].get_midpoint() + dGAP*DOWN,
                    color=COLX,
                    stroke_width=STROKE_WIDTH,
                    dash_length=DEFAULT_DASH_LENGTH*2.5
                    )
        dividerLine = Line(
                    start=BRectGroup[3].get_midpoint() + dGAP*UP,
                    end=BRectGroup[4].get_midpoint() + dGAP*DOWN,
                    color=COLX,
                    stroke_width=STROKE_WIDTH
                    )
        self.play(Create(dividerDash))
        self.play(Create(dividerLine))
        self.remove(dividerDash, dividerLine)

    def reveal_halved_b_rects(self, KhawaSqrGroup: VGroup):
        position = KhawaSqrGroup[1].get_center()
        BRectLGroup = HalfBRect(VALX, VALB, move_to=position + LEFT*(1/4)*VALB.get_value())
        BRectRGroup = HalfBRect(VALX, VALB, move_to=position + RIGHT*(1/4)*VALB.get_value())
        KhawaSqrGroup.remove(rect:=KhawaSqrGroup[1])
        self.add(BRectRGroup, BRectLGroup)
        self.remove(rect)
        KhawaSqrGroup.add(BRectLGroup, BRectRGroup)

    def solve_geometry(self, KhawaSqrGroup: VGroup):
        main_geometry = KhawaSqrGroup[:-1]
        free_geometry = KhawaSqrGroup[-1]
        self.play(free_geometry.animate.shift(DOWN), main_geometry.animate.shift(UP))
        free_geometry.clear_updaters()
        self.play(Rotate(free_geometry, 0.5*PI))
        self.play(free_geometry.animate.next_to(main_geometry[0], DOWN, buff=0))
        self.play(KhawaSqrGroup.animate.move_to(ORIGIN + DOWN))

    def complete_the_square(self, KhawaSqrGroup: VGroup):
        def highlight(Object: Mobject, color=COLSQR, gap: float = 0, stroke_proportion: int = 1) -> Mobject:
            mobject = Rectangle(
                height=Object.height + gap,
                width=Object.width + gap,
                color=color,
                stroke_width = stroke_proportion*STROKE_WIDTH
            ).move_to(Object.get_center())
            return mobject
        half_b_sqr = HalfBSquare(VALB)
        half_b_sqr.next_to(KhawaSqrGroup[2], RIGHT, buff=0)
        KhawaSqrGroup.add(half_b_sqr)
        self.play(Create(hglt:=highlight(KhawaSqrGroup)), Create(half_b_sqr))
        self.play(FadeOut(hglt))
        return half_b_sqr

    def geometry_to_eq(self, KhawaSqrGroup: VGroup, equation: PersAkhir):
        def highlight(Object: Mobject, color=COLSQR, gap: float = 0.2, stroke_proportion: int = 0.5) -> Mobject:
            mobject = Rectangle(
                height=Object.height + gap,
                width=Object.width + gap,
                color=color,
                stroke_width = stroke_proportion*STROKE_WIDTH
            ).move_to(Object.get_center())
            return mobject
        self.play(KhawaSqrGroup.animate.shift(LEFT*2.3))

        b_Down = KhawaSqrGroup[2]
        b_Right = KhawaSqrGroup[1]
        b_side_R = b_Down[4].copy().shift(0.5*VALB.get_value()*RIGHT)
        b_side_D = b_Right[4].copy().shift(0.5*VALB.get_value()*DOWN)

        equation_ = equation.get_parts()

        self.add(b_side_D, b_side_R)
        self.play(
            Transform(b_Down[1].copy(), equation_["x"]), 
            Transform(b_side_D, equation_["b"]), 
            GrowFromCenter(equation[0][2])
        )
        self.play(
            Transform(b_Right[2].copy(), equation[0][0]), 
            Transform(b_side_R, equation[0][4:]),
        )

        self.play(Transform(KhawaSqrGroup[0:3].copy(), equation_["c"], replace_mobject_with_target_in_scene=True))
        self.play(Transform(KhawaSqrGroup[3].copy(), equation_["halfb"], replace_mobject_with_target_in_scene=True))
        self.play(GrowFromCenter(equation[2][1]))

        hglt = highlight(KhawaSqrGroup, gap=0, stroke_proportion=1)
        self.play(Create(hglt))
        self.play(Transform(hglt, highlight(equation[0])))
        self.play(Transform(hglt, highlight(equation[2:])))
        self.play(FadeOut(hglt), GrowFromCenter(equation[1]))

    def solve_final_eq():
        pass