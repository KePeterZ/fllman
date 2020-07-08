#!/usr/bin/env micropython

# from ev3dev2.display import Display
# screen = Display()
# import ev3dev2.fonts as fonts
from ev3dev2.button import Button
from ev3dev2.console import Console
console = Console("Lat15-TerminusBold28x14.psf.gz")
print = console.text_at
import time, sys
button = Button()

# Config
config = {
  "gyroPort": "in4",
  "robotName": "littleSapper",
  "runFiles": [
    "run1",
    "run2",
    "run3",
    "run4"
  ]
}

# Define myRobot
from imagine import myRobot
# k = myRobot("outB", "outC", "outD", "out4")
k = myRobot()

# Define functions
def reimportModulesAndRun(runFile):
  try: 
    sys.modules.pop(runFile)
  except:
    pass
  try: 
    exec("from %s import %sdef" % (runFile, runFile))
    exec("%sdef(k)" % runFile)

  except:
    print("Can't!", 1, 2)

def clearColumn(colNum): 
  console.text_at("            ", 1, colNum)

currentProgram = 0
program = 1
run = ""
programs = config["runFiles"]


# Button handling
def c(plus):
  global currentProgram
  global program
  global run
  bt = button.buttons_pressed
  if "left" in bt or "right" in bt or "enter" in bt:
    if type(plus)==type(2):
      if plus>0:
        program += 1
      else:
        program -= 1
    elif type(plus)==type(True):
      run = currentProgram
    currentProgram = (program%len(programs))+1

button.on_right = lambda x : c(1)
button.on_left = lambda x : c(-1)
button.on_enter = lambda x : c(True)

# Program running handling
currentProgram = 1
pastProgram = currentProgram

console.reset_console()
console.text_at("Selected: " + str(currentProgram))

while True:
  button.process()
  if currentProgram != pastProgram:
    clearColumn(1)
    console.text_at("Selected: " + str(currentProgram))
  if run: 
    clearColumn(1)
    console.text_at("Running: " + str(currentProgram), 1, 1)
    console.text_at("            ", 1, 2)
    console.text_at("", 1, 2)
    # Running file here
    reimportModulesAndRun("run%i" % currentProgram)
    run = False
    # Running file ending here
    console.text_at("Selected: " + str(currentProgram))
  pastProgram = currentProgram
