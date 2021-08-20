# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 19:10:21 2021

@author: iambe
"""
class Values:
    
    def __init__(self, startAngle, rotAngle, x, y, its, noAction, length):
        self.rules = dict()
        self.rules["startAngle"] = startAngle
        self.rules["startX"] = x
        self.rules["startY"] = y
    
    def setRule(self, var, rule):
        self.rules[var] = rule
    
    def setIterations(self, its):
        self.rules["iterations"] = its
        
    def setNoActionVars(self, variables):
        self.rules["noActionVars"] = variables
        
    def setLength(self, length):
        self.rules["length"] = length
        
    def setAngle(self, newAngle):
        self.rules["angle"] = newAngle
        
    def getRules(self):
        return self.rules
        
