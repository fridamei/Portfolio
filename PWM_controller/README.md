# PWM-control of motor

## Description
IP module that compromise the speed regulator for a motor. <br>
The module is part of a larger SoC project, where the speed of the motor is then encoded using a quadrature encoder, decoded using a quadrature decoder and read as velocity given the increment/decrement signals. The velocities are further displayed on a seven segment display. 

## Dependencies
IEEE

## Functionality
The system consists of a self test module that provide 20 different values which are displayed for 3 seconds each. The values 
are stored in a ROM after being read from a separate text file (ROM_data.txt) during synthesis (to easier change values when testing the system).
These values are fed into a Pulse Width Modulator (PWM), which modulate the signal, and thereby the speed of the motor, according to the 
the value (where 128 is full speed, 64 is half speed, -127 is full speed reverse and so on). 
The signal is fed through an output synchronizer because the data is read outside the clock domain and read asynchronous data
(input from external sources may change at random and create metastability and unpredictable behaviours in registers, and the output may be the souce of glitches. Synchronization takes care of these two hazards).
The synchronized input (coming from a quadrature encoder) is fed through a quadrature decoder.
The quadrature decoder provides increment/decrement signals which are fed to a velocity reader (pre-written) which then is fed to a 7 segment display. 
