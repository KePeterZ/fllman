from ev3dev2.display import Display
from ev3dev2.button import Button
import ev3dev2.fonts as fonts
import time, sys
screen = Display()
button = Button()

# Config
config = {
  "gyroPort": "in4",
  "robotName": "littleSapper",
  "runFiles": [
    "run1.py",
    "run2.py",
    "run3.py",
    "run4.py"
  ]
}

# Define myRobot
from imagine import myRobot
k = myRobot("outB", "outC", "outD", "out4")

screen.draw.rectangle((1,1,177,127))
screen.text_pixels("Waiting", clear_screen=False, x=10, y=10, font=fonts.load("charB24"))

screen.update()
currentProgram = 0
run = ""
programs = config["runFiles"]

def c(plus):
  global currentProgram
  global run
  bt = button.buttons_pressed
  if "left" in bt or "right" in bt or "enter" in bt:
    if type(plus)==type(2):
      if plus>0:
        currentProgram += 1
      else:
        currentProgram -= 1
    elif type(plus)==type("hello"):
      run = plus

button.on_right = lambda x : c(1)
button.on_left = lambda x : c(-1)
button.on_enter = lambda x : c("run1.py")

while True:
  program = currentProgram
  button.process()
  if run != "" and run != "stopped":
    screen.clear()
    screen.draw.rectangle((1,1,177,127))
    screen.text_pixels("Running:", clear_screen=False, x=30, y=78, font=fonts.load("charB24"))
    screen.text_grid(programs[currentProgram%len(programs)], clear_screen=False, x=7, y=10.3, font=fonts.load("helvB18"))
    screen.update()
    # Run code here
    time.sleep(2)
    run = "stopped"
  if program != currentProgram or run == "stopped":
    screen.clear()
    screen.draw.rectangle((1,1,177,127))
    screen.text_pixels("Selected:", clear_screen=False, x=30, y=78, font=fonts.load("charB24"))
    screen.text_grid(programs[currentProgram%len(programs)], clear_screen=False, x=7, y=10.3, font=fonts.load("helvB18"))
    screen.update()
