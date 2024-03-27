import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import numpy as np
import random

# Global variables
dataOut = np.array([])
dataRef = np.array([])
tracking_time = 10.0  # seconds
h = 10  # ms
xRef = []
index = 0.0
fps = 10  # Does not work for very high numbers (Becomes laggy and out of sync w time)
squarePeriodTime = 3
squareAmp = 5
iteration = 0

# Initialize root window
root = tk.Tk()
root.geometry("1920x1024")
root.option_add('*Font', ("Courier", 15, "bold"))
root.title("Ball & Beam GUI")

# Create 3 main frames
parameterFrame = tk.Frame(root)
plotFrame = tk.Frame(root)
referenceFrame = tk.Frame(root)

# Define frames as three column grids
parameterFrame.grid(row=0, column=0, sticky="ns")
plotFrame.grid(row=0, column=1, sticky="nsew")
referenceFrame.grid(row=0, column=2, sticky="nsew")

# Set column/row weights to allow resizing
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=6)
root.columnconfigure(2, weight=1)
root.rowconfigure(0, weight=1)

# Create frame for settings (off,beam,ball and stop)
settings = tk.Frame(parameterFrame)
settings.pack(side=tk.BOTTOM)

# Radio-buttons
options = ['Off', 'Beam', 'Ball']
x = tk.IntVar()  # Define x as integer object
for i in range(len(options)):
    button = tk.Radiobutton(settings, text=options[i], variable=x, value=i, padx=2, font=('Courier', 20), width=4)
    # Put settings as a grid
    button.grid(row=0, column=i)

# Stop-button
stop = tk.Button(settings, text='Stop', font=('Courier', 20), width=20)
stop.grid(row=1, column=1)

# Create frame for header text
textFrame = tk.Frame(parameterFrame)
textFrame.pack(side=tk.TOP)

# Header text
innerpar_label = tk.Label(textFrame, text='Inner Parameters', padx=8, pady=5, font=('Courier', 20, 'bold'))
innerpar_label.grid(row=1, column=0)
outerpar_label = tk.Label(textFrame, text='          Outer Parameters', padx=8, pady=5, font=('Courier', 20, 'bold'))
outerpar_label.grid(row=1, column=1)

# Create frame for parameter buttons
params = tk.Frame(parameterFrame)
params.pack(side=tk.TOP, expand=True)


# Help-function to ensure int/float inputs only to text-box
def on_validate(P):
    if P == "":
        return True
    try:
        float(P)
        return True
    except ValueError:
        root.bell()  # Ring a bell when invalid input is detected
        return False


# Parameter buttons
param1 = ['K', 'Ti', 'Tr', 'Beta', 'h']
for i in range(len(param1)):
    label = tk.Label(params, text=param1[i], font=('Courier', 20), width=5)
    label.grid(row=i, column=0, sticky="nsew")
    button = tk.Entry(params, validate="key", validatecommand=(params.register(on_validate), "%P"),
                      font=('Courier', 60), width=3)
    button.grid(row=i, column=1, sticky="nsew")

param2 = ['K', 'Ti', 'Td', 'N', 'Tr', 'Beta', 'h']
for i in range(len(param2)):
    label = tk.Label(params, text=param2[i], font=('Courier', 20), width=5)
    label.grid(row=i, column=2, sticky="nsew")
    button = tk.Entry(params, validate="key", validatecommand=(params.register(on_validate), "%P"),
                      font=('Courier', 60), width=3)
    button.grid(row=i, column=3, sticky="nsew")

# Apply buttons
apply1 = tk.Button(params, text='Apply', font=('Courier', 15), width=5)
apply1.grid(row=7, column=3, sticky="nsew")
apply2 = tk.Button(params, text='Apply', font=('Courier', 15), width=5)
apply2.grid(row=5, column=1, sticky="nsew")

# Create plots
fig, (axRef, axCon) = plt.subplots(2)

axRef.set_title('Reference and Output signal')
axRef.set_xlabel('Time')
axRef.set_ylabel('Position')
axRef.set_xlim(0, tracking_time)
axRef.set_ylim(-10, 10)
linesOut, = axRef.plot([], [], color='red')
linesRef, = axRef.plot([], [], color='black')

axCon.set_title('Control signal')
axCon.set_xlabel('Time')
axCon.set_ylabel('Position')
axCon.set_xlim(0, tracking_time)
axCon.set_ylim(-10, 10)
linesCon, = axCon.plot([], [], color='blue')

# Create canvas
canvas = FigureCanvasTkAgg(fig, master=plotFrame)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


def update(frame):
    global dataOut, dataRef, xRef, index, tracking_time, fps, iteration, squareAmp
    xRef.append(index)  # This counts the iterations for the x-axis

    # Append data to dataOut
    dummy = random.randrange(-10, 10)  # This should be changed to the actual output signal
    dataOut = np.append(dataOut, dummy)

    # Append data to dataRef
    if iteration / fps % squarePeriodTime == 0:
        squareAmp *= -1
    dataRef = np.append(dataRef, squareAmp)
    # Update x-axis limits dynamically
    axRef.set_xlim(max(0.0, index - tracking_time), max(tracking_time, index))
    linesOut.set_data(xRef, dataOut)
    linesRef.set_data(xRef, dataRef)
    index += 1 / fps
    iteration += 1
    return linesOut,  # Return the new changes. This is to just plot the new data using "blit"


animation = FuncAnimation(fig, update, interval=1000 / fps, cache_frame_data=False, blit=False)

root.mainloop()
