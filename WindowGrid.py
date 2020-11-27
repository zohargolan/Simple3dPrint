import tkinter as tk

def createGrid(window, rowNumber, columnNumber):
	frameDict = {}
	for i in range(rowNumber):
		frameDict[i] = {}
		window.columnconfigure(i, weight=1)
		window.rowconfigure(i, weight=1)
		for j in range(columnNumber):
			frame = tk.Frame(master=window, pady=5)
			frame.grid(row=i, column=j)
			frameDict[i][j] = frame
	return frameDict