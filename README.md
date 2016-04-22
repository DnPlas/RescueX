# RescueX
This repository contains code for a rescue robot (driven by a Raspberry Pi 3 B), which is inteded to rescue a person in spaces with different obstacles:
- Altitude obstacle. To rescue a person standing on the edge of a 30 cm and 50 cm shelf.
- Muddy inclined plane. To rescue a person in a simulated cliff.

#Instructions to execute this code

1. On a Linux machine (different from the RPi): Connect to RPi through SSH:
   ssh pi@10.43.26.17
   Password: tallervertical
   
   If the IP has changed, you have to look at it connecting the RPi to an HDMI
   monitor

2. Once logged in the RPi, run the command:
   sudo systemctl start vncserver-x11-serviced.service

3. On Linux machine: 
   Go to Start > VNC Viewer > Connect
   If it doesn't let you connect to your RPi, make sure you have the right IP.
   Once it is started, it'll ask you for a password: taller.
   A window will show you the RPi desktop.

4. From the VNC window, open two terminals

5. In one terminal write:
   cd Rescuex/
   python rescuex.py

   This will start the program to run the motors and servos. Remember you have
   to turn on the PS3 controller. Now you'll be able to control the robot.

6. In other terminal write:
   python video.py

   Now you'll be able to watch the camera streaming in a new generated window. 
