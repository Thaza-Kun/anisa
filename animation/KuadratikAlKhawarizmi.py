"""
Author  : Murthadza bin Aznam
Date    : 2021-11-16 -> 2021-11-23
Manim   : v0.12.0
"""

from manim import *
from numpy import ndarray
from typing import Dict
from assets import Twitter

# Global Values
# =============
COL_X = BLUE
COL_B = YELLOW
COL_C = GREEN

COL_SQR = RED
COL_HALFB_SQR = ORANGE

COL_HALFB_MINUS_C = RED_E

COLC_OPACITY = 0.6

STROKE_WIDTH = DEFAULT_STROKE_WIDTH * 2

dGAP = 0.037

# Object Classes
# ==============


class XSquare(Square):
    def __init__(
        self, VALX: ValueTracker, move_to: ndarray = ORIGIN, update_size: bool = True
    ):
        super().__init__(
            side_length=VALX.get_value(),
            color=COL_C,
            stroke_width=STROKE_WIDTH,
            stroke_color=COL_X,
            fill_opacity=0,
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
    def __init__(
        self,
        VALX: ValueTracker,
        VALB: ValueTracker,
        move_to: ndarray = ORIGIN,
        width_proportion: float = 1,
        update_size: bool = True,
        show_color: bool = False,
        fill_color=COL_C,
        stroke_color=COL_B,
        hori_color=COL_B,
        vert_color=COL_X,
    ):
        self.width_proportion = width_proportion
        if show_color:
            opacity = COLC_OPACITY
        else:
            opacity = 0
        self.main_rect = Rectangle(
            height=VALX.get_value(),
            width=self.width_proportion * VALB.get_value(),
            color=fill_color,
            stroke_width=STROKE_WIDTH,
            stroke_color=stroke_color,
            fill_opacity=opacity,
        )
        super().__init__(self.main_rect)
        self.add(
            *[
                self.color_vert_side(side, fill_color=vert_color)
                for side in (LEFT, RIGHT)
            ]
        )
        self.add(
            *[self.color_hori_side(side, fill_color=hori_color) for side in (UP, DOWN)]
        )
        self.move_to(move_to)
        if update_size:
            self.update_size(VALX, VALB)

    def color_vert_side(self, side: ndarray, fill_color=COL_X):
        GAP = [0, dGAP, 0]
        vert = always_redraw(
            lambda: Line(
                start=self.main_rect.get_corner(side + UP) + GAP,
                end=self.main_rect.get_corner(side + DOWN) - GAP,
                color=fill_color,
                stroke_width=STROKE_WIDTH,
            )
        )
        return vert

    def color_hori_side(self, side: ndarray, fill_color=COL_B):
        GAP = [dGAP, 0, 0]
        hori = always_redraw(
            lambda: Line(
                start=self.main_rect.get_corner(LEFT + side) - GAP,
                end=self.main_rect.get_corner(RIGHT + side) + GAP,
                color=fill_color,
                stroke_width=STROKE_WIDTH,
            )
        )
        return hori

    def update_size(self, VALX: ValueTracker, VALB: ValueTracker):
        self.main_rect.add_updater(
            lambda rect: rect.stretch_to_fit_height(VALX.get_value())
        )
        self.main_rect.add_updater(
            lambda rect: rect.stretch_to_fit_width(
                self.width_proportion * VALB.get_value()
            )
        )
        return self


class HalfBRect(BXRect):
    def __init__(
        self,
        VALX: ValueTracker,
        VALB: ValueTracker,
        move_to: ndarray = ORIGIN,
        width_proportion: float = 0.5,
    ):
        super().__init__(
            VALX,
            VALB,
            move_to=move_to,
            width_proportion=width_proportion,
            show_color=True,
        )


class CRect(Rectangle):
    def __init__(
        self,
        VALX: ValueTracker,
        VALB: ValueTracker,
        move_to: ndarray = ORIGIN,
        update_size: bool = True,
        eq_num: int = 1,
    ):
        self.equation_number = eq_num
        xb_width = self.set_xb_width(VALX, VALB)
        super().__init__(
            height=VALX.get_value(),
            width=xb_width,
            color=COL_C,
            fill_opacity=COLC_OPACITY,
            stroke_width=0,
        )
        self.move_to(move_to)
        if update_size:
            self.update_size(VALX, VALB)

    def update_size(self, VALX: ValueTracker, VALB: ValueTracker):
        self.add_updater(lambda rect: rect.stretch_to_fit_height(VALX.get_value()))
        self.add_updater(
            lambda rect: rect.stretch_to_fit_width(self.set_xb_width(VALX, VALB))
        )
        return self

    def set_xb_width(self, VALX: ValueTracker, VALB: ValueTracker):
        eq_num = self.equation_number
        if eq_num == 1:
            xb_width = VALX.get_value() + VALB.get_value()
        elif eq_num == 2:
            xb_width = VALB.get_value() - VALX.get_value()
        return xb_width


class HalfBSquare(Square):
    def __init__(
        self, VALB: ValueTracker, move_to: ndarray = ORIGIN, update_size: bool = True
    ):
        super().__init__(
            side_length=0.5 * VALB.get_value(),
            color=COL_HALFB_SQR,
            stroke_width=STROKE_WIDTH,
            stroke_color=COL_B,
            fill_opacity=1,
        )
        self.move_to(move_to)
        if update_size:
            self.update_size(VALB)

    def update_size(self, VALB: ValueTracker):
        self.add_updater(lambda sqr: sqr.stretch_to_fit_height(0.5 * VALB.get_value()))
        self.add_updater(lambda sqr: sqr.stretch_to_fit_width(0.5 * VALB.get_value()))
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
        1: {"X": 0, "B": 2, "C": 4},
        2: {"X": 0, "B": 4, "C": 2},
        3: {"X": 0, "B": 2, "C": 4},
    }

    def __init__(self, eq_num: int):
        if eq_num == 1:
            equation = [r"x^2", "+", "bx", "=", "c"]
        elif eq_num == 2:
            equation = [r"x^2", "+", "c", "=", "bx"]
        elif eq_num == 3:
            equation = [r"x^2", "=", "bx", "+", "c"]
        else:
            equation = [""]
        idx = self.equations[eq_num]
        super().__init__(*equation)
        self.scale(2)
        if eq_num == 1:
            equation_ = {
                "sqr_x": self[0],
                "plus_sign": self[1],
                "b_of_bx": self[2][0],
                "x_of_bx": self[2][1],
                "bx": self[2],
                "=": self[3],
                "c": self[4],
            }
        if eq_num == 2:
            equation_ = {
                "sqr_x": self[0],
                "plus_sign": self[1],
                "c": self[2],
                "=": self[3],
                "b_of_bx": self[4][0],
                "x_of_bx": self[4][1],
                "bx": self[4],
            }
        self.equation_ = equation_
        self.equation_["sqr_x"].set_color(COL_X)
        self.equation_["x_of_bx"].set_color(COL_X)
        self.equation_["b_of_bx"].set_color(COL_B)
        self.equation_["c"].set_color(COL_C)


