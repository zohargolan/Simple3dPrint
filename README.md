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

the application is written in python 3.x with optionally a TK/Inter GUI interface (as a future improvement)

Command line parameters
Simple3dPrint comPort [-SL] [-SU] [-SUP] [-SP] [-P] [<sourceFilename>] [<destFilename8.3>]

comPort           The serial communication port name (COMx for windows)
sourceFilenae     source gcode filename on the host PC
destFilename8.3   Destination gcode filename in 8.3 format
-SL               SD card list
-SU               SD card upload
-SUP              SD card upload and print
-SP               SD card print only
-P                direct print through serial port

Examples:
Simple3dPrint COM5 -SL                                  
- prints the list of gcode files in the printer's SD card

Simple3dPrint COM5 -SU test_Model_1234.gcode            
- Upload a file test_Model_1234.gcode to the printer's SD card to destination filename model.gco

Simple3dPrint COM5 -SU test_Model_1234.gcode test.gco          
- Upload a file test_Model_1234.gcode to the printer's SD card to destination filename test.gco (Note: destination filename must be in 8.3 format)

Simple3dPrint COM5 -SUP test_Model_1234.gcode test.gco          
- Upload a file test_Model_1234.gcode to the printer's SD card to destination filename test.gco (Note: destination filename must be in 8.3 format) and then start the print from   the printer's SD card and exit. The printer continue the print without host intervention.

Simple3dPrint COM5 -SP test.gco          
- Start a print of a file test.gco which is already located in the the printer's SD card (Note: filename must be in 8.3 format). The printer continue the print without host intervention.

Simple3dPrint COM5 -P test_Model_1234.gcode            
- Start a print of a file test_Model_1234.gcode which is on the host PC directly controlling the printer via the serial pocommunication port.






