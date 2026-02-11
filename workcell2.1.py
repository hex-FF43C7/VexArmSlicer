# import image_converter.py
from shapes import *
import json

def main():
    arm = ArmSlicer()

    shape_commands = []

    DRAW_HEIGHT = 0
    TRAVEL_HEIGHT = 200
    
    arm.set_end_effector_type(arm.MAGNET)
    
    with open("worksetup2.1.txt", 'r') as file:
        json_commands = json.loads(file.read())
    
    
    for command in json_commands['Commands']: #tx-ty-tz:dx-dy-dz
        split_bits = [i.split('-') for i in command.split(':')]
        if len(split_bits) == 2:
            shape_commands.append(MoveBlock(
                    arm, 
                    box_start=[int(split_bits[0][0]), int(split_bits[0][1]), int(split_bits[0][2])],
                    box_end=[int(split_bits[1][0]), int(split_bits[1][1]), int(split_bits[1][2])],
                    travel_h = int(json_commands['Travel_Height'])
                )
            )
        else: #tx-ty-tz:dx-dy-dz:sl:bh
            shape_commands.append(MoveStack(
                    arm, 
                    top_block=[int(split_bits[0][0]), int(split_bits[0][1]), int(split_bits[0][2])],
                    block_destiation=[int(split_bits[1][0]), int(split_bits[1][1]), int(split_bits[1][2])],
                    travel_h=int(json_commands['Travel_Height']),
                    stack_length=int(split_bits[3][0]),
                    block_height=int(split_bits[2][0])
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