class PersGeometri(MathTex):
    def __init__(self, eq_num: int, move_to: ndarray = ORIGIN):
        if eq_num == 1:
            equation = [r"(x + \frac{1}{2}b)^2", "=", r"c + \frac{1}{4}b^2"]
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
                "half_b_sqr": self[2][2:],
            }
        elif eq_num == 2:
            equation_ = [""]
        elif eq_num == 3:
            equation_ = [""]
        else:
            equation_ = [""]
        equation_["x"].set_color(COL_X)
        equation_["b"].set_color(COL_B)
        equation_["c"].set_color(COL_C)
        equation_["half_b_sqr"].set_color(COL_HALFB_SQR)
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
            equation = [r"x", "=", r"-\frac{1}{2}b", "+", r"\sqrt{c + \frac{1}{4}b^2}"]
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
        equation_["x"].set_color(COL_X)
        equation_["b"].set_color(COL_B)
        equation_["c"].set_color(COL_C)
        equation_["half_b_sqr"].set_color(COL_HALFB_SQR)
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
class PenyelesaianKhawarizmi(Scene):
    Kaedah: str = ""
    KhawaSqrGroup: VGroup = VGroup()
    eq_num: int = int()

    def setup(self):
        self.add_title(f"Kaedah {self.Kaedah}")
        self.fade_in_equation(eq_num=self.eq_num)

    def construct(self):
        self.eq_to_geometry()
        self.reposition_items()
        self.add_labels()
        self.divide_b_rect()
        self.solve_geometry()
        self.complete_the_square()
        self.geometry_to_eq()
        self.solve_final_eq()
        self.wait(3)

    def pause(self, tick: float = 1):
        self.wait(tick * 0.5)

    def add_title(self, title: str):
        self.TitleGroup = TitleGroup(title)
        self.add(self.TitleGroup)
        twitter = Twitter.Twitter(remove_logo=True, twthandle="Thaza_Kun", scale=0.3)
        self.add(twitter)

    def fade_in_equation(self, eq_num: int):
        self.persamaan_pertama = PersAwal(eq_num=eq_num)
        self.play(FadeIn(self.persamaan_pertama))
        self.pause(3)

    def eq_to_geometry(self):
        pass

    def reposition_items(self):
        pass

    def add_labels(self):
        pass

    def divide_b_rect(self):
        pass

    def solve_geometry(self):
        pass

    def complete_the_square(self):
        pass

    def geometry_to_eq(self):
        pass

    def solve_final_eq(self):
        pass


