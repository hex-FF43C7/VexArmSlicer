# import image_converter.py
from shapes import *

def main():
    arm = ArmSlicer()

    shape_commands = []

    DRAW_HEIGHT = 0
    TRAVEL_HEIGHT = 200
    
    arm.set_end_effector_type(arm.MAGNET)
    
    shape_commands.append(MoveBlock(
            arm, 
            box_start=[120, 120, 30],
            box_end=[70, 70, 30],
            travel_h = TRAVEL_HEIGHT
        )
    )
    
    
    
    for command in shape_commands:
        command.do_shape()
        
    # print(arm.gcode)
    with open("end.txt", "w") as file:
        print(arm.get_gcode_commands(write_to_file=file))


# cte.cte_thread(main)
if __name__ == "__main__":
  main()