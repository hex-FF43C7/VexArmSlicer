# import image_converter.py
from shapes import *

def main():
    arm = ArmSlicer()

    shape_commands = []

    DRAW_HEIGHT = 0
    TRAVEL_HEIGHT = 30
    
    arm.set_end_effector_type(arm.PEN)
    
    orig = [50, 180, DRAW_HEIGHT]
    for distance in range(20, 90, 10):
        shape_commands.append(TravelSafe(
            shape=Rectangle(arm, [orig[0], orig[1], DRAW_HEIGHT], [orig[0]+distance*2, orig[1]-distance, DRAW_HEIGHT]), 
            draw_h=DRAW_HEIGHT,
            travel_h=TRAVEL_HEIGHT,
        ))
    
    
    for command in shape_commands:
        command.do_shape()
        
    # print(arm.gcode)
    with open("end.txt", "w") as file:
        print(arm.get_gcode_commands(write_to_file=file))


# cte.cte_thread(main)
if __name__ == "__main__":
  main()
  