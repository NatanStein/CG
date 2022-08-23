from OpenGL.GL import *
from OpenGL.GLU import *
import sdl2
import math

N = 20

def InitGL(width, height):
    glClearColor(0.0,0.0,0.0,0.0)
    glClearDepth(1.0)

    mat_ambient = (0.4, 0.0, 0.0, 1.0)
    mat_diffuse = (1.0, 0.0, 0.0, 1.0)
    mat_specular = (1.0, 0.5, 0.5, 1.0)
    mat_shininess = (50,)
    light_position = (0, 10, 10)

    glShadeModel(GL_SMOOTH)
    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_MULTISAMPLE)
    glDepthFunc(GL_LESS)               
    glEnable(GL_DEPTH_TEST)            
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    gluLookAt(0,0,10,0,0,0,0,1,0)

def map(valor, v0, vf, m0, mf):
    return m0+(((valor-v0)*(mf-m0))/(vf-v0))

def cor(i,j):
    g = map(i,0,N,0,1)
    r = map(j,0,N,0,1)
    b = 0
    return r, g, b

def coordenadaEsferica(i,j):
    theta = map(i,0,N,-math.pi/2,math.pi/2)
    phy = map(j,0,N,2*math.pi,0)
    x = r * math.cos(theta)*math.cos(phy)
    y = r * math.sin(theta)
    z = r * math.cos(theta)*math.sin(phy)
    return x, y, z

def paraboloide(x, y):
    return x**2 + y**2

def cela_de_cavalo(x, y):
    return x**2 - y**2   

def calculaNormalFace(v0, v1, v2):
    x = 0
    y = 1
    z = 2
    U = (v2[x]-v0[x], v2[y]-v0[y], v2[z]-v0[z])
    V = (v1[x]-v0[x], v1[y]-v0[y], v1[z]-v0[z])
    N = ((U[y]*V[z]-U[z]*V[y]),(U[z]*V[x]-U[x]*V[z]),(U[x]*V[y]-U[y]*V[x]))
    NLength = -math.sqrt(N[x]*N[x]+N[y]*N[y]+N[z]*N[z])
    return (N[x]/NLength, N[y]/NLength, N[z]/NLength)

def emiteVertice(x, y):
    z0 = cela_de_cavalo(x, y)
    z1 = cela_de_cavalo(x, y + 0.001)
    z2 = cela_de_cavalo(x + 0.001, y)
    v0 = [x, y, z0]
    v1 = [x, y + 0.001, z1]
    v2 = [x + 0.001 , y, z2]
    glNormal3fv(calculaNormalFace(v0, v1, v2))
    glVertex3f(x,y,z0)

velocidade=0
r=1
x0 = -2
xf = 2
y0 = -2
yf = 2
dx = (xf - x0)/N
dy = (yf - y0)/N

def draw():
    global velocidade
    glPushMatrix()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glRotatef(velocidade,0.0,1.0,0.0)   
    y = y0   
    for i in range(0,N):
        glBegin(GL_TRIANGLE_STRIP)
        x = x0
        for j in range(0,N):
            r, g, b = cor(i, j)
            glColor3f(r,g,b)
            emiteVertice(x, y)
            glColor3f(r,g,b)
            emiteVertice(x, y + dy)
            x += dx
        y += dy            
        glEnd()
    velocidade+=1
    glPopMatrix()

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 300

sdl2.SDL_Init(sdl2.SDL_INIT_EVERYTHING)
sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MAJOR_VERSION, 2)
sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MINOR_VERSION, 1)
sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_PROFILE_MASK,sdl2.SDL_GL_CONTEXT_PROFILE_CORE)
sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_DOUBLEBUFFER, 1)
sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_DEPTH_SIZE, 24)
sdl2.SDL_GL_SetSwapInterval(1)
window = sdl2.SDL_CreateWindow(b"Paraboloide  hiperbolico", sdl2.SDL_WINDOWPOS_CENTERED, sdl2.SDL_WINDOWPOS_CENTERED, WINDOW_WIDTH, WINDOW_HEIGHT, sdl2.SDL_WINDOW_OPENGL | sdl2.SDL_WINDOW_SHOWN)

glcontext = sdl2.SDL_GL_CreateContext(window)
InitGL(WINDOW_WIDTH,WINDOW_HEIGHT)
fim = False
event = sdl2.SDL_Event()
while True:
    while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
        if event.type == sdl2.SDL_QUIT:
            fim = True
            break
        if event.type == sdl2.events.SDL_KEYDOWN:
            if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                fim = True
                break
    draw()
    sdl2.SDL_GL_SwapWindow(window)
    if fim:
        break