class PenyelesaianKhawarizmiPertama(PenyelesaianKhawarizmi):
    VALX = ValueTracker(1)
    VALB = ValueTracker(1.5)

    Kaedah = "Pertama"
    eq_num = 1

    X_Square = XSquare(VALX, move_to=DOWN * 2 + LEFT * 2.5)
    BX_Rect = BXRect(VALX, VALB, move_to=DOWN * 2)
    C_Rect = CRect(VALX, VALB, move_to=DOWN * 2, eq_num=1)

    def eq_to_geometry(self):
        equation_ = self.persamaan_pertama.equation_
        x_sqr = self.X_Square
        BX_RectGroup = self.BX_Rect

        self.play(
            Transform(
                equation_["sqr_x"].copy(),
                x_sqr,
                replace_mobject_with_target_in_scene=True,
            )
        )
        self.play(
            Transform(
                equation_["b_of_bx"].copy(),
                BX_RectGroup - BX_RectGroup[3:],
                replace_mobject_with_target_in_scene=True,
            ),
            Transform(
                equation_["x_of_bx"].copy(),
                BX_RectGroup[3:],
                replace_mobject_with_target_in_scene=True,
            ),
        )
        self.play(
            x_sqr.animate.move_to(DOWN * 2 + LEFT * (1 / 2) * BX_RectGroup.width),
            BX_RectGroup.animate.move_to(DOWN * 2 + RIGHT * (1 / 2) * x_sqr.width),
        )
        self.play(
            Transform(
                equation_["c"].copy(),
                self.C_Rect,
                replace_mobject_with_target_in_scene=True,
            )
        )

        x_sqr.set_opacity(COLC_OPACITY)
        BX_RectGroup[0].set_opacity(COLC_OPACITY)
        self.remove(self.C_Rect)
        self.KhawaSqrGroup.add(x_sqr, BX_RectGroup)

    def reposition_items(self):
        x_square, BRectGroup = self.KhawaSqrGroup
        equation = self.persamaan_pertama
        Title = self.TitleGroup

        x_square.add_updater(lambda sqr: sqr.next_to(BRectGroup, LEFT, buff=0))
        self.play(
            equation.animate.scale(0.5),
            self.VALX.animate.set_value(2),
            self.VALB.animate.set_value(2.5),
            BRectGroup[0].animate.move_to(
                DOWN * 2 + RIGHT * 2 * 0.625 + LEFT * 2 * 0.1435
            ),
        )
        *others, follow_rect = x_square.get_updaters()
        x_square.remove_updater(follow_rect)
        self.play(
            equation.animate.next_to(Title, DOWN),
            self.KhawaSqrGroup.animate.move_to(ORIGIN + 1.3 * DOWN),
        )

    def add_labels(self):
        label_x_U = MathTex("x").scale(0.7)
        label_x_U.set_color(COL_X)

        BUFFX: float = 0.3
        label_x_U.next_to(self.KhawaSqrGroup[0], UP, buff=BUFFX)
        label_x_L = label_x_U.copy().next_to(self.KhawaSqrGroup[0], LEFT, buff=BUFFX)

        label_b = MathTex("b").scale(0.7)
        label_b.set_color(COL_B)

        BUFF_B: float = 0.3
        label_b.next_to(self.KhawaSqrGroup[1], UP, buff=BUFF_B)

        self.play(FadeIn(labelGroup := VGroup(label_x_U, label_x_L, label_b)))
        self.pause(3)

        self.labelGroup = labelGroup

    def divide_b_rect(self):
        BRectGroup = self.KhawaSqrGroup[1]
        labelb = self.labelGroup[2]

        position = BRectGroup.get_center()
        BRectLGroup = HalfBRect(
            self.VALX,
            self.VALB,
            move_to=position + LEFT * (1 / 4) * self.VALB.get_value(),
        )
        BRectRGroup = HalfBRect(
            self.VALX,
            self.VALB,
            move_to=position + RIGHT * (1 / 4) * self.VALB.get_value(),
        )

        label_halfb_U = MathTex(r"\frac{1}{2}", "b").scale(0.7)
        label_halfb_U[1].set_color(COL_B)
        label_halfb_L = label_halfb_U.copy()

        BUFF_HALFB: float = 0.1
        label_halfb_U.next_to(BRectLGroup, UP, buff=BUFF_HALFB)
        label_halfb_L.next_to(BRectRGroup, UP, buff=BUFF_HALFB)

        dividerDash = DashedLine(
            start=BRectGroup[3].get_midpoint() + dGAP * UP,
            end=BRectGroup[4].get_midpoint() + dGAP * DOWN,
            color=COL_X,
            stroke_width=STROKE_WIDTH,
            dash_length=DEFAULT_DASH_LENGTH * 2.5,
        )
        dividerLine = Line(
            start=BRectGroup[3].get_midpoint() + dGAP * UP,
            end=BRectGroup[4].get_midpoint() + dGAP * DOWN,
            color=COL_X,
            stroke_width=STROKE_WIDTH,
        )

        self.play(
            LaggedStart(
                Create(dividerDash, run_time=1.5),
                Transform(
                    labelb,
                    VGroup(label_halfb_U, label_halfb_L),
                    replace_mobject_with_target_in_scene=True,
                ),
            )
        )

        self.play(Create(dividerLine))

        self.labelGroup.remove(labelb)
        self.labelGroup.add(label_halfb_U, label_halfb_L)

        self.remove(dividerDash, dividerLine)

        self.add(BRectRGroup, BRectLGroup)
        self.KhawaSqrGroup.add(BRectLGroup, BRectRGroup)

        self.remove(BRectGroup)
        self.KhawaSqrGroup.remove(BRectGroup)

    def solve_geometry(self):
        main_label = self.labelGroup[:-1]
        free_label = self.labelGroup[-1]

        main_geometry = self.KhawaSqrGroup[:-1]
        free_geometry = self.KhawaSqrGroup[-1]

        self.play(
            VGroup(free_geometry, free_label).animate.shift(DOWN),
            VGroup(main_geometry, main_label).animate.shift(UP),
        )
        free_geometry.clear_updaters()  # clear updaters sebab garis-garis dalam tu update itu bentuk dan arah

        self.play(
            Rotate(free_geometry, 0.5 * PI),
            free_label.animate.next_to(free_geometry, LEFT, buff=0.57),
        )

        free_label.add_updater(
            lambda label: label.next_to(free_geometry, LEFT, buff=0.2)
        )
        self.play(free_geometry.animate.next_to(main_geometry[0], DOWN, buff=0))
        free_label.clear_updaters()

        self.play(
            VGroup(self.KhawaSqrGroup, self.labelGroup).animate.move_to(
                ORIGIN + DOWN + 0.5 * UP + 0.25 * LEFT
            )
        )

    def complete_the_square(self):
        def highlight(
            Object: Mobject, color=COL_SQR, gap: float = 0, stroke_proportion: int = 1
        ) -> Mobject:
            mobject = Rectangle(
                height=Object.height + gap,
                width=Object.width + gap,
                color=color,
                stroke_width=stroke_proportion * STROKE_WIDTH,
            ).move_to(Object.get_center())
            return mobject

        half_b_sqr = HalfBSquare(self.VALB)
        half_b_sqr.next_to(self.KhawaSqrGroup[2], RIGHT, buff=0)

        label_halfb_U = self.labelGroup[2].copy()
        label_halfb_L = self.labelGroup[3].copy()

        halfb_sqr_pos = half_b_sqr.get_center()

        halfb_sqr_expression = MathTex(r"\frac{1}{4}", "b", r"^2")
        halfb_sqr_expression.move_to(halfb_sqr_pos)
        halfb_sqr_expression.scale(0.7)
        halfb_sqr_expression[1].set_color(COL_B)

        self.pause(3)
        self.play(Create(hglt := highlight(self.KhawaSqrGroup)))
        self.play(
            Transform(
                VGroup(label_halfb_U, label_halfb_L),
                halfb_sqr_expression,
                replace_mobject_with_target_in_scene=True,
            )
        )
        half_b_sqr.set_z_index(-1)
        self.play(Create(half_b_sqr), run_time=1)
        self.KhawaSqrGroup.add(half_b_sqr)
        self.pause(2)

        self.play(LaggedStart(FadeOut(halfb_sqr_expression), FadeOut(hglt)))
        return half_b_sqr

    def geometry_to_eq(self):
        self.persamaan_geometri = PersGeometri(1, move_to=RIGHT * 2.5 + UP * 0.5)

        def highlight(
            Object: Mobject,
            color=COL_SQR,
            gap: float = 0.2,
            stroke_proportion: int = 0.5,
        ) -> Mobject:
            mobject = Rectangle(
                height=Object.height + gap,
                width=Object.width + gap,
                color=color,
                stroke_width=stroke_proportion * STROKE_WIDTH,
            ).move_to(Object.get_center())
            return mobject

        self.play(VGroup(self.KhawaSqrGroup, self.labelGroup).animate.shift(LEFT * 2.5))
        self.pause()

        b_Right = self.KhawaSqrGroup[1]
        b_Down = self.KhawaSqrGroup[2]
        b_side_D = b_Right[4].copy().shift(0.5 * self.VALB.get_value() * DOWN)
        b_side_R = b_Down[4].copy().shift(0.5 * self.VALB.get_value() * RIGHT)

        equation_ = self.persamaan_geometri.get_parts()

        self.add(b_side_D, b_side_R)
        self.play(
            Transform(b_Down[1].copy(), equation_["x"]),
            Transform(b_side_D, VGroup(equation_["b"], equation_["half_b_free"])),
            GrowFromCenter(equation_["sign_x_plus_b"]),
        )
        self.play(
            Transform(b_Right[2].copy(), equation_["sqr_x"][0]),
            Transform(b_side_R, equation_["sqr_x"][1]),
        )

        self.play(
            Transform(
                self.KhawaSqrGroup[0:3].copy(),
                equation_["c"],
                replace_mobject_with_target_in_scene=True,
            )
        )

        self.play(
            Transform(
                self.KhawaSqrGroup[3].copy(),
                equation_["half_b_sqr"],
                replace_mobject_with_target_in_scene=True,
            )
        )
        self.play(GrowFromCenter(equation_["sign_c_plus_halfb"]))

        hglt = highlight(self.KhawaSqrGroup[:3], gap=0, stroke_proportion=1)

        self.play(Create(hglt))
        self.pause()
        self.play(Transform(hglt, highlight(self.persamaan_geometri[0])))
        self.pause()
        self.play(Transform(hglt, highlight(self.persamaan_geometri[2:])))
        self.pause()
        self.play(FadeOut(hglt), GrowFromCenter(equation_["="]))
        self.pause()

    def solve_final_eq(self):
        awal = self.persamaan_geometri.copy()
        self.persamaan_akhir = PersAkhir(eq_num=1)

        self.add(awal)
        self.play(awal.animate.shift(DOWN * 2))

        self.persamaan_akhir.pivot_to(awal.get_pivot_point())
        awal_ = awal.get_parts()
        akhir_ = self.persamaan_akhir.get_parts()

        self.play(
            Transform(
                VGroup(awal_["c"], awal_["sign_c_plus_halfb"], awal_["half_b_sqr"]),
                VGroup(akhir_["c"], akhir_["sign_c_plus_halfb"], akhir_["half_b_sqr"]),
                replace_mobject_with_target_in_scene=True,
            ),
            Transform(
                awal_["sqr_x"],
                akhir_["sqrt"],
                replace_mobject_with_target_in_scene=True,
            ),
        )
        self.play(
            Transform(
                VGroup(awal_["b"], awal_["half_b_free"]),
                VGroup(akhir_["b"], akhir_["half_b_free"]),
                replace_mobject_with_target_in_scene=True,
            ),
            FadeIn(akhir_["sign_b"], akhir_["sign_b_plus_c"]),
            FadeOut(awal_["sign_x_plus_b"]),
            Transform(
                awal_["x"], akhir_["x"], replace_mobject_with_target_in_scene=True
            ),
            Transform(
                awal_["="], akhir_["="], replace_mobject_with_target_in_scene=True
            ),
        )
        self.play(self.persamaan_akhir.animate.shift(LEFT * 2))


