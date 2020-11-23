import serial
import sys
import time


class Simple3dPrint:
    #Error code definition
    OK                                      = 0
    ERROR_OPEN_SERIAL_PORT                  = 1
    ERROR_CLOSE_SERIAL_PORT                 = 2
    ERROR_DEST_FILENAME_MORE_THAN_2_FIELDS  = 3
    ERROR_DEST_FILENAME_BASE_MORE_THAN_8    = 4
    ERROR_DEST_FILENAME_EXT_MORE_THAN_3     = 5
    ERROR_DEST_FILENAME_NOT_STRING          = 6
    ERROR_OPEN_SOURCE_FILE                  = 7
    ERROR_IN_SAVE_FILENAME_RESPONSE         = 8
    ERROR_IN_CLOSE_FILENAME_RESPONSE        = 9
    ERROR_OPEN_SD_CARD_FILE_FOR_PRINTING    = 10
    ERROR_DELETING_SD_CARD_FILE             = 11

    def __init__(self,comPort):
        self.comPort = comPort 

    def openComPort(self):
        try:
            self.ser = serial.Serial(self.comPort,baudrate=250000,timeout=0.5)
        except:
            return self.ERROR_OPEN_SERIAL_PORT

        return self.OK

    def check8_3_filename(self, filename):
        #Check validity of destination file
        try:
            if filename != "model.gco":
                filenameParts = filename.split(".")
                if len(filenameParts) > 2:
                    return self.ERROR_DEST_FILENAME_MORE_THAN_2_FIELDS
                elif len(filenameParts[0]) > 8:
                    return self.ERROR_DEST_FILENAME_BASE_MORE_THAN_8
                elif len(filenameParts[1]) > 3:
                    return self.ERROR_DEST_FILENAME_EXT_MORE_THAN_3
                else:
                    return self.OK
        except:
            return self.ERROR_DEST_FILENAME_NOT_STRING

    def sdList(self):
        #flush the serial port from boot data
        time.sleep(2)
        response = self.ser.read(1000)

        #send the dir command
        self.ser.write("M20\r".encode())
        response = self.ser.read(1000).decode() 
        responseLines = response.split("\n")
        for line in responseLines:
            if not line.startswith("Begin") and not line.startswith("End") and not line.startswith("ok"):
                print(line)
        return self.OK

    def DeleteSdFile(self, DestFilename):
        #Check validity of destination file
        error = self.check8_3_filename(DestFilename)
        if error != self.OK:
            return error

        #flush recieve buffer
        time.sleep(2)
        response = self.ser.read(20000).decode() 

        #Start the print
        self.ser.write(("M30 " + DestFilename + "\r").encode())
        response = self.ser.read(200).decode() 
        if "failed" in response.lower():
            return self.ERROR_DELETING_SD_CARD_FILE    
        
        return self.OK
    
    def UploadFile(self, SourceFileName, DestFilename="model.gco"):
        #Check validity of destination file
        error = self.check8_3_filename(DestFilename)
        if error != self.OK:
            return error

        #open source file
        try:
            f = open(SourceFileName)
        except:
            return self.ERROR_OPEN_SOURCE_FILE

        #read source file
        lines = f.readlines()

       
        #flush the serial port from boot data
        time.sleep(2)
        response = self.ser.read(1000)

        #Start the file save to filename model.gco
        self.ser.write(("M28 " + DestFilename + "\r").encode())
        response = self.ser.read(200).decode() 
        if not 'ok' in response:
            return self.ERROR_IN_SAVE_FILENAME_RESPONSE
            
        else:
            lineNumber = 0
            for line in lines:
                lineNumber += 1
                if line.startswith(';'):
                    continue
                if ";" in line:
                    line = line[:line.index(";")]
                    line += "\n"
                self.ser.write(line.encode())
                response = self.ser.read(3).decode() 

                progressBarValue = round(lineNumber/len(lines)*50)
                progressBar = '['
                for i in range(50):
                    if i < progressBarValue:
                        progressBar += "#"
                    else:
                        progressBar += " "
                progressBar += "]"
                
                print("\r",round(lineNumber/len(lines)*100),"% ",progressBar,lineNumber,"/",len(lines),end=''),
                

            #flush recieve buffer
            time.sleep(2)
            response = self.ser.read(20000).decode() 
            
            #Close the destination file
            self.ser.write("M29\n".encode())
            response = self.ser.read(200).decode() 
            
            if not 'Done' in response:
                return self.ERROR_IN_CLOSE_FILENAME_RESPONSE
            else:
                return self.OK


    def PrintSdFile(self, DestFilename):
        #Check validity of destination file
        error = self.check8_3_filename(DestFilename)
        if error != self.OK:
            return error

        #flush recieve buffer
        time.sleep(2)
        response = self.ser.read(20000).decode() 

        #Start the print
        self.ser.write(("M23 " + DestFilename + "\r").encode())
        response = self.ser.read(200).decode() 
        if "failed" in response.lower():
            return self.ERROR_OPEN_SD_CARD_FILE_FOR_PRINTING    
        self.ser.write("M24\n".encode())
        response = self.ser.read(200).decode() 

        return self.OK
        
        
