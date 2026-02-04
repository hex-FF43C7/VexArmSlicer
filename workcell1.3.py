# import image_converter.py
from shapes import *

def main():
    arm = ArmSlicer()

    shape_commands = []

    DRAW_HEIGHT = 0
    TRAVEL_HEIGHT = 30
    
    arm.set_end_effector_type(arm.PEN)
    
    shape_commands.append(TravelSafe(
        shape=Circle(arm, [130, 145, DRAW_HEIGHT], 40), 
        draw_h=DRAW_HEIGHT,
        travel_h=TRAVEL_HEIGHT,
    ))

    shape_commands.append(TravelSafe(
        shape=Rectangle(arm, [155, 123, DRAW_HEIGHT], [140, 170, DRAW_HEIGHT]), 
        draw_h=DRAW_HEIGHT,
        travel_h=TRAVEL_HEIGHT,
    ))

    shape_commands.append(TravelSafe(
        shape=Circle(arm, [120, 130, DRAW_HEIGHT], 5), 
        draw_h=DRAW_HEIGHT,
        travel_h=TRAVEL_HEIGHT,
    ))
    
    shape_commands.append(TravelSafe(
        shape=Circle(arm, [120, 165, DRAW_HEIGHT], 5), 
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