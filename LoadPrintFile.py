import serial
import sys
import time

def LoadPrintFile(comPort, fileName):
    try:
        ser = serial.Serial(comPort,baudrate=250000,timeout=0.5)
        #ser.open()
    except Exception as exception:
        return 1

    try:
        f = open(fileName)
    except:
        return 2

    lines = f.readlines()

    time.sleep(2)
    #flush the serial port from boot data
    response = ser.read(1000)

    #Start the file save to filename model.gco
    ser.write("M28 model.gco\r".encode())
    response = ser.read(200).decode() 
    if not 'ok' in response:
        print("Failed openning file on SD card")
    else:
        lineNumber = 0
        for line in lines:
            lineNumber += 1
            if line.startswith(';'):
                continue
            if ";" in line:
                line = line[:line.index(";")]
                line += "\n"
            ser.write(line.encode())
            response = ser.read(3).decode() 
            # if 'ok' in response:
            #     print("\r",lineNumber,"/",len(lines),end=''),
            #print("\r",lineNumber,"/",len(lines),end=''),
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
        response = ser.read(20000).decode() 
        
        #Close the file model.gco
        ser.write("M29\n".encode())
        response = ser.read(200).decode() 
        
        if not 'Done' in response:
            print("\rFailed closing file to SD card")
        else:
            print("\rDone saving model.gco file to SD card")

        #Start the print
        print("\rStart printing model: ", fileName)
        ser.write("M23 model.gco\n".encode())
        response = ser.read(200).decode() 
        ser.write("M24\n".encode())
        response = ser.read(200).decode() 
        
        #exit
        print("Exit and let the printer do its work")
        ser.close()
        return 0
        

if __name__ == "__main__":
    if len(sys.argv) != 3 or not(str(sys.argv[1]).upper().startswith("COM")):
        print("Error! use LoadPrintFile COMx,<fileName>")
    else:
        error = LoadPrintFile(str(sys.argv[1]),str(sys.argv[2]))
        if error == 1:
            print("Error! cannot open com port: " + str(sys.argv[1]))
        elif error == 2:
            print("Error! cannot open file: " + str(sys.argv[2]))
            