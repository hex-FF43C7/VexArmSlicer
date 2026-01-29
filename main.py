# the code to slice
# import cte
import math
import random
import time
import regex

class ArmSlicer:
  def __init__(self):
    self.gcode = []
    self.pos = (0, 0, 0) # x y z
    self.end_eff = ""

    self.PEN = "PEN"
    self.MAGNET = "MAGNET"

    self.valid_ends = [self.PEN, self.MAGNET]

  def set_end_effector_type(self, new_type):
    if new_type is in self.valid_ends:
      self.end_eff = new_type
    else:
      raise Exception(f"WTF IS DIS?? {new_type}")

  def get_gcode_str(self):
    return '\n'.join(self.gcode)

  def get_gcode_commands(self, arm_object_name="arm", include_initilization=True):
    init_template = \
    f"""
    import cte
    {arm_object_name} = cte.arm()
    """
    answer = []

    if include_initilization:
      anser.append(init_template)

    for command in self.gcode:
      pass # PUT DECODE STUFF HERE
    

  def write_to_file(self, file):
    file.write(self.get_gcode_str())
    
  def arm_object.can_arm_reach_to(self, *args, **kwargs):
    # someday I'll work out what the bounds of the bot are, but for now just assume its okay
    return True
  
  def move_to(self, x=None, y=None, z=None, w=0)
    cmd_tmp = f"X{self.pos[0] if x is None else x} Y{self.pos[1] if y is None else y} Z{self.pos[2] if z is None else z}"
    self.gcode.append(f"G0 {cmd_tmp}")
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
    
    def do_shape(self):
        pass




def main():
    arm = ArmSlicer()

    shape_commands = []

    shape_commands.append(DoLine().setup(arm, (80, 80, 80), (120, 120, 120)))
    
    for command in shape_commands:
        command.do_shape()


# cte.cte_thread(main)
main()