class PenyelesaianKhawarizmiKedua(PenyelesaianKhawarizmi):
    VALX = ValueTracker(1.5)
    VALB = ValueTracker(4)

    Kaedah = "Kedua"
    eq_num = 2

    X_Square = XSquare(VALX, move_to=DOWN * 2 + LEFT * 2.5)
    C_Rect = CRect(VALX, VALB, move_to=DOWN * 2 + RIGHT, eq_num=2)
    BX_Rect = BXRect(VALX, VALB, move_to=DOWN * 2)

    def construct(self):
        self.eq_to_geometry()
        self.reposition_items()
        self.add_labels()
        self.divide_b_rect()
        self.solve_geometry()
        # self.complete_the_square()
        # self.geometry_to_eq()
        # self.solve_final_eq()
        # self.wait(3)

    def eq_to_geometry(self):
        equation_ = self.persamaan_pertama.equation_
        c_rect = self.C_Rect
        x_sqr = self.X_Square
        BX_RectGroup = self.BX_Rect

        self.play(
            Transform(
                equation_["sqr_x"].copy(),
                x_sqr,
                replace_mobject_with_target_in_scene=True,
            )
        )
        self.play(
            Transform(
                equation_["c"].copy(),
                c_rect,
                replace_mobject_with_target_in_scene=True,
            )
        )
        self.play(
            x_sqr.animate.move_to(DOWN * 2 + LEFT * (1 / 2) * c_rect.width),
            c_rect.animate.move_to(DOWN * 2 + RIGHT * (1 / 2) * x_sqr.width),
        )

        self.play(
            Transform(
                equation_["b_of_bx"].copy(),
                BX_RectGroup - BX_RectGroup[3:],
                replace_mobject_with_target_in_scene=True,
            ),
            Transform(
                equation_["x_of_bx"].copy(),
                BX_RectGroup[3:],
                replace_mobject_with_target_in_scene=True,
            ),
        )
        self.KhawaSqrGroup.add(x_sqr, c_rect, BX_RectGroup)
        self.wait(3)

    def reposition_items(self):
        x_square, c_rect, BX_RectGroup = self.KhawaSqrGroup
        equation: VGroup = self.persamaan_pertama
        Title: VGroup = self.TitleGroup

        x_square.add_updater(lambda sqr: sqr.next_to(c_rect, LEFT, buff=0))
        x_square.add_updater(
            lambda sqr: sqr.move_to(DOWN * 2 + LEFT * (1 / 2) * c_rect.width)
        )
        c_rect.add_updater(
            lambda rect: rect.move_to(DOWN * 2 + RIGHT * (1 / 2) * x_square.width)
        ),
        self.play(
            equation.animate.scale(0.5),
            self.VALX.animate.set_value(2.5),
            self.VALB.animate.set_value(6),
            BX_RectGroup[0].animate.move_to(
                VGroup(x_square, c_rect).get_center()
                # DOWN * 2 + LEFT * ((12 * 0.1435) - (2 * 0.625))
            ),
        )
        *others, center_group_while_growing = x_square.get_updaters()
        x_square.remove_updater(center_group_while_growing)
        *others, center_group_while_growing = c_rect.get_updaters()
        c_rect.remove_updater(center_group_while_growing)

        self.play(
            equation.animate.next_to(Title, DOWN),
            self.KhawaSqrGroup.animate.move_to(ORIGIN + 1.3 * DOWN),
        )

    def add_labels(self):
        x_square, c_rect, BX_RectGroup = self.KhawaSqrGroup
        label_x_U = MathTex("x").scale(0.7)
        label_x_U.set_color(COL_X)

        BUFFX: float = -0.4
        label_x_U.next_to(x_square, UP, buff=BUFFX)
        label_x_L = label_x_U.copy().next_to(x_square, LEFT, buff=BUFFX)

        label_b = MathTex("b").scale(0.7)
        label_b.set_color(COL_B)

        BUFF_B: float = 0.3
        label_b.next_to(BX_RectGroup, UP, buff=BUFF_B)

        self.labelGroup: VGroup = VGroup(label_x_U, label_x_L, label_b)
        self.play(FadeIn(self.labelGroup))
        self.pause(3)

    def divide_b_rect(self):
        x_square, c_rect, BRectGroup = self.KhawaSqrGroup
        labelb = self.labelGroup[2]
        labelx_U = self.labelGroup[0]

        position = BRectGroup.get_center()
        half_b_minus_x = 0.5 * self.VALB.get_value() - self.VALX.get_value()

        BRectLGroup = BXRect(
            self.VALX,
            self.VALB,
            width_proportion=self.VALX.get_value() / self.VALB.get_value(),
            move_to=position
            + LEFT * ((1 / 2) * self.VALX.get_value() + half_b_minus_x),
        )
        BRectMidGroup = BXRect(
            self.VALX,
            self.VALB,
            width_proportion=half_b_minus_x / self.VALB.get_value(),
            move_to=position + LEFT * 0.5 * half_b_minus_x,
            show_color=True,
            fill_color=COL_C,
            stroke_color=COL_X,
            hori_color=COL_HALFB_MINUS_C,
            vert_color=COL_X,
        )
        BRectRGroup = HalfBRect(
            self.VALX,
            self.VALB,
            move_to=position + RIGHT * (1 / 4) * self.VALB.get_value(),
        )

        label_halfb_L = MathTex(r"\frac{1}{2}", "b").scale(0.7)
        label_halfb_L[1].set_color(COL_B)
        label_halfb_R = label_halfb_L.copy()

        BUFF_HALFB: float = 0.1
        label_halfb_L.next_to(VGroup(BRectLGroup, BRectMidGroup), UP, buff=BUFF_HALFB)
        label_halfb_R.next_to(BRectRGroup, UP, buff=BUFF_HALFB)

        label_halfb_minus_x = MathTex(r"\frac{1}{2}", "b", "-", "x").scale(0.7)
        label_halfb_minus_x[1].set_color(COL_B)
        label_halfb_minus_x[3].set_color(COL_X)
        label_halfb_minus_x.next_to(BRectMidGroup, UP, buff=BUFF_HALFB)

        dividerDash = DashedLine(
            start=BRectGroup[3].get_midpoint() + dGAP * UP,
            end=BRectGroup[4].get_midpoint() + dGAP * DOWN,
            color=COL_X,
            stroke_width=STROKE_WIDTH,
            dash_length=DEFAULT_DASH_LENGTH * 2.5,
        )
        dividerLine = Line(
            start=BRectGroup[3].get_midpoint() + dGAP * UP,
            end=BRectGroup[4].get_midpoint() + dGAP * DOWN,
            color=COL_X,
            stroke_width=STROKE_WIDTH,
        )

        self.play(
            LaggedStart(
                Create(dividerDash, run_time=1.5),
                Transform(
                    labelb,
                    VGroup(label_halfb_L, label_halfb_R),
                    replace_mobject_with_target_in_scene=True,
                ),
            )
        )
        self.labelGroup.remove(labelb)
        self.labelGroup.add(label_halfb_L, label_halfb_R)
        self.play(Create(dividerLine))
        self.remove(dividerDash)

        temp_halfb_L_line = Line(
            start=BRectLGroup.get_corner(UP + LEFT) + dGAP * DOWN,
            end=BRectMidGroup.get_corner(UP + RIGHT) + dGAP * DOWN,
            color=COL_B,
            stroke_width=STROKE_WIDTH,
        )
        temp_x_U_line = Line(
            start=BRectLGroup.get_corner(UP + LEFT),
            end=BRectLGroup.get_corner(UP + RIGHT),
            color=COL_X,
            stroke_width=STROKE_WIDTH,
        )
        self.add(temp_x_U_line, temp_halfb_L_line)

        TopHalfBGroup = VGroup(label_halfb_L, temp_halfb_L_line)
        TopXGroup = VGroup(labelx_U, temp_x_U_line)

        shift_x_by: float = 0.9
        self.play(
            TopXGroup.animate.shift(shift_x_by * UP),
            TopHalfBGroup.animate.shift((shift_x_by + 0.15) * UP),
        )
        temp_halfb_minus_c_line = Line(
            start=temp_x_U_line.get_end()
            + (0.5 * self.VALB.get_value() - self.VALX.get_value()) * RIGHT,
            end=temp_x_U_line.get_end() + (2 * dGAP) * LEFT,
            color=COL_HALFB_MINUS_C,
            stroke_width=STROKE_WIDTH,
        )
        self.play(Create(temp_halfb_minus_c_line))

        self.play(
            Transform(label_halfb_L, label_halfb_minus_x[:1]),
            Transform(labelx_U, label_halfb_minus_x[3]),
            FadeIn(label_halfb_minus_x),
        )
        self.wait(3)
        self.play(
            Uncreate(temp_halfb_L_line),
            Uncreate(temp_x_U_line),
        )
        self.play(
            temp_halfb_minus_c_line.animate.shift((shift_x_by + dGAP) * DOWN),
            temp_halfb_minus_c_line.copy().animate.shift(
                (shift_x_by + dGAP + self.VALX.get_value()) * DOWN
            ),
        )
        self.remove(temp_halfb_minus_c_line)
        self.KhawaSqrGroup.remove(*self.KhawaSqrGroup[:-1])
        self.remove(dividerLine)
        self.add(
            BRectLGroup,
            BRectRGroup,
            BRectMidGroup,
        )
        self.wait(3)

    def solve_geometry(self):
        # TODO Solve geometry
        main_label = self.labelGroup[:-1]
        free_label = self.labelGroup[-1]

        main_geometry = self.KhawaSqrGroup[:-1]
        free_geometry = self.KhawaSqrGroup[-1]

        self.play(
            VGroup(free_geometry, free_label).animate.shift(DOWN),
            VGroup(main_geometry, main_label).animate.shift(UP),
        )
        free_geometry.clear_updaters()  # clear updaters sebab garis-garis dalam tu update itu bentuk dan arah

        self.play(
            Rotate(free_geometry, 0.5 * PI),
            free_label.animate.next_to(free_geometry, LEFT, buff=0.57),
        )

        free_label.add_updater(
            lambda label: label.next_to(free_geometry, LEFT, buff=0.2)
        )
        self.play(free_geometry.animate.next_to(main_geometry[0], DOWN, buff=0))
        free_label.clear_updaters()

        self.play(
            VGroup(self.KhawaSqrGroup, self.labelGroup).animate.move_to(
                ORIGIN + DOWN + 0.5 * UP + 0.25 * LEFT
            )
        )

    def complete_the_square(self, KhawaSqrGroup: VGroup, labelGroup: VGroup):
        def highlight(
            Object: Mobject, color=COL_SQR, gap: float = 0, stroke_proportion: int = 1
        ) -> Mobject:
            mobject = Rectangle(
                height=Object.height + gap,
                width=Object.width + gap,
                color=color,
                stroke_width=stroke_proportion * STROKE_WIDTH,
            ).move_to(Object.get_center())
            return mobject

        half_b_sqr = HalfBSquare(VALB)
        half_b_sqr.next_to(KhawaSqrGroup[2], RIGHT, buff=0)

        label_halfb_U = labelGroup[2].copy()
        label_halfb_L = labelGroup[3].copy()

        halfb_sqr_pos = half_b_sqr.get_center()

        halfb_sqr_expression = MathTex(r"\frac{1}{4}", "b", r"^2")
        halfb_sqr_expression.move_to(halfb_sqr_pos)
        halfb_sqr_expression.scale(0.7)
        halfb_sqr_expression[1].set_color(COL_B)

        self.pause(3)
        self.play(Create(hglt := highlight(KhawaSqrGroup)))
        self.play(
            Transform(
                VGroup(label_halfb_U, label_halfb_L),
                halfb_sqr_expression,
                replace_mobject_with_target_in_scene=True,
            )
        )
        half_b_sqr.set_z_index(-1)
        self.play(Create(half_b_sqr), run_time=1)
        KhawaSqrGroup.add(half_b_sqr)
        self.pause(2)

        self.play(LaggedStart(FadeOut(halfb_sqr_expression), FadeOut(hglt)))
        return half_b_sqr

    def geometry_to_eq(
        self, KhawaSqrGroup: VGroup, equation: PersGeometri, labelGroup: VGroup
    ):
        def highlight(
            Object: Mobject,
            color=COL_SQR,
            gap: float = 0.2,
            stroke_proportion: int = 0.5,
        ) -> Mobject:
            mobject = Rectangle(
                height=Object.height + gap,
                width=Object.width + gap,
                color=color,
                stroke_width=stroke_proportion * STROKE_WIDTH,
            ).move_to(Object.get_center())
            return mobject

        self.play(VGroup(KhawaSqrGroup, labelGroup).animate.shift(LEFT * 2.5))
        self.pause()

        b_Right = KhawaSqrGroup[1]
        b_Down = KhawaSqrGroup[2]

        b_side_D = b_Right[4].copy().shift(0.5 * VALB.get_value() * DOWN)
        b_side_R = b_Down[4].copy().shift(0.5 * VALB.get_value() * RIGHT)

        equation_ = equation.get_parts()

        self.add(b_side_D, b_side_R)
        self.play(
            Transform(b_Down[1].copy(), equation_["x"]),
            Transform(b_side_D, VGroup(equation_["b"], equation_["half_b_free"])),
            GrowFromCenter(equation_["sign_x_plus_b"]),
        )
        self.play(
            Transform(b_Right[2].copy(), equation_["sqr_x"][0]),
            Transform(b_side_R, equation_["sqr_x"][1]),
        )

        self.play(
            Transform(
                KhawaSqrGroup[0:3].copy(),
                equation_["c"],
                replace_mobject_with_target_in_scene=True,
            )
        )

        self.play(
            Transform(
                KhawaSqrGroup[3].copy(),
                equation_["half_b_sqr"],
                replace_mobject_with_target_in_scene=True,
            )
        )
        self.play(GrowFromCenter(equation_["sign_c_plus_halfb"]))

        hglt = highlight(KhawaSqrGroup[:3], gap=0, stroke_proportion=1)
        self.play(Create(hglt))
        self.pause()
        self.play(Transform(hglt, highlight(equation[0])))
        self.pause()
        self.play(Transform(hglt, highlight(equation[2:])))
        self.pause()
        self.play(FadeOut(hglt), GrowFromCenter(equation_["="]))
        self.pause()
        return equation

    def solve_final_eq(self, original_eq: MathTex):
        awal = original_eq.copy()
        akhir = PersAkhir(eq_num=1)

        self.add(awal)
        self.play(awal.animate.shift(DOWN * 2))

        akhir.pivot_to(awal.get_pivot_point())
        awal_ = awal.get_parts()
        akhir_ = akhir.get_parts()

        self.play(
            Transform(
                VGroup(awal_["c"], awal_["sign_c_plus_halfb"], awal_["half_b_sqr"]),
                VGroup(akhir_["c"], akhir_["sign_c_plus_halfb"], akhir_["half_b_sqr"]),
                replace_mobject_with_target_in_scene=True,
            ),
            Transform(
                awal_["sqr_x"],
                akhir_["sqrt"],
                replace_mobject_with_target_in_scene=True,
            ),
        )
        self.play(
            Transform(
                VGroup(awal_["b"], awal_["half_b_free"]),
                VGroup(akhir_["b"], akhir_["half_b_free"]),
                replace_mobject_with_target_in_scene=True,
            ),
            FadeIn(akhir_["sign_b"], akhir_["sign_b_plus_c"]),
            FadeOut(awal_["sign_x_plus_b"]),
            Transform(
                awal_["x"], akhir_["x"], replace_mobject_with_target_in_scene=True
            ),
            Transform(
                awal_["="], akhir_["="], replace_mobject_with_target_in_scene=True
            ),
        )

        self.play(akhir.animate.shift(LEFT * 2))
        return akhir
