#!/usr/bin/python3
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from direct.gui.DirectGui import *
from panda3d.core import Point3, CollisionTraverser, CollisionSegment, CollisionHandlerEvent, LineSegs, NodePath, TextNode, CardMaker
from math import pi, sin, cos
from statistics import median
from pprint import pprint
import requests
import json
class Wizualizacja(ShowBase):
    def __init__(self):
        self.cameraMode = 0
        ShowBase.__init__(self)
        self.taskMgr.add(self.spinCameraTask, "spinCameraTask");
        self.prepareDron()
        samples = [0] * 9
        for i in range(0, 9):
            samples[i] = [0] * 5
        self.samples = samples

        self.text_lines = {
                0: OnscreenText(text = str(0.0),pos = (-1.6,0.9),scale = .05,fg=(1,1,1,1),align=TextNode.ALeft,mayChange=1),
                1: OnscreenText(text = str(0.0),pos = (-1.6,0.8),scale = .05,fg=(1,1,1,1),align=TextNode.ALeft,mayChange=1),
                2: OnscreenText(text = str(0.0),pos = (-1.6,0.7),scale = .05,fg=(1,1,1,1),align=TextNode.ALeft,mayChange=1),
                3: OnscreenText(text = str(0.0),pos = (-1.6,0.6),scale = .05,fg=(1,1,1,1),align=TextNode.ALeft,mayChange=1),
                4: OnscreenText(text = str(0.0),pos = (-1.6,0.5),scale = .05,fg=(1,1,1,1),align=TextNode.ALeft,mayChange=1),
                5: OnscreenText(text = str(0.0),pos = (-1.6,0.4),scale = .05,fg=(1,1,1,1),align=TextNode.ALeft,mayChange=1),
                6: OnscreenText(text = str(0.0),pos = (-1.6,0.3),scale = .05,fg=(1,1,1,1),align=TextNode.ALeft,mayChange=1),
                7: OnscreenText(text = str(0.0),pos = (-1.6,0.2),scale = .05,fg=(1,1,1,1),align=TextNode.ALeft,mayChange=1),
                8: OnscreenText(text = str(0.0),pos = (-1.6,0.1),scale = .05,fg=(1,1,1,1),align=TextNode.ALeft,mayChange=1)
            }

        bounds_bottom = LineSegs("bbottom")
        bounds_bottom.set_color(1,0,0)
        bounds_bottom.moveTo(0,0,0)
        bounds_bottom.drawTo(4096,0,0)
        bounds_bottom.drawTo(4096,4096,0)
        bounds_bottom.drawTo(0,4096,0)
        bounds_bottom.drawTo(0,0,0)
        NodePath(bounds_bottom.create()).reparentTo(self.render)

        bounds_mid = LineSegs("mid")
        bounds_mid.set_color(0,1,0)
        bounds_mid.moveTo(0,0,256/3)
        bounds_mid.drawTo(4096,0,256/3)
        bounds_mid.drawTo(4096,4096,256/3)
        bounds_mid.drawTo(0,4096,256/3)
        bounds_mid.drawTo(0,0,256/3)
        bounds_mid.moveTo(0,0,2*256/3)
        bounds_mid.drawTo(4096,0,2*256/3)
        bounds_mid.drawTo(4096,4096,2*256/3)
        bounds_mid.drawTo(0,4096,2*256/3)
        bounds_mid.drawTo(0,0,2*256/3)
        NodePath(bounds_mid.create()).reparentTo(self.render)
        bounds_top = LineSegs("btop")


        bounds_top.set_color(1,0,0)
        bounds_top.moveTo(0,0,256)
        bounds_top.drawTo(4096,0,256)
        bounds_top.drawTo(4096,0,0)
        bounds_top.moveTo(4096,0,256)

        bounds_top.drawTo(4096,4096,256)
        bounds_top.drawTo(4096,4096,0)
        bounds_top.moveTo(4096,4096,256)

        bounds_top.drawTo(0,4096,256)
        bounds_top.drawTo(0,4096,0)
        bounds_top.moveTo(0,4096,256)

        bounds_top.drawTo(0,0,256)
        bounds_top.drawTo(0,0,0)
        bounds_top.moveTo(0,0,256)

        NodePath(bounds_top.create()).reparentTo(self.render)
        ground_grid = LineSegs("mid")
        ground_grid.set_color(0.25,0.38,0)
        for x in range(128):
            ground_grid.moveTo(0,x*32,0)
            ground_grid.drawTo(4096,x*32,0)
            ground_grid.moveTo(x*32,0,0)
            ground_grid.drawTo(x*32,4096,0)

        NodePath(ground_grid.create()).reparentTo(self.render)


        self.terrainLine = LineSegs("terrainLine")
        self.terrainLine.set_color(1,1,1)
        #bounds_top.drawTo(0,4096,0)
        #bounds_top.moveTo(0,4096,256)

        #bounds_top.reparentTo(self.render)
        self.accept("space-up", self.changeCamera)
    def changeCamera(self):
        self.cameraMode+=1
        if self.cameraMode > 4:
            self.cameraMode = 0


        #bounds_top.drawTo(0,4096,0)
        #bounds_top.moveTo(0,4096,256)

        #bounds_top.reparentTo(self.render)

    def prepareDron(self):
        self.dronActor = Actor("dron")
        self.dronActor.setScale(0.2, 0.2, 0.2)
        self.dronActor.reparentTo(self.render)
        self.dronActor.setPos(2048,2018,128)


    def spinCameraTask(self, task):
        try:
            data = self.getParams()
            print(data[3], data[4], data[5])
            self.dronActor.setPos(data[0], data[1], data[2])
            self.dronActor.setHpr(data[5],data[6],data[7])
            dronPos = self.dronActor.getPos();
            angleDegrees = task.time*0.0
            angle = (task.time*0.0)*(pi/180.0)
            self.last_data = data
        except Exception as e:
            data = self.last_data
            print(e)

        # pprint(data)

        labels = {
            0: "X = ",
            1: "Y = ",
            2: "Wysokość bezw. = ",
            3: "Wysokość wzgl. = ",
            4: "Bateria = ",
            5: "Azymut = ",
            6: "Pitch = ",
            7: "Roll = ",
            8: "Czas = "
        }

        for x in data:
            if data.index(x) == 8:
                try:
                    time_string = "Dzień: " + str(ord(x[1])) + ", " + str(ord(x[2])).zfill(2) + ":" + str(ord(x[3])).zfill(2) + ":" + str(ord(x[4])).zfill(2)
                    self.text_lines[data.index(x)].setText(labels[data.index(x)] + str(time_string))
                except IndexError:
                    self.text_lines[data.index(x)].setText(labels[data.index(x)] + "")
            else:
                self.text_lines[data.index(x)].setText(labels[data.index(x)] + str(float("{:10.3f}".format(x))))

        # print(data[0], data[1], data[2])
        self.dronActor.setPos(data[0], data[1], data[2])
        self.dronActor.setHpr(data[5],data[6],data[7])
        dronPos = self.dronActor.getPos();
        angleDegrees = task.time*0.0
        angle = (task.time*0.0)*(pi/180.0)
        #self.camera.setPos(dronPos.getX()+40, dronPos.getY()-40, dronPos.getZ()+3)
        #self.camera.setPos(dronPos.getX()+20*sin(angle), dronPos.getY()-20*cos(angle), dronPos.getZ()+3)
        #self.camera.setPos(dronPos.getX(), dronPos.getY(),280)
        if self.cameraMode == 0:
            self.camera.setPos(self.dronActor.getPos())
            self.camera.setPos(self.camera, 0,10,20)
            self.camera.lookAt(self.dronActor)
        elif self.cameraMode == 1:
            self.camera.setPos(0,0,255)
            self.camera.lookAt(self.dronActor)
        elif self.cameraMode == 2:
            self.camera.setPos(4096,4096,255)
            self.camera.lookAt(self.dronActor)
        if self.cameraMode == 3:
            self.camera.setPos(self.dronActor, 0, 20, 3)
            self.camera.lookAt(self.dronActor)
        if self.cameraMode == 4:
            self.camera.setPos(self.dronActor, 0, 45, 6)
            self.camera.lookAt(self.dronActor)
        #self.camera.setPos(dronPos.getX(), dronPos.getY(),280)
        self.drawTerrainLine(data[3])
        return Task.cont
    def drawTerrainLine(self, relativeHeight):
        dronePos = self.dronActor.getPos()
        tHeight = dronePos.getZ()-relativeHeight
        self.terrainLine.drawTo(dronePos.getX(), dronePos.getY(),tHeight)
        NodePath(self.terrainLine.create()).reparentTo(self.render)
    def getParams(self):
        data = [0] * 9

        r = requests.get('http://192.168.0.19:5000/singleRead')
        loadedData = json.loads(r.text)
        for i in range(0,8):
            self.samples[i].append(loadedData[i])

            if len(self.samples[i]) > 5:
                del self.samples[i][0]

        uart = loadedData[8]
        del loadedData[8]

        data[0] = median(self.samples[0])
        data[1] = median(self.samples[1])
        data[2] = median(self.samples[2])
        data[3] = median(self.samples[3])
        data[4] = median(self.samples[4])
        data[5] = median(self.samples[5])
        data[6] = median(self.samples[6])
        data[7] = median(self.samples[7])
        data[8] = uart
        return data

    def walk(self, direction):
        self.dronWalking = direction
    def stop(self):
        self.dronWalking = False
    def setTurn(self, value):
        self.dronTurn = value

app = Wizualizacja()
app.run();
