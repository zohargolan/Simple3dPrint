import serial
import sys
import time

def LoadPrintFile(comPort):
    try:
        ser = serial.Serial(comPort,baudrate=250000,timeout=0.5)
        #ser.open()
    except Exception as exception:
        return 1

        #Start the print
        print("\rStart printing model: ")
        ser.write("M23 model.gco\n".encode())
        response = ser.read(200).decode() 
        ser.write("M24\n".encode())
        response = ser.read(200).decode() 
        
        #exit
        print("Exit and let the printer do its work")
        ser.close()
        return 0
        

if __name__ == "__main__":
    if len(sys.argv) != 2 or not(str(sys.argv[1]).upper().startswith("COM")):
        print("Error! use PrintModelFile COMx")
    else:
        error = PrintModelFile(str(sys.argv[1]))
        if error == 1:
            print("Error! cannot open com port: " + str(sys.argv[1]))
        
            