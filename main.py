# the code to slice
import cte
import math
import random
import time

class Arm_Slicer:
  def __init__(self):
    self.gcode = []

  def get_gcode_str(self):
    return '\n'.join(self.gcode)

  def write_to_file(self, file):
    file.write(self.get_gcode_str())
    
  def arm_object.can_arm_reach_to(self, *args, **kwargs):
    # someday I'll work out what the bounds of the bot are, but for now just assume its okay
    return True
  
  def move_to(self, x, y, z, w=0)
    self.gcode.append(f"G0 X{x} Y{y} Z{z}")
    if w != 0:
      self.gcode.append(f"G4 {w.upper()}")

class DoLine:
    def setup(self, arm_object, start_point, stop_point) -> None:
        self.start_p = start_point
        self.stop_p = stop_point

        self.arm_object = arm_object
        self.arm_object.set_end_effector_type(self.arm_object.PEN)

        if not self.arm_object.can_arm_reach_to(*self.start_p):
            raise Exception(f'cant reach start point {self.start_p}')

        if not self.arm_object.can_arm_reach_to(*self.stop_p):
            raise Exception(f'cant reach end point {self.start_p}')
        return self

    def do_shape(self):
        self.arm_object.move_to(*self.start_p)
        self.arm_object.move_to(*self.stop_p)



class Circle:
    def __init__(self, arm, origin, radius, plane="z", slice_start=0, slice_end=360):
        self.arm = arm
        self.arm.set_end_effector_type(self.arm.PEN)

        self.origin = origin
        self.radius = radius
        self.plane = plane
        self.slice_start = slice_start
        self.slice_end = slice_end
    
    def do(self):
        pass




def main():
    arm = 

    cte.wait(100, cte.MSEC)

    shape_commands = []

    shape_commands.append(DoLine().setup(arm, (80, 80, 80), (120, 120, 120)))
    
    for command in shape_commands:
        command.do_shape()


cte.cte_thread(main)
