import sys, time, pygame
from constantes import *
from labyrinthe import *
from timer import *

def chargeParams():
    with open('options.txt', 'r') as file:
        data = file.readlines()

    difficultyChosen = data[0][:-1]
    MODESELECTED=MODESELECT[data[1][:-1]]
    tailleLabyCube=taillesLaby[difficultyChosen]
    TEMPSINIT=timeTotal[difficultyChosen]*1000
    BOOSTTIMEREDUCE = BOOSTTIME[difficultyChosen]

    return difficultyChosen, MODESELECTED, TEMPSINIT, BOOSTTIMEREDUCE, tailleLabyCube

class Joueur:
    def __init__(self,case):
        difficultyChosen, MODESELECTED, TEMPSINIT, BOOSTTIMEREDUCE, tailleLabyCube=chargeParams()
        wr = widthCentralLaby*width/tailleLabyCube
        hr = heightCentralLaby*height/tailleLabyCube
        self.cooldowns={"wb":pygame.time.get_ticks()}
        self.onCase=case
        self.inventaire=[]
        self.sprite=pygame.transform.scale(pygame.image.load("Minion.png"),(int(hr)-4,int(wr)-4))
        self.cadre = self.sprite.get_rect()
        self.cadre = self.cadre.move([self.onCase.x*hr+3+POSXCentralLaby, self.onCase.y*wr+3+POSYCentralLaby])
        
    
    def movejoueur(self,grids,layer,timer):
        difficultyChosen, MODESELECTED, TEMPSINIT, BOOSTTIMEREDUCE, tailleLabyCube=chargeParams()
        keys = pygame.key.get_pressed()
        x=self.onCase.x
        y=self.onCase.y
        wr = widthCentralLaby*width/len(grids[layer][0])
        hr = heightCentralLaby*height/len(grids[layer][0][x])
        
        def aMove(xplus,yplus):
            if not grids[layer][0][x+xplus][y+yplus].locked:
                self.onCase=grids[layer][0][x+xplus][y+yplus]
                self.cadre = self.cadre.move([xplus*hr,yplus*wr])
            elif "key" in self.inventaire:
                self.inventaire.remove("key")
                grids[layer][0][x+xplus][y+yplus].locked=False

        if keys[pygame.K_UP] and not self.onCase.walls[0]:
            aMove(0,-1)
        elif keys[pygame.K_DOWN] and not self.onCase.walls[2]:
            aMove(0,1)
        elif keys[pygame.K_RIGHT] and not self.onCase.walls[1]:
            aMove(1,0)
        elif keys[pygame.K_LEFT] and not self.onCase.walls[3]:
            aMove(-1,0)
        else:
            self.onCase=grids[layer][0][x][y]
        if keys[pygame.K_SPACE] and "wb" in self.inventaire and self.cooldowns["wb"]+500<pygame.time.get_ticks():
            if x!=0 and grids[layer][0][x-1][y].walls[1]:
                grids[layer][0][x-1][y].walls[1]=False
                self.onCase.walls[3]=False
                self.onCase.neighbors.append(grids[layer][0][x-1][y])
            if y!=0 and grids[layer][0][x][y-1].walls[2]:
                grids[layer][0][x][y-1].walls[2]=False
                self.onCase.walls[0]=False
                self.onCase.neighbors.append(grids[layer][0][x][y-1])
            if x!=tailleLabyCube-1 and grids[layer][0][x+1][y].walls[3]:
                grids[layer][0][x+1][y].walls[3]=False
                self.onCase.walls[1]=False
                self.onCase.neighbors.append(grids[layer][0][x+1][y])
            if y!=tailleLabyCube-1 and grids[layer][0][x][y+1].walls[0]:
                grids[layer][0][x][y+1].walls[0]=False
                self.onCase.walls[2]=False
                self.onCase.neighbors.append(grids[layer][0][x][y+1])
            self.inventaire.remove("wb")
            self.cooldowns["wb"]=pygame.time.get_ticks()
        if self.onCase.typeCase=="nextup":
            layer+=1
        for obj in self.onCase.objects[:]:
            if "timer"==obj[:5]:
                timer.timeReduce(int(obj[-3:])*1000)
            if obj=="fAri":
                useFAri(self.onCase)
            else:
                self.inventaire.append(obj)
            self.onCase.objects.remove(obj)
        return layer, timer

    def printPerso(self, screen):
        difficultyChosen, MODESELECTED, TEMPSINIT, BOOSTTIMEREDUCE, tailleLabyCube=chargeParams()
        screen.blit(self.sprite,self.cadre)
    
    def countObjInInv(self, obj):
        count=0
        for object in self.inventaire:
            if object==obj:
                count+=1
        return str(count)

    def printInventory(self, screen):
        screen.blit(spriteKeys,cadreKeys)
        screen.blit(spriteWb,cadreWb)
        nbKeys = myfont.render(":"+self.countObjInInv('key'), False, RED)
        screen.blit(nbKeys,(490, 720))
        nbWb = myfont.render(":"+self.countObjInInv('wb'), False, RED)
        screen.blit(nbWb,(690, 720))
