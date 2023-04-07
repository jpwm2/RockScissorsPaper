import tkinter
import numpy
import math
import random
import copy

#初期ステータス
#オブジェクトのスピード
s = 2
#オブジェクトの画像
imgsHolder = ['img0.png', 'img1.png', 'img2.png']
#生成するオブジェの数
quantity = 60


#変えてもうまみがない初期ステータス
#画面サイズ
windowSize = [1800,900]
#オブジェ画像サイズ
objSize = 20

#触れてはいけないステータス
window = tkinter.Tk()
adjustedWinSize = [windowSize[0] + objSize/2, windowSize[1] + objSize/2]
enemy = {0:2, 1:0, 2:1}
prey = {0:1, 1:2, 2:0}
imgs = [tkinter.PhotoImage(file=imgsHolder[0], width=objSize, height=objSize), tkinter.PhotoImage(file=imgsHolder[1], width=objSize, height=objSize),tkinter.PhotoImage(file=imgsHolder[2], width=objSize, height=objSize)]
randomRad = [-math.pi, math.pi]


class Obj:
    def __init__(self, attribute, xy):
        self.attribute = attribute
        self.newAttribute = attribute
        self.xy = xy
        self.prey = prey[attribute]
        self.enemy = enemy[attribute]
        self.img = imgs[attribute]

    def changeAttribute(self, newAttribute):
        self.attribute = newAttribute
        self.prey = prey[newAttribute]
        self.enemy = enemy[newAttribute]
        self.img = imgs[attribute]


    def trigAttribute(self):
        self.newAttribute = enemy[self.attribute]


    def commitAttribute(self):
        self.attribute = self.newAttribute
        self.prey = prey[self.newAttribute]
        self.enemy = enemy[self.newAttribute]
        self.img = imgs[self.attribute]


    def commit(self, o):
        xy = o.xy
        vec = xy - self.xy
        rad = numpy.arctan2(vec[1], vec[0])
        if self.enemy == o.attribute:
            rad += math.pi
        if self.xy[0] == 0 or self.xy[0] == windowSize[0] and rad == math.pi/2 or rad == math.pi * 3/2:
            rad += random.choices(randomRad)
        elif self.xy[1] == 0 or self.xy[1] == windowSize[1] and rad == math.pi or rad == 0:
            rad += random.choices(randomRad)
        self.vxy = numpy.array([s*math.cos(rad),s*math.sin(rad)])
        self.xy = self.xy + self.vxy
        if self.xy[0] <= 0:
            self.xy[0] = 0
        elif self.xy[0] >= windowSize[0]:
            self.xy[0] = windowSize[0]
        if self.xy[1] <= 0:
            self.xy[1] = 0
        elif self.xy[1] >= windowSize[1]:
            self.xy[1] = windowSize[1]
        

def place(canvas, o):
    canvas.create_image(o.xy[0]-objSize/2, o.xy[1]-objSize/2, image=o.img, anchor=tkinter.NW)

# 画面作成
window.geometry(str(windowSize[0]) + 'x' + str(windowSize[1]))
canvas = tkinter.Canvas(window, bg='white', height = windowSize[1], width = windowSize[0])
canvas.place(x=0, y=0)
#オブジェ作成
objs = []
attributes = [0,1,2]
for i in range(quantity):
    attribute = random.choices(attributes)
    xy = numpy.array([random.random()*adjustedWinSize[0], random.random()*adjustedWinSize[1]])
    attribute = attribute[0]
    objs.append(Obj(attribute, xy))

def move():
    global canvas, window, objs
    canvas.delete('all')
    for o in objs:
        nearest =[(windowSize[0] + windowSize[1])**2,None]
        for o1 in objs:
            if o.attribute == o1.attribute:
                pass
            else:
                distance = numpy.linalg.norm(o1.xy - o.xy)
                if distance < objSize:
                    if o.prey == o1.attribute:
                        o1.trigAttribute()
                    else:
                        o.trigAttribute()
                elif distance < nearest[0]:
                    nearest = [distance, o1]
        o.commit(nearest[1])
    for o in objs:
        o.commitAttribute()
        place(canvas, o)
    canvas.update()
    window.after(1, move)

window.after(1,move)
window.mainloop()
