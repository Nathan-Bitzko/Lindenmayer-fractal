# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 13:21:48 2021

store rules, fractal lines, and generate fractals

@author: Nathan Bitzko
"""

#ToDo - handel exceptions
import math
from PIL import Image, ImageDraw

class Generate:
    coordMin = {"x" : 99999, "y" : 99999}
    coordMax = {"x" : -99999, "y" : -99999}
    lines = []
    
    def __init__(self):
        pass
    
    def addLine(self, xOne, yOne, xTwo, yTwo):
        self.lines.append({"xOne":xOne, "yOne":yOne, "xTwo":xTwo, "yTwo":yTwo})
    
    """
    creates final fractal string
    """
    def generateFracString(self, rules, filename):
        varStr = rules['']
        iters = rules["iterations"]
        while iters > 0:
            newVarStr = ""
            for var in [char for char in varStr]:
                if var not in ("[]+-"):
                    try:
                        newVarStr += rules[var]
                    except Exception:
                        newVarStr += var
                else:
                    newVarStr += var
            varStr = newVarStr
            iters -= 1
        self.generateFracLines(varStr, rules, filename)
    
    """
    generates the lines that draw a fractal froma a fractal string
    """
    def generateFracLines(self, varStr, rules, filename):
        currX = rules["startX"]
        currY = rules["startY"]
        coordStack = []
        angleStack = []
        lineLen = rules["length"]
        ignore = rules["noActionVars"]
        curAng = rules["startAngle"]
        #loop through fractal string
        for var in [char for char in varStr]:
            #save and load coordinates and agles to and from a stack
            if var == "[":
                coordStack.append({"x" : currX, "y" : currY})
                angleStack.append(curAng)
            elif var == "]":
                try:
                    coord = coordStack.pop()
                    currX = coord["x"]
                    currY = coord["y"]
                    curAng = angleStack.pop()
                except Exception:
                    pass
            #change direction in which linews are drawn
            elif var == "-":
                curAng = curAng - rules["angle"]
            elif var == "+":
                curAng = curAng + rules["angle"]
            #draw line and update current coordinates
            else:
                newX = lineLen * math.cos(math.radians(curAng)) + currX
                newY = lineLen * math.sin(math.radians(curAng)) + currY
                if var not in ignore:
                    self.addLine(currX, currY, newX, newY)
                currX = newX
                currY = newY
                #save smallest coordinate values
                if newX < self.coordMin["x"]:
                    self.coordMin["x"] = newX
                if newY < self.coordMin["y"]:
                    self.coordMin["y"] = newY
                #save largest coordinate values
                if newX > self.coordMax["x"]:
                    self.coordMax["x"] = newX
                if newY > self.coordMax["y"]:
                    self.coordMax["y"] = newY
        self.saveFractal(filename)
    
    #save the fractal as a image (tkinter canvas cant handle thousands of lines)
    def saveFractal(self, filename):
        minimum = self.coordMin
        maximum = self.coordMax
        #find fractal image size
        width = int(math.ceil(maximum["x"]-minimum["x"]))
        height = int(math.ceil(maximum["y"]-minimum["y"]))
        image = Image.new("RGB", (width+10, height+10), "white")
        #draw fractal
        draw = ImageDraw.Draw(image)
        for line in self.lines:
            xOne = line["xOne"] - minimum["x"]
            yOne = line["yOne"] - minimum["y"]
            xTwo = line["xTwo"] - minimum["x"]
            yTwo = line["yTwo"] - minimum["y"]
            draw.line([xOne, yOne, xTwo, yTwo], "black")
        image.save(filename)
                    