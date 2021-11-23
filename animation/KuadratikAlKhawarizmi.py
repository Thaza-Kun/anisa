"""
Author  : Murthadza bin Aznam
Date    : 2021-11-16
Manim   : v0.12.0
"""

from manim import *
from numpy import ndarray
from typing import Dict
from assets import Twitter

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

class PersGeometri(MathTex):
    def __init__(self, eq_num: int, move_to: ndarray = ORIGIN):
        if eq_num == 1:
            equation = [r"(x + \frac{1}{2}b)^2", "=", r"c + \frac{1}{2}b^2"]
        elif eq_num == 2:
            equation = [""]
        elif eq_num == 3:
            equation = [""]
        else:
            equation = [""]

        super().__init__(*equation)
        if eq_num == 1:
            equation_ = {
                "sqr_x": VGroup(self[0][0], self[0][7:]),
                "x": self[0][1],
                "sign_x_plus_b": self[0][2],
                "half_b_free": self[0][3:6],
                "b": self[0][6],
                "=": self[1],
                "c": self[2][0],
                "sign_c_plus_halfb": self[2][1],
                "half_b_sqr": self[2][2:]
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
        equation_["half_b_sqr"].set_color(COLHALFB)
        self.equation_ = equation_
        self.move_to(move_to)

    def get_parts(self):
        return self.equation_

    def get_pivot_point(self):
        return self.equation_["="].get_center()

    def pivot_to(self, pivot_point: ndarray):
        self.move_to(pivot_point - self.get_pivot_point())

    def pivot_with_shift(self, pivot_point: ndarray = ORIGIN, shift: ndarray = DOWN):
        self.pivot_to(pivot_point)
        self.shift(shift)

class PersAkhir(MathTex):
    def __init__(self, eq_num: int, move_to: ndarray = ORIGIN):
        if eq_num == 1:
            equation = [r"x", "=", r"-\frac{1}{2}b", "+", r"\sqrt{c + \frac{1}{2}b^2}"]
        elif eq_num == 2:
            equation = [""]
        elif eq_num == 3:
            equation = [""]
        else:
            equation = [""]

        super().__init__(*equation)
        if eq_num == 1:
            equation_ = {
                "x": self[0],
                "=": self[1],
                "sign_b": self[2][0],
                "half_b_free": self[2][1:4],
                "b": self[2][4],
                "sign_b_plus_c": self[3],
                "sqrt": self[4][0:2],
                "c": self[4][2],
                "sign_c_plus_halfb": self[4][3],
                "half_b_sqr": self[4][4:],
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
        equation_["half_b_sqr"].set_color(COLHALFB)
        self.equation_ = equation_
        self.move_to(move_to)

    def get_parts(self):
        return self.equation_

    def get_pivot_point(self):
        return self.equation_["="].get_center()

    def pivot_to(self, pivot_point: ndarray):
        self.move_to(pivot_point - self.get_pivot_point())

    def pivot_with_shift(self, pivot_point: ndarray = ORIGIN, shift: ndarray = DOWN):
        self.pivot_to(pivot_point)
        self.shift(shift)


# Animation Classes
# =================
class PenyelesaianKhawarizmiPertama(Scene):
    def construct(self):
        # TODO Add name at the bottom of the screen
        Title = self.add_title()
        pers_awal = self.fade_in_equation()
        KhawaSqrGroup = self.eq_to_geometry(pers_awal, XSquare(VALX, move_to=DOWN*2+LEFT*2.5), BXRect(VALX, VALB, move_to=DOWN*2))
        self.reposition_items(pers_awal, KhawaSqrGroup, Title)
        self.divide_b_rect(KhawaSqrGroup)
        self.solve_geometry(KhawaSqrGroup)
        self.complete_the_square(KhawaSqrGroup)
        pers_geometri = self.geometry_to_eq(KhawaSqrGroup, PersGeometri(1, move_to=RIGHT*2.5 + UP*0.5))
        pers_jawapan = self.solve_final_eq(pers_geometri)
        self.finalize_scene(pers_awal, pers_geometri, pers_jawapan, geometri=KhawaSqrGroup)
        self.wait(3)

    def add_title(self):
        title = TitleGroup("Kaedah Pertama")
        self.add(title)
        twitter = Twitter.Twitter(remove_logo=True, twthandle="Thaza_Kun", scale=0.4)
        self.add(twitter)
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

    def divide_b_rect(self, KhawaSqrGroup: VGroup):
        BRectGroup = KhawaSqrGroup[1]

        position = BRectGroup.get_center()
        BRectLGroup = HalfBRect(VALX, VALB, move_to=position + LEFT*(1/4)*VALB.get_value())
        BRectRGroup = HalfBRect(VALX, VALB, move_to=position + RIGHT*(1/4)*VALB.get_value())

        halfb_textL = MathTex(r"\frac{1}{2}","b").scale(0.7)
        halfb_textL[1].set_color(COLB)
        halfb_textR = halfb_textL.copy()

        halfb_textL.next_to(BRectLGroup, DOWN)
        halfb_textR.next_to(BRectRGroup, DOWN)

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

        self.play(LaggedStart(
            FadeIn(labelgroup := VGroup(halfb_textL, halfb_textR)),
            Create(dividerDash, run_time=1.5),
            ))
        self.play(Create(dividerLine), FadeOut(labelgroup))
        self.remove(dividerDash, dividerLine)

        KhawaSqrGroup.remove(BRectGroup)
        self.add(BRectRGroup, BRectLGroup)
        self.remove(BRectGroup)
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

        label_x_U = MathTex("x").scale(0.7)
        label_x_U.set_color(COLX)

        BUFFX: float = 0.3
        label_x_U.next_to(KhawaSqrGroup[0], UP, buff=BUFFX)
        label_x_L = label_x_U.copy().next_to(KhawaSqrGroup[0], LEFT, buff=BUFFX)

        label_halfb_U = MathTex(r"\frac{1}{2}","b").scale(0.5)
        label_halfb_U[1].set_color(COLB)
        label_halfb_L = label_halfb_U.copy()

        BUFF_HALFB: float = 0.15
        label_halfb_U.next_to(KhawaSqrGroup[1], UP, buff=BUFF_HALFB)
        label_halfb_L.next_to(KhawaSqrGroup[2], LEFT, buff=BUFF_HALFB+0.1)

        self.play(FadeIn(labelGroup:= VGroup(label_x_U, label_halfb_U, label_x_L, label_halfb_L)))
        self.play(Create(hglt:=highlight(KhawaSqrGroup)))
        KhawaSqrGroup.add(half_b_sqr)
        KhawaSqrGroup.add(labelGroup)
        self.play(Create(half_b_sqr))
        self.play(FadeOut(hglt))
        return half_b_sqr

    def geometry_to_eq(self, KhawaSqrGroup: VGroup, equation: PersGeometri):
        def highlight(Object: Mobject, color=COLSQR, gap: float = 0.2, stroke_proportion: int = 0.5) -> Mobject:
            mobject = Rectangle(
                height=Object.height + gap,
                width=Object.width + gap,
                color=color,
                stroke_width = stroke_proportion*STROKE_WIDTH
            ).move_to(Object.get_center())
            return mobject
        self.play(KhawaSqrGroup.animate.shift(LEFT*2.5))

        b_Down = KhawaSqrGroup[2]
        b_Right = KhawaSqrGroup[1]
        b_side_R = b_Down[4].copy().shift(0.5*VALB.get_value()*RIGHT)
        b_side_D = b_Right[4].copy().shift(0.5*VALB.get_value()*DOWN)

        equation_ = equation.get_parts()

        self.add(b_side_D, b_side_R)
        self.play(
            Transform(b_Down[1].copy(), equation_["x"]), 
            Transform(b_side_D, VGroup(equation_["b"], equation_["half_b_free"])), 
            GrowFromCenter(equation_["sign_x_plus_b"])
        )
        self.play(
            Transform(b_Right[2].copy(), equation_["sqr_x"][0]), 
            Transform(b_side_R, equation_["sqr_x"][1]),
        )

        self.play(
            Transform(KhawaSqrGroup[0:3].copy(), equation_["c"], replace_mobject_with_target_in_scene=True),
            Transform(KhawaSqrGroup[3].copy(), equation_["half_b_sqr"], replace_mobject_with_target_in_scene=True),
            GrowFromCenter(equation_["sign_c_plus_halfb"]))

        hglt = highlight(KhawaSqrGroup[:3], gap=0, stroke_proportion=1)
        self.play(Create(hglt))
        self.play(Transform(hglt, highlight(equation[0])))
        self.play(Transform(hglt, highlight(equation[2:])))
        self.play(FadeOut(hglt), GrowFromCenter(equation_["="]))
        return equation

    def solve_final_eq(self, original_eq: MathTex):
        awal = original_eq.copy()
        akhir = PersAkhir(eq_num=1)

        self.add(awal)
        self.play(awal.animate.shift(DOWN*2))

        akhir.pivot_to(awal.get_pivot_point())
        awal_ = awal.get_parts()
        akhir_ = akhir.get_parts()

        self.play(
            Transform(
                VGroup(awal_["c"], awal_["sign_c_plus_halfb"], awal_["half_b_sqr"]), 
                VGroup(akhir_["c"], akhir_["sign_c_plus_halfb"], akhir_["half_b_sqr"]),
                replace_mobject_with_target_in_scene=True),
            Transform(
                awal_["sqr_x"],
                akhir_["sqrt"],
                replace_mobject_with_target_in_scene=True
                )
            )
        self.play(
            Transform(
                VGroup(awal_["b"], awal_["half_b_free"]),
                VGroup(akhir_["b"], akhir_["half_b_free"]),
                replace_mobject_with_target_in_scene=True
                ),
            FadeIn(akhir_["sign_b"], akhir_["sign_b_plus_c"]),
            FadeOut(awal_["sign_x_plus_b"]),
            Transform(
                awal_["x"],
                akhir_["x"],
                replace_mobject_with_target_in_scene=True
            ),
            Transform(
                awal_["="],
                akhir_["="],
                replace_mobject_with_target_in_scene=True
            )
        )

        self.play(akhir.animate.shift(LEFT*2))
        return akhir

    def finalize_scene(self, pers_awal, pers_geometri, pers_jawapan, geometri):
        pass