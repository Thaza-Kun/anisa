from math import sin
from typing_extensions import runtime
from manim import *

class Graphing(Scene):
    def construct(self):
        axes = Axes(x_range=[0,5,0.5], y_range=[0,10,1]).add_coordinates()
        axes.to_edge(DL)
        
        axis_labels = axes.get_axis_labels(x_label="x", y_label="f(x)")

        graph = axes.get_graph(lambda x: x**2, x_range=[0,5])

        graph_object = VGroup(axes, graph, axis_labels)

        self.play(DrawBorderThenFill(axes), Write(axis_labels))
        self.play(Create(graph))

class OnNumberPlane(Scene):
    def construct(self):
        myplane = NumberPlane(x_range=[-6,6], y_range=[-3,3])
        myplane.add_coordinates()

        myfunc = myplane.get_graph(lambda x : np.sin(x))
        area = myplane.get_area(graph = myfunc)

        theline = Line(
            start=myplane.c2p(0, myfunc.underlying_function(-2)),
            end=myplane.c2p(-2, myfunc.underlying_function(-2))
        )

        self.play(DrawBorderThenFill(myplane))
        self.play(Create(myfunc))
        self.play(FadeIn(area))
        self.play(Create(theline))

class SyncedGraph(Scene):
    def construct(self):
        e = ValueTracker(0.01)

        polar = PolarPlane(radius_max=2).add_coordinates()
        polar.shift(LEFT*2.2)
        polgraph = always_redraw(lambda: 
            ParametricFunction(lambda t: polar.polar_to_point(2*np.sin(3*t), t),
                t_range=[0,e.get_value()])
            )

        poldot = always_redraw(lambda:
            Dot().scale(0.5).move_to(polgraph.get_end())
            )

        axes = Axes(x_range=[0,4,1], x_length=3, y_range=[-3,3,1], y_length=3).add_coordinates()
        axes.shift(RIGHT*2.2)
        axgraph = always_redraw(lambda:
            axes.get_graph(lambda x: 2*np.sin(3*x), x_range=[0, e.get_value()])
            )
        
        axdot = always_redraw(lambda:
            Dot().scale(0.5).move_to(axgraph.get_end())
            )

        self.play(Create(polar), Create(axes))
        self.add(polgraph, axgraph, poldot, axdot)
        self.play(e.animate.set_value(PI), run_time=10)
        self.wait()