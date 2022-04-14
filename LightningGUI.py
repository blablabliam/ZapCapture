from tkinter import *
from tkinter import filedialog
from tkinter import ttk

# def calculate(*args):
#     try:
#         value = float(feet.get())
#         meters.set(int(0.3048 * value * 10000.0 + 0.5)/10000.0)
#     except ValueError:
#         pass
def browse_button_in():
    # Allow user to select a directory and store it in global var
    # called folder_path_in
    # This function is called by the input directory button.
    global folder_path_in
    filename = filedialog.askdirectory()
    folder_path_in.set(filename)
    print(filename)

def browse_button_out():
    # Allow user to select a directory and store it in global var
    # called folder_path_out
    # This function is called by the output directory button.
    global folder_path_out
    filename = filedialog.askdirectory()
    folder_path_out.set(filename)
    print(filename)

def execute_analysis():
    print('analyzed!')

#Build window root frame
root = Tk()
root.title("Lightning Bolt Analyzer")
root.geometry('700x250+1000+300')
#establish grid in root called mainframe
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

#Get the input folder directory.
#This directory will hold all of the video files to be analyzed.
folder_path_in = StringVar()
inputlabel = Label(master=mainframe,textvariable=folder_path_in)
inputlabel.grid(row=0, column=1)
inputbutton = Button(master=mainframe, text="Input Folder", command=browse_button_in)
inputbutton.grid(row=0, column=0)

#Get the output folder directory.
#This directory will hold all of the image frames after analysis.
folder_path_out = StringVar()
outputlabel = Label(master=mainframe,textvariable=folder_path_out)
outputlabel.grid(row=1, column=1)
outputbutton = Button(master=mainframe,text="Output Folder", command=browse_button_out)
outputbutton.grid(row=1, column=0)

#input for the Threshold.
#Input can range from 10,000 all the way to 500,000 while giving good results.
thresholdsetpoint = StringVar()
thresholdsetpoint.set(50000)
thresholdlabel = Label(master=mainframe, text="Threshold Select")
thresholdlabel.grid(row=2, column=0)
threshold = Entry(master=mainframe, textvariable=thresholdsetpoint)
threshold.grid(row=2, column=1)

#Analyze button
#This should start the analysis, and give some kind of feedback.
analysislabel = Label(master=mainframe, text='Perform Analysis?')
analysislabel.grid(row=3, column=0)
analysisbutton = Button(master=mainframe, text='Analyze!', command=execute_analysis)
analysisbutton.grid(row=3, column=1)

#Progress Bar
#A progress bar can be installed here, although since that requires multithreading
#I am not super exited to get into it until the whole system is working.
#For now, a placeholder bar gets to occupy the slot.

progressbar =

#Instructions Text Box
#This sits below the mainframe, and gives instructions on running the software.
instructions = '''Instructions to be filled in on later date.
https://blablabliam.github.io'''
instructionbox=Label(master=root, text=instructions)
instructionbox.grid(row=1, column=0)


# folder_selected = filedialog.askdirectory()
# feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
# feet_entry.grid(column=2, row=1, sticky=(W, E))
#
# meters = StringVar()
# ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))
#
# ttk.Button(mainframe, text="Calculate", command=calculate).grid(column=3, row=3, sticky=W)
#
# ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
# ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
# ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)
#
for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

inputlabel.focus()
#root.bind("<Return>", calculate)

root.mainloop()
