# Curing Machine

## Machine Contents

This code will run on a raspberry pi, and operate a curing machine. This machine will consist of the following components:

- A belt driven by two stepper motors.
- Five physical input buttons
- A 4x20 lcd screen
- Two load cells
- Two Raspberry Pi Cameras

## Machine capabilities 

The machine will display a menu on the lcd screen, which can be navigated with the input buttons. This menu will allow the user to start the following operations:

- Configuring the speed of the belt 
- Manually turning the belt
- Manually take a picture
- Export saved data over usb
- Export saved data over different methods
- Starting the belt continuously
- Starting one cycle of the curing machine
- Starting repeated production with the curing machine
- Configuring any additional parameters 


This leavee the following subsystems for this program:

- Driving the stepper motors
- Driving the camera
- Handling the input buttons
- Driving the lcd 
- Parsing input to a menu
- Managing parameter saving and editing
- Managing data saving
- Managing data exporting
- Handling sequences of output 