from manim import *

class PersKhawarizmiPertama(Scene):
    def construct(self):
        ##############################
        # Constants and variables
        TITLE = Text("Penyempurnaan Kuasa Dua Al-Khawarizmi").to_edge(UP)
        SUBTITLE = Text("KAEDAH PERTAMA").next_to(TITLE, DOWN)
        TitleGroup = VGroup(TITLE, SUBTITLE).scale(0.5)

        VALX = ValueTracker(1)
        VALB = ValueTracker(1.5)
        VALC = ValueTracker(VALX.get_value()**2 + VALB.get_value()*VALX.get_value())

        COLX = BLUE
        COLB = YELLOW
        COLC = GREEN

        ##############################
        # OBJEK 1: Persamaan
        pers = MathTex(r"x^2", "+", "bx", "=", "c")
        pers.scale(2)
        pers[0].set_color(COLX)
        pers[2][0].set_color(COLB)
        pers[2][1].set_color(COLX)
        pers[4].set_color(COLC)

        ##############################
        # OBJEK 2: Segi-segi empat
        x_square = Rectangle(
            height=VALX.get_value(), 
            width=VALX.get_value(), 
            color=COLX, 
            stroke_width=DEFAULT_STROKE_WIDTH*2
        ).move_to(DOWN * 2 + LEFT * 1.5)
        x_square.add_updater(lambda sqr: sqr.stretch_to_fit_height(VALX.get_value()))
        x_square.add_updater(lambda sqr: sqr.stretch_to_fit_width(VALX.get_value()))


        b_rect = Rectangle(
            height=VALX.get_value(), 
            width=VALB.get_value(), 
            color=COLX, 
            stroke_width=DEFAULT_STROKE_WIDTH*2
        ).move_to(DOWN * 2 + RIGHT * 1.5).set_z_index(-1)

        b_rect_side_b1 = always_redraw(lambda: 
            Line(
                start=b_rect.get_corner(RIGHT + UP), 
                end=b_rect.get_corner(LEFT + UP), 
                color=COLB, 
                stroke_width=DEFAULT_STROKE_WIDTH*2)
            )
        b_rect_side_b2 = always_redraw(lambda: 
            Line(
                start=b_rect.get_corner(LEFT + DOWN), 
                end=b_rect.get_corner(RIGHT + DOWN), 
                color=COLB, 
                stroke_width=DEFAULT_STROKE_WIDTH*2)
            )
        b_rect_side_x1 = always_redraw(lambda: 
            Line(
                start=b_rect.get_corner(LEFT + UP), 
                end=b_rect.get_corner(LEFT + DOWN), 
                color=COLX, 
                stroke_width=DEFAULT_STROKE_WIDTH*2)
            )
        b_rect_side_x2 = always_redraw(lambda: 
            Line(
                start=b_rect.get_corner(RIGHT + DOWN), 
                end=b_rect.get_corner(RIGHT + UP), 
                color=COLX, 
                stroke_width=DEFAULT_STROKE_WIDTH*2)
            )

        b_rect.add_updater(lambda rect: rect.stretch_to_fit_height(VALX.get_value()))
        b_rect.add_updater(lambda rect: rect.stretch_to_fit_width(VALB.get_value()))


        c_rect = Rectangle(
            height=VALX.get_value(), 
            width=VALX.get_value() + VALB.get_value(), 
            color=COLC, 
            fill_opacity=0.6
        ).move_to(DOWN * 1.5 + RIGHT)     
        c_rect.add_updater(lambda rect: rect.stretch_to_fit_height(VALX.get_value()))
        c_rect.add_updater(lambda rect: rect.stretch_to_fit_width(VALX.get_value() + VALB.get_value()))

        BRectSidesGroup = VGroup(b_rect_side_b1, b_rect_side_b2, b_rect_side_x1, b_rect_side_x2)
        XBGroup = VGroup()

        ##############################
        # OBJEK 3: Supporting Objects

        x_val = always_redraw(lambda:
            Text("x = {:.2f}".format(VALX.get_value()))
                .move_to(UP + LEFT * 1.5)
        )
        b_val = always_redraw(lambda:
            Text("b = {:.2f}".format(VALB.get_value()))
                .move_to(UP + RIGHT * 1.5)
        )

        ##############################
        # ANIMASI

        self.add(TitleGroup)
        self.play(FadeIn(pers))
        self.play(Transform(pers[0].copy(), x_square, replace_mobject_with_target_in_scene=True))
        self.wait(1)
        self.play(Transform(pers[2][1].copy(), b_rect, replace_mobject_with_target_in_scene=True), 
            Transform(pers[2][0].copy(), BRectSidesGroup - b_rect_side_x2 - b_rect_side_x1, replace_mobject_with_target_in_scene=True))
        self.add(b_rect_side_x2, b_rect_side_x1)
        self.wait(1)
        for _ in range(1):
            self.play(VALX.animate.set_value(2))
            self.play(VALX.animate.set_value(1))
        for _ in range(1):
            self.play(VALB.animate.set_value(2.5))
            self.play(VALB.animate.set_value(1.5))
        self.play(x_square.animate.next_to(b_rect, LEFT, buff=0))
        XBGroup.add(x_square, b_rect, BRectSidesGroup)
        XBGroup.set_z_index(2)
        x_square.add_updater(lambda sqr:
            sqr.next_to(b_rect, LEFT, buff=0)
        )
        
        c_rect.move_to(XBGroup.get_center())
        self.play(Transform(pers[4].copy(), c_rect, replace_mobject_with_target_in_scene=True))
        c_rect.add_updater(lambda rect:
            rect.move_to(XBGroup.get_center())
        )

        self.play(pers.animate.scale(0.5))
        self.play(pers.animate.next_to(TitleGroup, DOWN), VALX.animate.set_value(2), VALB.animate.set_value(2.5))
        self.play(XBGroup.animate.move_to(ORIGIN))
        self.wait(3)