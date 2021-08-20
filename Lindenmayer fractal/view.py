# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 13:21:06 2021

Lindenmayer fractal view

@author: nathan bitzko
"""

from tkinter import Canvas, Frame, Scrollbar, Label, StringVar, Entry, Button
from tkinter import Tk, mainloop, LEFT, RIGHT, N, W, E, S
from tkinter.filedialog import asksaveasfile
from PIL import Image
import generator
import values
import imgZoom
import re
import os
import threading
from multiprocessing import Process

RULES_WIDTH = 300
RULE_HEIGHT = 75
ANGLE = 90
ANGLE_KEY = "angle"
START_ANGLE = -90
START_X = 900
START_Y = 600
ITERATIONS = 4
ITERATIONS_KEY = "iterations"
LENGTH = 10
LENGTH_KEY = "length"
IMG_WIDTH = 500
IMG_HEIGHT = 500
NO_ACTION_VARS = ""
NO_ACTION_KEY = "noActionVars"
FILENAME = "fractal.png"

#top level widgets that were made clobal for ease of use in functions
rules = "placeholder"
fractal = "placeholder"

sem = threading.Semaphore()

availableVars = ['9', '8', '7', '6', '5', '4', '3', '2', '1', 'z', 'y', 'x', 
                 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 
                 'k', 'j', 'i', 'h', 'g', 'f', 'e', 'd', 'c', 'b', 'a']
numRules = 0

vals = values.Values(START_ANGLE, ANGLE, START_X, START_Y, ITERATIONS, NO_ACTION_VARS, LENGTH)

def getVar():
    try:
        return availableVars.pop()
    except:
        return -1


"""
event handlers
"""
def drawFractal():
    sem.acquire()
    argOne = vals.getRules()
    argTwo = FILENAME
    p = Process(target=drawFractalSafe, args=(argOne, argTwo,))
    p.start()
    sem.release()
    fractal.after(100, drawFractalfinal, p)

def drawFractalfinal(p):
    if p.is_alive():
        fractal.after(200, drawFractalfinal, p)
    else:
        fractalCanvas = imgZoom.MainWindow(fractal, FILENAME)
    
def drawFractalSafe(fracRules, file):
    gen = generator.Generate()
    gen.generateFracString(fracRules, file)
    
def save():
    image = Image.open(FILENAME)
    file = asksaveasfile(mode='w', defaultextension=".png")
    if file:
        path = os.path.abspath(file.name)
        image.save(path)
    file.close()
    
def setRule(var, rule):
    t = threading.Thread(target=setRuleSafe, args=(var, rule.get(),))
    t.start()
        
def setRuleSafe(var, rule):
    sem.acquire()
    vals.setRule(var, rule)
    sem.release()

def setIgnoreVars(ignore):
    ignore.set(re.sub("[\[\]\+\-]", "", ignore.get()))
    t = threading.Thread(target=setRuleSafe, args=(NO_ACTION_KEY, ignore.get(),))
    t.start()

def setAngle(angle):
    try:
        angle = float(angle.get())
        t = threading.Thread(target=setRuleSafe, args=(ANGLE_KEY, angle,))
        t.start()
    except Exception:
        if angle.get() != "":
            angle.set(re.sub("[^0-9]","",angle.get()))
            setAngle(angle)
      
def setIterations(iterations):
    try:
        iterations = int(iterations.get())
        t = threading.Thread(target=setRuleSafe, args=(ITERATIONS_KEY, iterations,))
        t.start()
    except Exception:
        if iterations.get() != "":
            iterations.set(re.sub("[^0-9]","",iterations.get()))
            setIterations(iterations)
         
def setLength(length):
    try:
        length = float(length.get())
        t = threading.Thread(target=setRuleSafe, args=(LENGTH_KEY, length,))
        t.start()
    except Exception:
        if length.get() != "":
            length.set(re.sub("[^0-9]","",length.get()))
            setLength(length)
    
def newRule():
    global numRules
    var = getVar()
    if var == -1:
        return
    varFrame = Frame(rules, highlightbackground="black", highlightthickness=1, width = RULES_WIDTH, height = RULE_HEIGHT)
    varFrame.grid(row = numRules + 7, column = 0, sticky = W+E)
    varFrame.grid_propagate(0)
    numRules += 1

    varLab = Label(varFrame, text=var + " : ")
    varLab.pack(side=LEFT)

    varStr = StringVar()
    varStr.trace("w", lambda name, index, mode, varStr=varStr: setRule(var, varStr))
    varIn = Entry(varFrame, width = RULES_WIDTH, textvariable=varStr)
    varIn.pack(side=RIGHT, pady=5)
    if var == "a":
        varStr.set("a+a-a-a+a")
        setRule(var, varStr)
    else:
        varStr.set(var)
        setRule(var, varStr)
        
        
        
"""
initial set up
"""
def makeButtons():
    buttonFrame = Frame(rules, highlightbackground="black", highlightthickness=1, width = RULES_WIDTH, height = RULE_HEIGHT - 25)
    buttonFrame.grid(row = 0, column = 0, sticky = W+E)
    buttonFrame.grid_propagate(0)

    generate = Button(buttonFrame, text = "Generate", command=drawFractal)
    generate.grid(row=0, column = 0, padx=34, pady=10)

    clear = Button(buttonFrame, text = "Add Rule", command=newRule)
    clear.grid(row=0, column = 1, pady=10)

    addRule = Button(buttonFrame, text = " Save ", command=save)
    addRule.grid(row=0, column=2, padx=34, pady=10)
    
def makeAxiom():
    axiomFrame = Frame(rules, highlightbackground="black", highlightthickness=1, width = RULES_WIDTH, height = RULE_HEIGHT)
    axiomFrame.grid(row = 2, column = 0, sticky = W+E)
    axiomFrame.grid_propagate(0)

    axLab = Label(axiomFrame, text="axiom : ")
    axLab.pack(side=LEFT)

    axStr = StringVar()
    axStr.trace("w", lambda name, index, mode, axStr=axStr: setRule("", axStr))
    axIn = Entry(axiomFrame, width = RULES_WIDTH, textvariable=axStr)
    axIn.pack(side=RIGHT, pady=5)
    axStr.set("-a")
    setRule("", axStr)
    
def makeIgnore():
    ignoreFrame = Frame(rules, highlightbackground="black", highlightthickness=1, width = RULES_WIDTH, height = RULE_HEIGHT)
    ignoreFrame.grid(row = 3, column = 0, sticky = W+E)
    ignoreFrame.grid_propagate(0)

    igLab = Label(ignoreFrame, text="ignore vars : ")
    igLab.pack(side=LEFT)

    igStr = StringVar()
    igStr.trace("w", lambda name, index, mode, igStr=igStr: setIgnoreVars(igStr))
    igIn = Entry(ignoreFrame, width = RULES_WIDTH, textvariable=igStr)
    igIn.pack(side=RIGHT, pady=5)
    igStr.set(NO_ACTION_VARS)
    setIgnoreVars(igStr)
    
def makeAngle():
    angleFrame = Frame(rules, highlightbackground="black", highlightthickness=1, width = RULES_WIDTH, height = RULE_HEIGHT)
    angleFrame.grid(row = 4, column = 0, sticky = W+E)
    angleFrame.grid_propagate(0)

    angLab = Label(angleFrame, text="angle : ")
    angLab.pack(side=LEFT)

    angStr = StringVar()
    angStr.trace("w", lambda name, index, mode, angStr=angStr: setAngle(angStr))
    angIn = Entry(angleFrame, width = RULES_WIDTH, textvariable=angStr)
    angIn.pack(side=RIGHT, pady=5)
    angStr.set(ANGLE)
    setAngle(angStr)
    
def makeIterations():
    interationsFrame = Frame(rules, highlightbackground="black", highlightthickness=1, width = RULES_WIDTH, height = RULE_HEIGHT)
    interationsFrame.grid(row = 5, column = 0, sticky = W+E)
    interationsFrame.grid_propagate(0)

    intLab = Label(interationsFrame, text="interations : ")
    intLab.pack(side=LEFT)

    intStr = StringVar()
    intStr.trace("w", lambda name, index, mode, intStr=intStr: setIterations(intStr))
    intIn = Entry(interationsFrame, width = RULES_WIDTH, textvariable=intStr)
    intIn.pack(side=RIGHT, pady=5)
    intStr.set(ITERATIONS)
    setIterations(intStr)
    
def makeLength():
    lineLengthFrame = Frame(rules, highlightbackground="black", highlightthickness=1, width = RULES_WIDTH, height = RULE_HEIGHT)
    lineLengthFrame.grid(row = 6, column = 0, sticky = W+E)
    lineLengthFrame.grid_propagate(0)

    lenLab = Label(lineLengthFrame, text="line Length : ")
    lenLab.pack(side=LEFT)

    lenStr = StringVar()
    lenStr.trace("w", lambda name, index, mode, lenStr=lenStr: setLength(lenStr))
    lenIn = Entry(lineLengthFrame, width = RULES_WIDTH, textvariable=lenStr)
    lenIn.pack(side=RIGHT, pady=5)
    lenStr.set(LENGTH)
    setLength(lenStr)


"""
create top level tkinter widgets and instruction box
"""
def main():
    global fractal
    global rules
    window = Tk()
    window.title("Lindenmayer Fractal Generator")
    window.geometry("1300x800")

    rulesFrame = Frame(window, bg = "light grey", height = 800, width = RULES_WIDTH)
    rulesFrame.grid(row = 0, column = 0, sticky = W+N+S)
    rulesFrame.grid_propagate(0)

    rulesCanvas = Canvas(rulesFrame, width = RULES_WIDTH)
    scrollbar = Scrollbar(rulesFrame, orient="vertical", command=rulesCanvas.yview)

    rules = Frame(rulesCanvas, bg = "light grey", width = RULES_WIDTH)
    rules.bind("<Configure>", lambda event: rulesCanvas.configure(scrollregion=rulesCanvas.bbox("all")))
    rulesCanvas.create_window((0,0), window=rules, anchor=N+W)
    rulesCanvas.configure(yscrollcommand=scrollbar.set)
    rulesCanvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")


    fractal = Canvas(window)
    fractal.grid(row = 0, column = 1, sticky=W+N+E+S)

    window.rowconfigure(0, weight=1)
    window.columnconfigure(1, weight=1)


    makeButtons()
    makeAxiom()
    makeIgnore()
    makeAngle()
    makeIterations()
    makeLength()
    newRule()
    drawFractal()

    """
    instructions window
    """
    instructions = Tk()
    instructions.title("Instructions")
    instructions.geometry("400x190")

    lineOne = Label(instructions, text="axiom is the starting rule", justify="left")
    lineOne.grid(row=0, column=0)
    lineTwo = Label(instructions, text="ignore vars are vars to draw a transparent line for")
    lineTwo.grid(row=1, column=0)
    lineThree = Label(instructions, text="angle is the angle to turn when a + or - is found")
    lineThree.grid(row=2, column=0)
    lineFour = Label(instructions, text="- turns right + turns left.")
    lineFour.grid(row=3, column=0)
    lineFive = Label(instructions, text="[ logs current location and angle.")
    lineFive.grid(row=4, column=0)
    lineSix = Label(instructions, text="] returns to last logged location and angle")
    lineSix.grid(row=5, column=0)
    lineSeven = Label(instructions, text="iterations is the number times replacments are done on the starting axiom")
    lineSeven.grid(row=6, column=0)
    close = Button(instructions, text="  OK  ", command=instructions.destroy)
    close.grid(row=7, column=0, pady=5)


    mainloop()

if __name__ == '__main__':
    main()




