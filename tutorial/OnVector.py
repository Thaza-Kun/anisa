from manim import *

class Vectors(VectorScene):
    def construct(self):
        plane = self.add_plane(animate=True).add_coordinates()
        vector = self.add_vector([-3,2])

        # basis = self.get_basis_vectors()
        # self.add(basis)
        self.vector_to_coords(vector=vector, clean_up=False) # Draws vector components and a matrix on screen

        new_vector = self.add_vector([2,1])
        self.write_vector_coordinates(vector=new_vector) # Writes only the matrix

class Matrix(LinearTransformationScene):
    def __init__(self):
        LinearTransformationScene.__init__(
            self,
            show_coordinates=True,
            leave_ghost_vectors=True,
            show_basis_vectors=True
        )
    
    def construct(self):
        matrix = [[1,2],[2,1]] # The matrix for transformation

        unit_square = self.get_unit_square()
        text = always_redraw(lambda : Tex("Det(A)").set(width=0.7).move_to(unit_square.get_center()))

        vect = self.get_vector([-1,-2])

        rect = Rectangle(height=2, width=1).shift(UP*2+LEFT*2)

        circ = Circle(radius=1).shift(DOWN*2+RIGHT*2)

        self.add_transformable_mobject(vect, rect, circ)
        self.add_background_mobject(text)
        self.apply_matrix(matrix)
        self.wait()