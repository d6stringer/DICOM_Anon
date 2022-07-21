"""
Written by: Daniel Woodson
7/21/22

Select a directory containing DICOM files. Click "Anonymize"
"""

import os
import tkinter.messagebox
import pydicom
import tkinter as tk
from tkinter import filedialog, ttk, IntVar

def anonymize():
    #takes path of file containing dicom files
    # delete's paitent's name
    total_files = len(os.listdir(path))
    global root, pb, value_label, name, bd, other
    n = 0
    for file in os.listdir(path):
        n += 1
        status = round((n / total_files) * 100, 0)

        full_path = path + '/' + file
        # skip over empty files
        if os.path.getsize(full_path) > 0:
            # skip over non-dcm files
            if full_path[-4:] == '.dcm':
                dicomObject = pydicom.read_file(full_path)
                if name.get() == 1:
                    dicomObject.PatientName = '' #set to blank, could be None
                if bd.get() == 1:
                    dicomObject.PatientBirthDate = ''
                if other.get() == 1:
                    dicomObject.PatientSex = ''
                    dicomObject.PatientID = ''
                dicomObject.save_as(full_path)
                pb['value'] = status
                value_label.config(text=str(status) + "%")
                root.update_idletasks()
def user_confirm():
    answer = tkinter.messagebox.askquestion(title='Are you sure?',
                                   message='The DICOM files in\n' + path + '\nwill all be fully and irreversably anonymized!',
                                   icon='question')
    if answer == 'yes':
        anonymize()
    else:
        mkBye()
def mkBye():
    tkinter.messagebox.showinfo(title='M-kay',
                                message='Bye!')
    return
def get_dir():
    global path
    path = filedialog.askdirectory()
    dir_label['text'] = path
    return

path = ''
status = 0
if __name__ == '__main__':
    root = tk.Tk()
    root.title('Anonymize DICOMs')
    root.iconbitmap('w.ico')
    btn1 = tk.Button(root,
                    text= 'Select Folder',
                    command= get_dir)
    btn1.grid(row=0, column=1, pady=10)
    dir_label = ttk.Label(root,
                          text=path)
    dir_label.grid(row=1, column=1, pady=10)
    name = IntVar()
    bd = IntVar()
    other = IntVar()
    cb1 = tk.Checkbutton(root, text='Name',
                         variable=name,
                         onvalue=1,
                         offvalue=0,
                         height=2)
    cb1.select()
    cb2 = tk.Checkbutton(root, text='Birthday',
                         variable=bd,
                         onvalue=1,
                         offvalue=0,
                         height=2)
    cb2.select()
    cb3 = tk.Checkbutton(root, text='Other',
                         variable=other,
                         onvalue=1,
                         offvalue=0,
                         height=2)
    cb3.select()
    cb1.grid(row=2, column=0, pady=10, padx=10)
    cb2.grid(row=2, column=1, pady=10, padx=10)
    cb3.grid(row=2, column=2, pady=10, padx=10)
    btn2 = tk.Button(root,
                    text= 'Anonymize',
                    command= user_confirm)
    btn2.grid(row=3, column=1, pady=10)
    stat = ttk.Label(root, text='Status')
    stat.grid(row=4, column=1)
    pb = ttk.Progressbar(root,
                         orient='horizontal',
                         mode='determinate',
                         length=175)

    pb.grid(row=5, column=1)
    value_label = ttk.Label(root, text='0%')
    value_label.grid(row=6, column=1, pady=10)
    root.mainloop()


