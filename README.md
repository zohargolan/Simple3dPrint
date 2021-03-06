# Simple3dPrint
Simple 3d printer control host application

This application allows the user to send gcode files to a 3d printer for printing.
the initial feature set includes:
1. Sending a file to the printer's SD card with or without printing it
2. Starting a print from a gcode file on the printer's SD card
3. Printing a gcode file directly to a 3d printer 
4. Support for 3d printers with Marlin firmware variety
5. Multiple instances can run simultanously to control several 3d printers at the same time

The application is meant to be "simple" so (initially at least) there is no plan to have any fancy graphics for disaplying the model or manually controling the printer. There is no reason to do that anyway if the gcode was generated with a slicer that configured correctly.

The application is written in python 3.x with optionally a TK/Inter GUI (as a future improvement).

## Command line parameters
Simple3dPrint [comPort] [command] [< sourceFilename >] [< destFilename8.3 >]

| Parameter       | Description                                            |
| --------------- | ------------------------------------------------------ |
| comPort         | The serial communication port name (COMx for windows)  |
| sourceFilename  | Source gcode filename on the host PC                   |
| destFilename8.3 | Destination gcode filename **(must be in 8.3 format)** | 
| command         | The command to send to the printer                     |

### Commands
| Command  | Description                       |
| -------- | --------------------------------- |
| -SL      | SD card list                      |
| -SD      | SD card file delete               |
| -SU      | SD card upload                    |
| -SUP     | SD card upload and print          | 
| -SP      | SD card print only                |
| -P       | Direct print through serial port  |

#### SD Card List
Prints the list of gcode files in the printer's SD card.<br>
Ex: Simple3dPrint COM5 -SL

#### SD Card file delete
Delete a file from the printer's SD card.<br>
Ex: Simple3dPrint COM5 -SD test.gco

#### SD Card Upload
Uploads a file to the printer's SD card. It takes an optional destination filename. Not adding the destination filename will override the contents of model.gco with the new file.<br>
Ex: Simple3dPrint COM5 -SU test_Model_1234.gcode

Adding the optional destination filename will save the file to the destination file.<br>
Ex: Simple3dPrint COM5 -SU test_Model_1234.gcode test.gco

#### SD Card Upload and Print
Uploads a file to the printer's SD card to model.gco by default and the destination file if a filename is provided.
After upload it starts the print from the printer's SD card and exits, continuing the print without host intervention.<br>
Ex: Simple3dPrint COM5 -SUP test_Model_1234.gcode test.gco

#### SD Card Print Only
Starts a print of the provided file which is already located in the the printer's SD card.
The printer continues the print without host intervention.<br>
Ex: Simple3dPrint COM5 -SP test.gco

#### Direct Print Through Serial Port
Start a print of the source file which is on the host PC directly controlling the printer via the serial communication port.<br>
Ex: Simple3dPrint COM5 -P test_Model_1234.gcode
