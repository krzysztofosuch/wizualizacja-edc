#!/usr/bin/python3
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3, CollisionTraverser, CollisionSegment, CollisionHandlerEvent, LineSegs, NodePath
from math import pi, sin, cos
from pprint import pprint
import requests
import json
class Wizualizacja(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.taskMgr.add(self.spinCameraTask, "spinCameraTask");
        self.prepareDron()
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
        #bounds_top.drawTo(0,4096,0)
        #bounds_top.moveTo(0,4096,256)

        #bounds_top.reparentTo(self.render) 

    def prepareDron(self):
        self.droneTexture = loader.loadTexture("./6-01.jpg")
        self.dronActor = Actor("dron")
        self.dronActor.setScale(0.5, 0.5, 0.5)
        self.dronActor.setTexture(self.droneTexture)
        self.dronActor.reparentTo(self.render)
        self.dronActor.setPos(2048,2018,128)
    def spinCameraTask(self, task):
        r = requests.get('http://192.168.0.19:5000/singleSteadyRead')
        #r = requests.get('http://192.168.0.19:5000/singleRead')
        data = json.loads(r.text)
        print(data[0], data[1], data[2])
        self.dronActor.setPos(data[0], data[1], data[2])
        self.dronActor.setHpr(data[5],data[6],data[7])
        dronPos = self.dronActor.getPos();
        angleDegrees = task.time*0.0
        angle = (task.time*0.0)*(pi/180.0)
        #self.camera.setPos(dronPos.getX()+40, dronPos.getY()-40, dronPos.getZ()+3)
        #self.camera.setPos(dronPos.getX()+20*sin(angle), dronPos.getY()-20*cos(angle), dronPos.getZ()+3)
        #self.camera.setPos(dronPos.getX(), dronPos.getY(),280)
        self.camera.setPos(self.dronActor, 0, 20, 10)
        self.camera.lookAt(self.dronActor)
        #self.camera.setPos(dronPos.getX(), dronPos.getY(),280)
        return Task.cont
    def walk(self, direction):
        self.dronWalking = direction
    def stop(self):
        self.dronWalking = False
    def setTurn(self, value):
        self.dronTurn = value
app = Wizualizacja()
app.run();
