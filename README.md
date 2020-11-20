# Simple3dPrint
Simple 3d printer control host application

This application allows the user to send gcode files to a 3d printer for printing.
the initial feature set includes:
1. Sending a file to the printer's SD card with or without printing it
2. Start a print from a gcode file on the printe'r SD card
3. Printing a gcode file directly to a 3d printer 
4. support 3d printers with Marlin firmware variety
5. multiple instances can run simultanously to control several 3d printer in the same time

The application meant to be "simple" so (initially at least) there is no plan to have any fancy graphic for disaplyig the model or manually control the printer. There is no reason to do that anyway if the gcode was generated with a slicer that configured correctly.

the application is written in python 3.x with optionally a TK/Inter GUI interface

