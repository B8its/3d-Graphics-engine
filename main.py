import pygame
import numpy
import math

class camera:
    def __init__(self, pos, anglex, angley):
        self.pos = pos 
        self.anglex = anglex
        self.angley = angley
    def directionalMovement(self):

        offset = vector(0,0,0)

        
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.anglex-=0.5
        elif key[pygame.K_RIGHT]:
            self.anglex+=.5
        else:
            self.anglex+=0
        if key[pygame.K_UP]:
            self.angley+=.5
        elif key[pygame.K_DOWN]:
            self.angley-=.5
        else:
            self.angley+=0
        if key[pygame.K_w]:
            offset.x = -.1
        elif key[pygame.K_s]:
            offset.x = .1
        else:
            offset.x = 0
        if key[pygame.K_a]:
            offset.z = -.1
        elif key[pygame.K_d]:
            offset.z = .1
        else:
            offset.z = 0
        if key[pygame.K_LSHIFT]:
            offset.y = -.1
        elif key[pygame.K_LCTRL]:
            offset.y = .1
        else:
            offset.y = 0
    
        # offset = MultiplyMatrixVector(offset, matrotx)
        # offset = MultiplyMatrixVector(offset, matrotz)


        return offset


class vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class triangle:
    def __init__(self, vector1, vector2, vector3):
        self.vector1 = vector1
        self.vector2 = vector2
        self.vector3 = vector3
    
class mesh:
    def __init__(self, triangles):
        self.tris = triangles

def MultiplyMatrixVector(v, m, vec = True):
    newvector = vector(0,0,0)
    if vec == True:


        newvector.x = v.x*m[0,0] + v.y*m[1,0] + v.z*m[2, 0] + m[3, 0]
        newvector.y = v.x* m[0,1] + v.y*m[1,1] + v.z*m[2, 1] + m[3, 1]
        newvector.z = v.x*m[0,2] + v.y*m[1,2] + v.z*m[2, 2] + m[3, 2]
        w = v.x*m[0,3] + v.y*m[1,3] + v.z*m[2, 3] + m[3, 3]
        
        if w != 0:
            newvector.x = newvector.x/w
            newvector.y = newvector.y/w
            newvector.z = newvector.z/w


    
    return newvector
