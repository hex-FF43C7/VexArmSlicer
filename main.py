# the code to slice
# import cte
import math
import random
import time
# import regex

class ArmSlicer:
  def __init__(self):
    self.gcode = []
    self.pos = [0, 0, 0] # x y z
    self.end_eff = ""

    self.PEN = "PEN"
    self.MAGNET = "MAGNET"

    self.valid_ends = [self.PEN, self.MAGNET]

  def set_end_effector_type(self, new_type):
    if new_type in self.valid_ends:
      self.gcode.append(f'EFF {new_type}')
      self.end_eff = new_type
    else:
      raise Exception(f"WTF IS DIS?? {new_type}")

  def get_gcode_str(self):
    return '\n'.join(self.gcode)

  def get_gcode_commands(self, arm_object_name="arm", include_initilization=True, write_to_file=None):
    init_template = \
f"""import cte
import time
{arm_object_name} = cte.Arm()
cte.wait(1, cte.SECONDS)
"""
    answer = []

    if include_initilization:
      answer.append(init_template)

    # DECODE START
    for line, command in enumerate(self.gcode):
      if command.strip() == '':
        continue
      sub_commands = command.strip().split(' ')
      if len(sub_commands) <= 1:
        continue
      # DECODE LINE
      match sub_commands[0]:
        case 'G0':
          end_loc = dict()
          for set_axis in sub_commands[1::]:
            if set_axis[0].upper() in ("X", "Y", "Z"):
              end_loc[set_axis[0]] = int(set_axis[1::])
            else:
              raise Exception(f'Unknown component on line {line+1}, "{set_axis}"')
          
          answer.append(f"{arm_object_name}.move_to(x={end_loc['X']}, y={end_loc['Y']}, z={end_loc['Z']})")
        case 'G4':
          if len(sub_commands) != 2:
            raise Exception(f'error on line {line+1}, G4 takes one argument, "{command.strip()}"')
          else:
            match sub_commands[1][0]:
              case 'S':
                answer.append(f"time.sleep({sub_commands[1][1::]})")
              case _:
                raise Exception(f'unsuported at the moment "{sub_commands[1][0]}" in "{command}" on line {line}')
                
        case 'EFF':
          answer.append(f"{arm_object_name}.set_end_effector_type({arm_object_name}.{sub_commands[-1]})")
        case _:
          raise Exception(f'unknown gcode cmd "{sub_commands} on line {line+1}"')

    text = '\n'.join(answer)
    if not write_to_file is None:
      write_to_file.write(text)
    return text

  def write_to_file(self, file):
    file.write(self.get_gcode_str())
    
  def can_arm_reach_to(self, *args, **kwargs):
    # someday I'll work out what the bounds of the bot are, but for now just assume its okay
    return True
  
  def move_to(self, x=None, y=None, z=None, w=0):

    new_pos = [(self.pos[0] if x is None else x), (self.pos[1] if y is None else y), (self.pos[2] if z is None else z)]
    self.pos = new_pos

    cmd_tmp = f"X{new_pos[0]} Y{new_pos[1]} Z{new_pos[2]}"
    
    self.gcode.append(f"G0 {cmd_tmp}")
    if w != 0:
      self.gcode.append(f"G4 {w.upper()}")

class DoLine:
    def __init__(self, arm_object, start_point, stop_point) -> None:
        self.start_p = start_point
        self.stop_p = stop_point

        self.arm_object = arm_object
        # self.arm_object.set_end_effector_type(self.arm_object.PEN)

        if not self.arm_object.can_arm_reach_to(*self.start_p):
            raise Exception(f'cant reach start point {self.start_p}')

        if not self.arm_object.can_arm_reach_to(*self.stop_p):
            raise Exception(f'cant reach end point {self.start_p}')

    def do_shape(self):
        self.arm_object.move_to(*self.start_p)
        self.arm_object.move_to(*self.stop_p)



class Circle:
    def __init__(self, arm, origin, radius, resolution=30, plane="z", slice_start=0, slice_end=360):
        self.arm = arm
        # self.arm.set_end_effector_type(self.arm.PEN)

        self.origin = origin
        self.radius = radius
        self.resolution = resolution
        self.plane = plane
        self.slice_start = slice_start
        self.slice_end = slice_end
    
    def do_shape(self):
      points = []
      for i in range(self.resolution):
          # Calculate the angle for each point, evenly spaced
          angle = 2 * math.pi / self.resolution * i
          
          # Calculate coordinates using the parametric equations
          x = self.origin[0] + self.radius * math.cos(angle)
          y = self.origin[1] + self.radius * math.sin(angle)
          
          # points.append((x, y))
          self.arm.move_to(x=int(round(x)), y=int(round(y)), z=self.origin[2])




def main():
    arm = ArmSlicer()

    shape_commands = []
    
    arm.set_end_effector_type(arm.PEN)
    shape_commands.append(DoLine(arm, (135+30, 158, 30), (135+30, 158, 0)))
    shape_commands.append(Circle(arm, origin=(135, 158, 0), radius=30, resolution=60))
    shape_commands.append(DoLine(arm, (135+30, 158, 0), (135+30, 158, 40)))
    

    
    for command in shape_commands:
        command.do_shape()
        
    # print(arm.gcode)
    with open("end.txt", "w") as file:
        print(arm.get_gcode_commands(write_to_file=file))


# cte.cte_thread(main)
main()