def printHelp():
    print()
    print()
    print("Simple3dPrint comPort [-SL] [-SU] [-SUP] [-SP] [-P] [< sourceFilename >] [< destFilename8.3 >]")
    print()
    print("Examples:")
    print("Simple3dPrint COM5 -SL")
    print("prints the list of gcode files in the printer's SD card")
    print()
    print("Simple3dPrint COM5 -SD test.gco")
    print("Delete a file from the 3d printer's SD card")
    print()
    print("Simple3dPrint COM5 -SU test_Model_1234.gcode")
    print("Upload a file test_Model_1234.gcode to the printer's SD card to destination filename model.gco")
    print()
    print("Simple3dPrint COM5 -SU test_Model_1234.gcode test.gco")
    print("Upload a file test_Model_1234.gcode to the printer's SD card to destination filename test.gco (Note: destination filename must be in 8.3 format)")
    print()
    print("Simple3dPrint COM5 -SUP test_Model_1234.gcode test.gco")
    print("Upload a file test_Model_1234.gcode to the printer's SD card to destination filename test.gco (Note: destination filename must be in 8.3 format) and then start the print from the printer's SD card and sys.exit(). The printer continue the print without host intervention.")
    print()
    print("Simple3dPrint COM5 -SP test.gco")
    print("Start a print of a file test.gco which is already located in the the printer's SD card (Note: filename must be in 8.3 format). The printer continue the print without host intervention.")
    print()
    print("Simple3dPrint COM5 -P test_Model_1234.gcode")
    print("Start a print of a file test_Model_1234.gcode which is on the host PC directly controlling the printer via the serial pocommunication port.")

if __name__ == "__main__":
    #fufu test for the variables
    if len(sys.argv) < 3 or not(str(sys.argv[1]).upper().startswith("COM")):
        print("Error in command line parameter!")
        printHelp()
        sys.exit()
            
    #instantiate Simple3dPrint class
    s3p = Simple3dPrint(str(sys.argv[1]))

    #open com port
    error = s3p.openComPort()
    if error != s3p.OK:
        print("Error openning com port! error code: " + str(error))
        printHelp()
        sys.exit() 

    # SD list command
    if str(sys.argv[2]).upper() == "-SL":
        if len(sys.argv) > 3:
            print("Error in command line parameter!")
            printHelp()
            sys.exit()
      
        print("Print SD card file list")
        error = s3p.sdList()
        if error != s3p.OK:
            print("Error! error code: " + str(error))
            sys.exit() 
        else:
            print("OK")

    #SD upload command
    elif str(sys.argv[2]).upper() == "-SU":
        if len(sys.argv) == 4:
            print("Upload file " +  sys.argv[3] + " to  SD card file model.gco")

            error = s3p.UploadFile(sys.argv[3])    
            if error != s3p.OK:
                print("Error! error code: " + str(error))
                sys.exit() 
            else:
                print("OK")
                sys.exit()

        elif len(sys.argv) == 5:
            print("Upload file " +  sys.argv[3] + " to  SD card file " + sys.argv[4])

            error = s3p.UploadFile(sys.argv[3], sys.argv[4])
            if error != s3p.OK:
                print("Error! error code: " + str(error))
                sys.exit()
            else:
                print("\r\nOK")
                sys.exit()

        else:
            print("Error in command line parameter!")
            printHelp()
            sys.exit()
        
    #SD upload and print command
    elif str(sys.argv[2]).upper() == "-SUP":
        if len(sys.argv) == 4:
            print("Upload file " +  sys.argv[3] + " to  SD card file model.gco")
            destinationFilename = "model.gco"

            error = s3p.UploadFile(sys.argv[3])    
            if error != s3p.OK:
                print("Error! error code: " + str(error))
                sys.exit()
            else:
                print("OK")

        elif len(sys.argv) == 5:
            print("Upload file " +  sys.argv[3] + " to  SD card file " +  sys.argv[4])
            destinationFilename = sys.argv[4]

            error = s3p.UploadFile(sys.argv[3], sys.argv[4])
            if error != s3p.OK:
                print("Error! error code: " + str(error))
                sys.exit()
            else:
                print("OK")


        else:
            print("Error in command line parameter!")
            printHelp()
            sys.exit()
        
        error = s3p.PrintSdFile(destinationFilename)    
        if error != s3p.OK:
            print("Error! error code: " + str(error))
            sys.exit()
        else:
            print("OK")
            sys.exit()

    #SD print command
    elif str(sys.argv[2]).upper() == "-SP":
        if len(sys.argv) == 4:
            print("Print " +  sys.argv[3] + " from SD card")

            error = s3p.PrintSdFile(sys.argv[3])    
            if error != s3p.OK:
                print("Error! error code: " + str(error))
                sys.exit()
            else:
                print("OK")
                sys.exit()
        
        else:
            print("Error in command line parameter!")
            printHelp()
            sys.exit()

    # #direct print to printer
    # elif str(sys.argv[2]).upper() == "-P":
    #     if len(sys.argv) == 3:
    #         print("Print " +  sys.argv[3] + " directly to printer")

    #         error = s3p.PrintFile(sys.argv[3])    
    #         if error != s3p.OK:
    #             print("Error! error code: " + str(error))
    #             sys.exit()
    #         else:
    #             print("OK")
    #             sys.exit()

    else:
        print("Error in command line parameter!")
        printHelp()
        sys.exit()