def main():
    screen = [400,400]
    done = True
    projmatrix = numpy.zeros((4,4))
    meshCube = mesh([])
    meshCube.tris = [
        #South
        triangle(vector(0,0,0), vector(0,1,0), vector(1,1,0)),
        triangle(vector(0,0,0), vector(1,1,0), vector(1,0,0)),

        #East
        triangle(vector(1,0,0), vector(1,1,0), vector(1,1,1)),
        triangle(vector(1,0,0), vector(1,1,1), vector(1,0,1)),

        #North
        triangle(vector(1,0,1), vector(1,1,1), vector(0,1,1)), 
        triangle(vector(1,0,1), vector(0,1,1), vector(0,0,1)), 

        #West
        triangle(vector(0,0,1), vector(0,1,1), vector(0,1,0)), 
        triangle(vector(0,0,1), vector(0,1,0), vector(0,0,0)), 

        #Top
        triangle(vector(0,1,0), vector(0,1,1), vector(1,1,1)), 
        triangle(vector(0,1,0), vector(1,1,1), vector(1,1,0)), 

        #Bottom
        triangle(vector(1,0,1), vector(0,0,1), vector(0,0,0)),
        triangle(vector(1,0,1), vector(0,0,0), vector(1,0,0))
    ]

    near = 1
    far = 1000
    fov = 90
    q = near/(far-near)
    aspectratio = screen[0]/screen[1]
    FovRad = 1 / math.tan(fov * .5 / 180 * 3.14159)
    projmatrix[0,0] = aspectratio * FovRad
    projmatrix[1,1] = FovRad
    projmatrix[2,2] = q
    projmatrix[2,3] = 1
    projmatrix[3,2] = -1*near*q
    
    tick = 0





    pygame.init()
    disp = pygame.display.set_mode(screen, pygame.SCALED)

    clock = pygame.time.Clock()
    key = pygame.key.get_pressed()
    lightbulb = vector(0,1,2)
    cam = vector(0,0,0)
    while done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # offset = cam.directionalMovement()
            
        matz = numpy.zeros((4,4))
        matx = numpy.zeros((4,4))

        matz[0,0] = math.cos(math.radians(tick/1.3))
        matz[0,1] = math.sin(math.radians(tick/1.3)) 
        matz[1,0] = -math.sin(math.radians(tick/1.3))
        matz[1,1] = math.cos(math.radians(tick/1.3))
        matz[2,2]  = 1
        matz[3,3] = 1

        matx[0,0] = 1
        matx[1,1] = math.cos(math.radians(tick/2))
        matx[1,2] = math.sin(math.radians(tick/2))
        matx[2,1] = -math.sin(math.radians(tick/2))
        matx[2,2] = math.cos(math.radians(tick/2))    
        matx[3,3] = 1


        

        disp.fill((0,0,0))
        for tri in meshCube.tris:
            triproj, tritranslatez, tritranslatex= triangle(vector(0,0,0), vector(0,0,0), vector(0,0,0)), triangle(vector(0,0,0), vector(0,0,0), vector(0,0,0)),triangle(vector(0,0,0), vector(0,0,0), vector(0,0,0)),
            tritranslated = tri
            
            tritranslatez.vector1  = MultiplyMatrixVector(tri.vector1, matz)
            tritranslatez.vector2 = MultiplyMatrixVector(tri.vector2, matz)
            tritranslatez.vector3 = MultiplyMatrixVector(tri.vector3, matz)

            tritranslatex.vector1 = MultiplyMatrixVector(tritranslatez.vector1, matx)
            tritranslatex.vector2 = MultiplyMatrixVector(tritranslatez.vector2, matx)
            tritranslatex.vector3 = MultiplyMatrixVector(tritranslatez.vector3, matx)

            tritranslated = tritranslatex

            tritranslated.vector1.z = 2
            tritranslated.vector2.z = 2
            tritranslated.vector3.z = 2

            triavg = vector((tritranslated.vector1.x+ tritranslated.vector2.x+ tritranslated.vector3.x)/3,
             (tritranslated.vector1.y+ tritranslated.vector2.y+ tritranslated.vector3.y)/3,
              (tritranslated.vector1.z+ tritranslated.vector2.z+ tritranslated.vector3.z)/3)

            distx = math.sqrt(triavg.x**2 + triavg.z**2)
            dist = (math.sqrt(distx**2 + triavg.z**2)**5)/255*255
            
            colour = (abs(255-dist),abs(255-dist),abs(255-dist))
            


            line1, line2, normal = vector(0,0,0), vector(0,0,0), vector(0,0,0)
            line1.x = tritranslated.vector2.x-tritranslated.vector1.x
            line1.y = tritranslated.vector2.y-tritranslated.vector1.y
            line1.z = tritranslated.vector2.z-tritranslated.vector1.z

            line2.x = tritranslated.vector3.x-tritranslated.vector1.x
            line2.y = tritranslated.vector3.y-tritranslated.vector1.y
            line2.z = tritranslated.vector3.z-tritranslated.vector1.z


            normal.x = line1.y*line2.z - line1.z*line2.y
            normal.y = line1.z*line2.x - line1.x*line2.z
            normal.z = line1.x*line2.y - line1.y*line2.x

            length = math.sqrt(normal.x**2 + normal.y**2 + normal.z**2)
            normal.x /=length; normal.y /=length; normal.z /=length
            


            # if normal.z <= -1:
            if (normal.x* (tritranslated.vector1.x- cam.x) +
                normal.y* (tritranslated.vector1.y- cam.y) +               
                normal.z* (tritranslated.vector1.z- cam.z)                
                ) < 1:
                triproj.vector1 = MultiplyMatrixVector(tritranslated.vector1, projmatrix)
                triproj.vector2 = MultiplyMatrixVector(tritranslated.vector2, projmatrix)
                triproj.vector3 = MultiplyMatrixVector(tritranslated.vector3, projmatrix)

                triproj.vector1.x+=1; triproj.vector1.y+=1
                triproj.vector2.x+=1; triproj.vector2.y+=1
                triproj.vector3.x+=1; triproj.vector3.y+=1

                triproj.vector1.x *= 0.5 * 400
                triproj.vector1.y *= 0.5 * 400
                triproj.vector2.x *= 0.5 * 400
                triproj.vector2.y *= 0.5 * 400
                triproj.vector3.x *= 0.5 * 400
                triproj.vector3.y *= 0.5 * 400

                


                pygame.draw.polygon(disp, colour, ((triproj.vector1.x, triproj.vector1.y),
                (triproj.vector2.x, triproj.vector2.y),
                (triproj.vector3.x, triproj.vector3.y)), width=0)
        
        clock.tick(60)
        pygame.display.update()
        tick+=1

if __name__ == "__main__":
    main()