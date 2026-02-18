# Auto 1.1
#region VEXcode Generated Robot Configuration
from vex import *
from cte import *
import urandom
import math

# Brain should be defined by default
brain = Brain()

# Robot configuration code
brain_inertial = Inertial()
arm1 = Arm(Ports.PORT1)


# Wait for sensor(s) to fully initialize
wait(100, MSEC)

# generating and setting random seed
def initializeRandomSeed():
    wait(100, MSEC)
    xaxis = brain_inertial.acceleration(XAXIS) * 1000
    yaxis = brain_inertial.acceleration(YAXIS) * 1000
    zaxis = brain_inertial.acceleration(ZAXIS) * 1000
    systemTime = brain.timer.system() * 100
    urandom.seed(int(xaxis + yaxis + zaxis + systemTime)) 

# Initialize random seed 
initializeRandomSeed()

# Initialize the 6-Axis Arm
arm1.initialize_arm()

#endregion VEXcode Generated Robot Configuration
from vex import *
arm1
#arm imported.

#This code, when started, has the purpose of;
#1: Picking up a disk.
#And 2: Placing the disk on a pallet.

arm1.set_end_effector_type(arm1.MAGNET)
arm1.move_to(150, 40, 30)
arm1.set_end_effector_magnet(True)
#activating the magnet & orienting the arm to the correct position.

arm1.move_inc(0, 0, 50)
#setting the Z axis to 50 in order to lift the disk.

arm1.move_to(150, 150, 85)
#moving the arm to the second location to place down the disk.
arm1.move_inc(0, 0, -50)
#inverting reality
arm1.set_end_effector_magnet(False)
#deactivating the magnet.
