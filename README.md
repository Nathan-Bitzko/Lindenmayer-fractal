# Lindenmayer-fractal
python program to generate Lindenmayer fractals

ToDo - add loading bar, big fractals can take a while to generate with no indication that it is happening to the user
     - create fractal pre sets and allow them to be loaded into the program on user request
     - allow user saving of fractal settings


axiom is the starting rule. ignore vars are vars to draw a transparent line for angle is 
the angle to turn when a + or - is found. - turns right + turns left. "[" logs current 
location and angle and "]" returns to last logged location. iterations is the number times 
replacments are done on the starting axiom

for those theoretical computer scientists out there, the fractal is contructed from a series 
of rules that make up a context free grammar.

see wiki page https://en.wikipedia.org/wiki/L-system
for more information on lindenmayer fractals
