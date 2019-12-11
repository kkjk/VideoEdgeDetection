
import numpy as np
import cv2
from PIL import Image
import tkinter as tk

from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror


# window = tk.Tk()

# ## rename the window title
# window.title('FARO Video Player')
# Fcanvas = tk.Canvas(bg="black", height=600, width=170)
#window.filename = tk.filedialog.askopenfilename


class MyFrame(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.master.title("Faro Video Player")
        self.master.rowconfigure(10, weight=1)
        self.master.columnconfigure(10, weight=1)
        self.grid(sticky=W+E+N+S)

        self.button = Button(self, text="Browse", command=self.load_file, width=10)
        self.button.grid(row=1, column=1, sticky=W)

    def load_file(self):
        fname = askopenfilename(filetypes=(("Video files", "*.mp4;*.avi"),
                                           ("All files", "*.*")))

        if fname:
            try:
                
                print("""here it comes: self.settings["template"].set(fname)""")
            except:                     # <- naked except is a bad idea
                showerror("Open Source File", "Failed to read file\n'%s'" % fname)
            return


if __name__ == "__main__":
    MyFrame().mainloop()

#window.mainloop()
