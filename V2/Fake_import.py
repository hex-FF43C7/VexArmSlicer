"""
This file pretends to be multible files to make it runable in test environments,
but it is actually just one file with fake imports and fake classes to make the code run without the actual hardware libraries. 
The real code is in chips.py, but this file allows us to run the code on a computer without the robot hardware. 
The fake classes and imports are just placeholders and do not have any functionality. 
They are only here to allow the code to run without errors in a test environment.

specifically, it emulates "vex" and "cte" imports, 
as well as some classes and constants that are used in the code but are not defined in the test environment.
"""

class Color:
    RED = 0
    GREEN = 1
    BLUE = 2
    WHITE = 3
    YELLOW = 4
    ORANGE = 5
    PURPLE = 6
    CYAN = 7
    BLACK = 8

class wait:
    def __init__(self, time, unit):
        pass

class LedStateType:
    ON = 0
    OFF = 1

class Ports:
    PORT1 = 0
    PORT2 = 1
    PORT3 = 2
    PORT4 = 3
    PORT5 = 4
    PORT6 = 5
    PORT7 = 6
    PORT8 = 7
    PORT9 = 8
    PORT10 = 9

class Brain:
    def __init__(self):
        self.screen = self.Screen()
    
    class Screen:
        def set_cursor(self, x, y):
            pass
        
        def clear_row(self, row):
            pass
        
        def print(self, msg):
            print(msg)




SECONDS = 0
MSEC = 1
PERCENT = 0

XAXIS = 0
YAXIS = 1
ZAXIS = 2

class SignalTower:
    ALL = 1
    GREEN = 2
    YELLOW = 3
    RED = 4

    def __init__(self, port):
        pass
    
    def on(self, color):
        pass
    
    def off(self):
        pass

class Inertial:
    def __init__(self):
        pass
    
    def get_rotation(self):
        return 0
    
class Optical:
    def __init__(self, port):
        pass
    
    def get_color(self):
        return Color.RED
    
class Arm:
    def __init__(self, port):
        pass

    def move_to(self, position):
        pass

