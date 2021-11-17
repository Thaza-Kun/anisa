from manim import *

plane = NumberPlane(x_range=[-7,7,1], y_range=[-4,4,1]).add_coordinates()

class AttachObjects(Scene):
    def construct(self):
        r = ValueTracker(0.5)

        circle = always_redraw(lambda:
            Circle(radius= r.get_value())
        )

        line_radius = always_redraw(lambda:
            Line(start=circle.get_center(), end=circle.get_bottom())
        )

        line_circumference = always_redraw(lambda:
            Line().set_length(2*PI*r.get_value()).next_to(circle, DOWN)  
        )

        self.play(LaggedStart(
            Create(circle), Create(line_radius)
        ))
        self.play(ReplacementTransform(circle.copy(), line_circumference))
        self.play(r.animate.set_value(2))

class Updaters(Scene):
    def construct(self):
        rectangle = RoundedRectangle()

        mathtext = MathTex(r"\frac{a}{b}")
        mathtext.move_to(rectangle.get_center())
        mathtext.add_updater(lambda x: x.move_to(rectangle.get_center())) # Follows the rectangle

        self.play(Create(rectangle))
        self.play(Write(mathtext))
        self.play(rectangle.animate.shift(RIGHT*1.5))
        self.wait()
        mathtext.clear_updaters() # Stop following the rectangle
        self.play(rectangle.animate.shift(LEFT*1))

class MoveBox(Scene):
    """
    A Scene of boxes moving in a predetermined path
    """
    def construct(self):
        box = Rectangle(height=1, width=1)

        self.play(FadeIn(plane))
        self.play(Create(box))
        self.play(box.animate.shift(RIGHT*2), run_time=2)
        self.play(box.animate.shift(LEFT*2 + DOWN*1.5), run_time=2)
        self.play(box.animate.shift(UP*2 - RIGHT*1.5), run_time=2)
        self.play(FadeOut(box))

class FittingObjects(Scene):
    def construct(self):
        circle = Circle(fill_color=RED_A, fill_opacity=1)
        circle.set_width(2).to_edge(DR)

        triangle = Triangle()
        
        self.play(FadeIn(plane))
        self.play(DrawBorderThenFill(circle))
        self.play(circle.animate.set_width(1))
        self.play(Transform(circle, triangle))
        self.wait(2)

