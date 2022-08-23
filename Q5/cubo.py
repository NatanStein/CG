from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *

verti = ((1, -1, -1),(1, 1, -1),(-1, 1, -1),(-1, -1, -1),(1, -1, 1),(1, 1, 1),(-1, -1, 1),(-1, 1, 1))
edgez = ((0,1),(0,3),(0,4),(2,1),(2,3),(2,7),(6,3),(6,4),(6,7),(5,1),(5,4),(5,7))

def Cubo():
    glBegin(GL_LINES)
    for edge in edgez:
        for vertex in edge:
            glVertex3fv(verti[vertex])
    glEnd()


pygame.init()
display = (400, 300)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
gluPerspective(55, (display[0] / display[1]), 0.1, 100.0)
glTranslatef(0.0, 0.0, -10)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    glRotatef(10, 1, 3, 1)
    glTranslate(0.01,0.01,0.01)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    Cubo()
    pygame.display.flip()
    pygame.time.wait(15)