# import image_converter.py
from shapes import *
import json

def main():
    arm = ArmSlicer()

    shape_commands = []

    DRAW_HEIGHT = 0
    TRAVEL_HEIGHT = 200
    
    arm.set_end_effector_type(arm.MAGNET)
    
    # shape_commands.append(MoveBlock(
    #         arm, 
    #         box_start=[120, 120, 30],
    #         box_end=[70, 70, 30],
    #         travel_h = TRAVEL_HEIGHT
    #     )
    # )
    
    with open("worksetup2.1.txt", 'r') as file:
        json_commands = json.loads(file.read())
    
    for command in json_commands['Commands']
        split_bits = [i.split('-') for i in command.split(':')]
        shape_commands.append(MoveBlock(
                arm, 
                box_start=[split_bits[0][0], split_bits[0][1], split_bits[0][2]],
                box_end=[split_bits[1][0], split_bits[1][1], split_bits[1][2]],
                travel_h = json_commands['Travel_Height']
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