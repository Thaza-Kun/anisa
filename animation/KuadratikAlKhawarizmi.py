from manim import *
from numpy import half, square

class PersKhawarizmiPertama(Scene):

    def construct(self):
        ##############################
        # Constants and variables
        TITLE = Text("Penyempurnaan Kuasa Dua Al-Khawarizmi").to_edge(UP)
        SUBTITLE = Text("KAEDAH PERTAMA").next_to(TITLE, DOWN)
        TitleGroup = VGroup(TITLE, SUBTITLE).scale(0.5)

        VALX = ValueTracker(1)
        VALB = ValueTracker(1.5)
        VALC = always_redraw(lambda:
            ValueTracker(VALX.get_value()**2 + VALB.get_value()*VALX.get_value())
        )

        COLX = BLUE
        COLB = YELLOW
        COLC = GREEN

        COLSQR = RED
        COLHALFB = COLSQR

        COLC_OPACITY = 0.6

        STROKE_WIDTH = DEFAULT_STROKE_WIDTH*2

        dGAP = 0.037

        ##############################
        # OBJEK 1: Persamaan
        pers = MathTex(r"x^2", "+", "bx", "=", "c")
        pers.scale(2)
        pers[0].set_color(COLX)
        pers[2][0].set_color(COLB)
        pers[2][1].set_color(COLX)
        pers[4].set_color(COLC)

        # Persamaan Akhir
        pers_lengkap = MathTex("(x + b)^2","=",r"c + \frac{1}{2}b")
        pers_lengkap.move_to(DOWN*3)

        pers_lengkap_ = {
            "x": pers_lengkap[0][1],
            "b": pers_lengkap[0][3],
            "c": pers_lengkap[2][0],
            "halfb": pers_lengkap[2][2:]
        }
        pers_lengkap_["x"].set_color(COLX)
        pers_lengkap_["b"].set_color(COLB)
        pers_lengkap_["c"].set_color(COLC)
        pers_lengkap_["halfb"].set_color(COLHALFB)

        ##############################
        # OBJEK 2: Segi Empat X
        x_square = Square(
            side_length=VALX.get_value(),
            color=COLC,
            stroke_width = STROKE_WIDTH,
            stroke_color = COLX
        ).move_to(DOWN*2 + LEFT*1.5)
        x_square.add_updater(lambda sqr: sqr.stretch_to_fit_height(VALX.get_value()))
        x_square.add_updater(lambda sqr: sqr.stretch_to_fit_width(VALX.get_value()))

        KhawaSqrGroup = VGroup()

        ##############################
        # OBJEK 3: Segi Empat B
        def create_bx_rect(width: float = 1, opacity: float = 0):
            main = Rectangle(
                height=VALX.get_value(),
                width=width*VALB.get_value(),
                color=COLC,
                stroke_width = STROKE_WIDTH,
                stroke_color = COLB,
                fill_opacity=opacity
            )

            vertex = main.get_vertices()

            main.add_updater(lambda rect: rect.stretch_to_fit_height(VALX.get_value()))
            main.add_updater(lambda rect: rect.stretch_to_fit_width(width*VALB.get_value()))

            def vert_side(side, RectMobject):
                GAP = [0,dGAP,0]
                ret = always_redraw(lambda:
                    Line(
                        start   = RectMobject.get_corner(side + UP) + GAP,
                        end     = RectMobject.get_corner(side + DOWN) - GAP,
                        color   = COLX,
                        stroke_width = STROKE_WIDTH
                    )
                )
                return ret

            def hori_side(side, RectMobject):
                GAP = [dGAP,0,0]
                ret = always_redraw(lambda:
                    Line(
                        start   = RectMobject.get_corner(LEFT + side) - GAP,
                        end     = RectMobject.get_corner(RIGHT + side) + GAP,
                        color   = COLB,
                        stroke_width = STROKE_WIDTH
                    )
                )
                return ret

            side_xL = vert_side(LEFT, main)
            side_xR = vert_side(RIGHT, main)
            side_bT = hori_side(UP, main)
            side_bB = hori_side(DOWN, main)

            return VGroup(main, side_bT, side_bB, side_xL, side_xR)

        BRectGroup = create_bx_rect(width=1)
        BRectGroup.move_to(DOWN*2 + RIGHT*1.5)

        # Bila dah jadi setengah
        BRectLGroup = create_bx_rect(width=0.5, opacity=COLC_OPACITY)
        BRectRGroup = create_bx_rect(width=0.5, opacity=COLC_OPACITY)

        ##############################
        # OBJEK 4: Segi Empat C

        c_rect = Rectangle(
            height=VALX.get_value(),
            width=VALX.get_value() + VALB.get_value(),
            color=COLC,
            fill_opacity=COLC_OPACITY
        ).move_to(DOWN*2)
        c_rect.set_z_index(-1)
        c_rect.add_updater(lambda rect: rect.stretch_to_fit_height(VALX.get_value()))
        c_rect.add_updater(lambda rect: rect.stretch_to_fit_width(VALX.get_value() + VALB.get_value()))

        ##############################
        # OBJEK 5: Segi Empat Khawarizmi Lengkap

        half_b_square = Square(
            side_length=0.5*VALB.get_value(),
            color=COLHALFB,
            stroke_width=STROKE_WIDTH,
            stroke_color = COLB,
            fill_opacity = 1
        )
        half_b_square.add_updater(lambda sqr: sqr.stretch_to_fit_height(0.5*VALB.get_value()))
        half_b_square.add_updater(lambda sqr: sqr.stretch_to_fit_width(0.5*VALB.get_value()))

        ##############################
        # OBJEK 6: Segi Empat Khawarizmi Lengkap

        Khawa_sqr_complete = Square(
            side_length=VALX.get_value() + 0.5*VALB.get_value(),
            color=COLSQR,
            stroke_width = STROKE_WIDTH
        )
        Khawa_sqr_complete.add_updater(lambda sqr: sqr.stretch_to_fit_height(VALX.get_value() + 0.5*VALB.get_value()))
        Khawa_sqr_complete.add_updater(lambda sqr: sqr.stretch_to_fit_width(VALX.get_value() + 0.5*VALB.get_value()))
        Khawa_sqr_complete.move_to(ORIGIN + 0.5*DOWN)

        ##############################
        # OBJEK: Fungsi tambahan
        def update_lines(RectMobject: Rectangle, left:Line, right:Line, top: Line, bottom:Line) -> None:
            top.add_updater(lambda ln: 
                ln.set_points_by_ends(
                    RectMobject.get_corner(LEFT + UP) + dGAP*LEFT,
                    RectMobject.get_corner(RIGHT + UP) + dGAP*RIGHT,
                )
            )
            bottom.add_updater(lambda ln: 
                ln.set_points_by_ends(
                    RectMobject.get_corner(LEFT + DOWN) + dGAP*LEFT,
                    RectMobject.get_corner(RIGHT + DOWN) + dGAP*RIGHT,
                )
            )
            left.add_updater(lambda ln: 
                ln.set_points_by_ends(
                    RectMobject.get_corner(LEFT + UP) + dGAP*UP,
                    RectMobject.get_corner(LEFT + DOWN) + dGAP*UP,
                )
            )
            right.add_updater(lambda ln: 
                ln.set_points_by_ends(
                    RectMobject.get_corner(RIGHT + UP) + dGAP*UP,
                    RectMobject.get_corner(RIGHT + DOWN) + dGAP*UP,
                )
            )
        

        ##############################
        # ANIMASI
        ##############################
        self.add(TitleGroup)
        self.play(FadeIn(pers))

        # Pertunjukan X dan B adalah sisi segi empat
        self.play(Transform(pers[0].copy(), x_square, replace_mobject_with_target_in_scene=True))
        self.play(Transform(pers[2][0].copy(), BRectGroup - BRectGroup[3:], replace_mobject_with_target_in_scene=True),
            Transform(pers[2][1].copy(), BRectGroup[3:], replace_mobject_with_target_in_scene=True))
        self.play(x_square.animate.move_to(DOWN*2 + LEFT*0.625 + LEFT*0.1435), BRectGroup.animate.move_to(DOWN*2 + RIGHT*0.625 + LEFT*0.1435))
        KhawaSqrGroup.add(x_square, BRectGroup)

        # C ialah luas semuanya
        self.play(Transform(pers[4].copy(), c_rect, replace_mobject_with_target_in_scene=True))
        x_square.set_opacity(COLC_OPACITY)
        BRectGroup[0].set_opacity(COLC_OPACITY)
        self.remove(c_rect)

        # Repositioning
        x_square.add_updater(lambda sqr: sqr.next_to(BRectGroup, LEFT, buff=0))
        self.play(pers.animate.scale(0.5),
                VALX.animate.set_value(2),
                VALB.animate.set_value(2.5),
                BRectGroup[0].animate.move_to(DOWN*2 + RIGHT*2*0.625 + LEFT*2*0.1435)
                )
        *others , follow_rect = x_square.get_updaters() 
        x_square.remove_updater(follow_rect)
        self.play(pers.animate.next_to(TitleGroup, DOWN),
                KhawaSqrGroup.animate.move_to(ORIGIN + DOWN))

        # b Bahagi Dua
        dividerDash = DashedLine(
                    start=BRectGroup[1].get_midpoint() + dGAP*UP,
                    end=BRectGroup[2].get_midpoint() + dGAP*DOWN,
                    color=COLX,
                    stroke_width=STROKE_WIDTH,
                    dash_length=DEFAULT_DASH_LENGTH*2.5
                    )
        dividerLine = Line(
                    start=BRectGroup[1].get_midpoint() + dGAP*UP,
                    end=BRectGroup[2].get_midpoint() + dGAP*DOWN,
                    color=COLX,
                    stroke_width=STROKE_WIDTH
                    )
        self.play(Create(dividerDash))
        self.play(Create(dividerLine))

        BRectLGroup[0].add_updater(lambda rect: rect.next_to(x_square, RIGHT, buff=0.02))
        BRectRGroup[0].next_to(BRectGroup[4], LEFT)
        self.add(BRectLGroup, BRectRGroup)
        self.remove(BRectGroup, dividerDash, dividerLine)
        KhawaSqrGroup.remove(BRectGroup)
        KhawaSqrGroup.add(BRectLGroup, BRectRGroup)

        # bawa setengah b melekat di bawah x
        self.play(BRectRGroup[0].animate.shift(DOWN), x_square.animate.shift(UP))
        # restore_updater = BRectRGroup.get_updaters()
        BRectRGroup.clear_updaters()
        self.play(Rotate(BRectRGroup, 0.5*PI))
        self.play(BRectRGroup.animate.next_to(x_square, DOWN, buff=0))

        # Reposition the incomplete square
        *rest, follow_x = BRectLGroup[0].get_updaters()
        BRectLGroup[0].remove_updater(follow_x)
        BRectLGroup[0].add_updater(lambda rect: rect.move_to(x_square.get_center() + (VALX.get_value()-0.1)*RIGHT))
        *rest, follow_x = BRectLGroup[0].get_updaters()
        BRectLGroup[0].remove_updater(follow_x)
        update_lines(*BRectRGroup)
        BRectRGroup[0].add_updater(lambda rect: rect.move_to(x_square.get_center() + (VALX.get_value()-0.1)*DOWN))
        *rest, follow_x = BRectRGroup[0].get_updaters()
        BRectRGroup.clear_updaters()
        self.play(KhawaSqrGroup.animate.move_to(Khawa_sqr_complete.get_center()))

        # Completing the Square
        half_b_square.move_to(x_square.get_center() + (0.5*VALX.get_value() + 0.25*VALB.get_value() + 0.03)*(DOWN + RIGHT) + 0.01*LEFT + 0.01*DOWN)
        self.remove(BRectRGroup[1:])
        self.play(Create(Khawa_sqr_complete), run_time=2)
        self.play(FadeOut(Khawa_sqr_complete), FadeIn(half_b_square))
        b_side_R, b_side_D = BRectRGroup[2].copy().shift(0.5*VALB.get_value()*RIGHT), BRectLGroup[2].copy().shift(0.5*VALB.get_value()*DOWN)
        
        # Terjemah menjadi persamaan
        self.add(b_side_D, b_side_R)
        self.play(
            Transform(BRectRGroup[3].copy(), pers_lengkap_["x"]), 
            Transform(b_side_D, pers_lengkap_["b"]), 
            Create(pers_lengkap[0][2])
            )
        pers_sementara = VGroup(pers_lengkap_["x"].copy(), pers_lengkap[0][2].copy(), pers_lengkap_["b"].copy()).shift(2*RIGHT)
        self.play(
            Transform(BRectLGroup[4].copy(), pers_sementara[0], replace_mobject_with_target_in_scene=True), 
            Transform(b_side_R, pers_sementara[2], replace_mobject_with_target_in_scene=True),
            FadeIn(pers_sementara[1])
            )
        mult_position = (pers_sementara.get_center() + pers_sementara.copy().shift(-2*RIGHT).get_center()) / 2
        mult = MathTex(r"\cross").move_to(mult_position)
        self.play(FadeIn(mult))
        self.play(Transform(pers_sementara, pers_lengkap[0]), FadeOut(mult))
        self.play(Transform(KhawaSqrGroup.copy(), pers_lengkap_["c"], replace_mobject_with_target_in_scene=True))
        self.play(
            Transform(half_b_square.copy(), pers_lengkap_["halfb"], replace_mobject_with_target_in_scene=True), 
            FadeIn(pers_lengkap[2][1])
            )
        self.play(FadeIn(pers_lengkap[1]))
        # self.add(pers_lengkap)
        self.wait(2)
        self.wait(3)