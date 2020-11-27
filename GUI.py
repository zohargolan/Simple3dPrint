import tkinter as tk
import tkinter.filedialog as fd
from WindowGrid import createGrid

def selectSourceFile(event, entry):
	name = fd.askopenfilename()
	entry.insert(0, name)
	print('button clicked')
	print(name)
	print(event)

window = tk.Tk()

frameDict = createGrid(window, 5, 2)

appTitle = tk.Label(master=frameDict[0][1], text='Simple3dPrint')
appTitle.pack()

comPortLbl = tk.Label(master=frameDict[1][1], text='Com Port')
comPortEnt = tk.Entry(master=frameDict[1][1])
comPortLbl.pack(side=tk.LEFT)
comPortEnt.pack(side=tk.LEFT)

destinationNameLbl = tk.Label(master=frameDict[2][1], text='Destination Filename')
destinationNameEnt = tk.Entry(master=frameDict[2][1])
destinationNameLbl.pack(side=tk.LEFT)
destinationNameEnt.pack(side=tk.LEFT)


sourceNameLbl = tk.Label(master=frameDict[3][1], text='Source Filename')
sourceNameEnt = tk.Entry(master=frameDict[3][1])
sourceNameSelectBtn = tk.Button(master=frameDict[3][1], text='Select File')
sourceNameSelectBtn.bind('<Button-1>', lambda event: selectSourceFile(event, sourceNameEnt))
sourceNameLbl.pack(side=tk.LEFT)
sourceNameEnt.pack(side=tk.LEFT)
sourceNameSelectBtn.pack(side=tk.LEFT)

sendBtn = tk.Button(master=frameDict[4][1], text='Send')
# Bind method to sendBtn click
# sendBtn.bind('<Button-1>', lambda event: selectSourceFile(event, sourceNameEnt))
sendBtn.pack(side=tk.LEFT)

window.mainloop()