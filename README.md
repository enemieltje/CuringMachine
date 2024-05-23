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

This leaves the following subsystems for this program:

- Driving the stepper motors
- Driving the camera
- Handling the input buttons
- Driving the lcd
- Parsing input to a menu
- Managing parameter saving and editing
- Managing data saving
- Managing data exporting
- Handling sequences of output

## Machine startup
When the raspberry pi boots, it will try to run the program. This will display its current ip address and port on the lcd screen. as \[ip\]:\[port\]
To see the logs of the program, one can connect to the raspberry via ssh. This can be done using the following command:
ssh curing@\[ip\]
Note that this command does not include the port displayed on the lcd screen.

When connected using ssh, the program can started and stopped in the background using the following commands:
sudo systemctl start curingmachine.service
sudo systemctl stop curingmachine.service

To see the logs and error messages of the program it needs to be started manually using the following command:
sudo ./startCuringMachine.sh
The program can then be interrupted using ctrl + C.

Once the program is running, the website may be visited to control the machine. This can be done by typing \[ip\]:\[port\] into a browser. Adding a slash at the end may be required to stop the browser from googling the address instead of opening the site.
