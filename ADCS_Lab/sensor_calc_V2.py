"""
The code you will write for this module should calculate
roll, pitch, and yaw (RPY) and calibrate your measurements
for better accuracy. Your functions are split into two activities.
The first is basic RPY from the accelerometer and magnetometer. The
second is RPY using the gyroscope. Finally, write the calibration functions.
Run plot.py to test your functions, this is important because auto_camera.py 
relies on your sensor functions here.
"""

#import libraries
#import libraries                                                                    
import time                                                                          
import numpy as np                                                                   
import time                                                                          
import os                                                                            
import board                                                                         
import busio                                                                         
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS                              
from adafruit_lis3mdl import LIS3MDL                                                 

#imu initialization                                                                  
i2c = busio.I2C(board.SCL, board.SDA)                                                
accel_gyro = LSM6DS(i2c)                                                             
mag = LIS3MDL(i2c)                                                                   


#Activity 1: RPY based on accelerometer and magnetometer                             
def roll_am(accelX,accelY,accelZ):                                                   
    roll = np.arctan(accelY / (np.sqrt(np.square(accelX) + np.square(accelZ))))      
    return 180 / np.pi * roll                                                        

def pitch_am(accelX,accelY,accelZ):                                                  
    pitch = np.arctan(accelX / (np.sqrt(np.square(accelY) + np.square(accelZ))))     
    return 180 / np.pi * pitch                                                       

def yaw_am(accelX,accelY,accelZ,magX,magY,magZ):                                     
    mag_x = magX * np.cos(pitch_am(accelX, accelY, accelZ)) + magY * np.sin(pitch_am(accelX, accelY, accelZ)) * np.sin(roll_am(accelX, accelY, accelZ)) + magZ * np.cos(roll_am(accelX, accelY, accelZ)) * np.sin(pitch_am(accelX, accelY, accelZ))                                                                                  
    mag_y = magY * np.cos(roll_am(accelX, accelY, accelZ)) - magZ * np.sin(roll_am(accelX, accelY, accelZ))                                                          
    return (180/np.pi)*np.arctan2(-mag_y, mag_x)                                     

#Activity 2: RPY based on gyroscope                                                  
def roll_gy(prev_angle, delT, gyro):                                                 
    roll = prev_angle + delT * gyro                                                  
    return roll                                                                      
def pitch_gy(prev_angle, delT, gyro):
    pitch = prev_angle + delT * gyro
    return pitch
def yaw_gy(prev_angle, delT, gyro):
    yaw = prev_angle + delT * gyro
    return yaw

#Activity 3: Sensor calibration
def calibrate_mag():
    x = []
    y = []
    z = []
    print("Preparing to calibrate magnetometer. Please wave around.")
    for i in range (1000):
        x1, y1, z1 = mag.magnetic
        x.append(x1)
        y.append(y1)
        z.append(z1)
    time.sleep(3)
    print("Calibrating...")
    av = [(max(x) + min(x)) / 2, (max(y) + min(y)) / 2, (max(z) + min(z)) / 2]
    print("Calibration complete.")
    return av

def calibrate_gyro():
    x = []
    y = []
    z = []
    print("Preparing to calibrate gyroscope. Put down the board and do not touch it.")
    time.sleep(3)
    print("Calibrating...")
    for i in range (1000):
        x1, y1, z1 = accel_gyro.acceleration
        x.append(x1)
        y.append(y1)
        z.append(z1)
    av = [(max(x) + min(x)) / 2, (max(y) + min(y)) / 2, (max(z) + min(z)) / 2]
    print("Calibration complete.")
    return av

def set_initial(mag_offset):
    """
    This function is complete. Finds initial RPY values.

    Parameters:
        mag_offset (list): magnetometer calibration offsets
    """
    #Sets the initial position for plotting and gyro calculations.
    print("Preparing to set initial angle. Please hold the IMU still.")
    time.sleep(3)
    print("Setting angle...")
    accelX, accelY, accelZ = accel_gyro.acceleration #m/s^2
    magX, magY, magZ = mag.magnetic #gauss
    #Calibrate magnetometer readings. Defaults to zero until you
    #write the code
    magX = magX - mag_offset[0]
    magY = magY - mag_offset[1]
    magZ = magZ - mag_offset[2]
    roll = roll_am(accelX, accelY,accelZ)
    pitch = pitch_am(accelX,accelY,accelZ)
    yaw = yaw_am(accelX,accelY,accelZ,magX,magY,magZ)
    print("Initial angle set.")
    return [roll,pitch,yaw]