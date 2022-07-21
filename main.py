"""
Written by: Daniel Woodson
7/21/22

Select a directory containing DICOM files. Click "Anonymize" 
"""

import os
import tkinter.messagebox
import pydicom
import tkinter as tk
from tkinter import filedialog, ttk

def anonymize():
    #takes path of file containing dicom files
    # delete's paitent's name
    total_files = len(os.listdir(path))
    global root, pb, value_label
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
                dicomObject.PatientName = '' #set to blank, could be None
                dicomObject.save_as(full_path)
                pb['value'] = status
                value_label.config(text=str(status) + "%")
                root.update_idletasks()

def user_confirm():
    answer = tkinter.messagebox.askquestion(title='Are you sure?',
                                   message='The DICOM files in\n' + path + '\nwill all be fully and irreversably anonymized!',
                                   icon='question'
                                   )
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
    root.geometry('500x250')
    root.title('Anonymize DICOMs')

    btn1 = tk.Button(root,
                    text= 'Select Folder',
                    command= get_dir)
    btn1.pack(pady=10)

    dir_label = ttk.Label(root,
                          text=path)
    dir_label.pack(pady=10)
    btn2 = tk.Button(root,
                    text= 'Anonymize',
                    command= user_confirm)
    btn2.pack(pady=10)
    pb = ttk.Progressbar(root,
                         orient='horizontal',
                         mode='determinate',
                         length=175)
    pb.pack(pady=10)
    value_label = ttk.Label(root, text='0%')
    value_label.pack(pady=10)
    root.mainloop()


