import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import os

def select_file(filetypes, encoding=None, sep=None):
    file_path = filedialog.askopenfilename(title="Select data file", filetypes=filetypes)
    if not file_path:
        messagebox.showinfo("No file", "No file selected. Exiting.")
        return None, None
    if file_path.endswith('.xls'):
        df = pd.read_excel(file_path, engine='xlrd')
    elif file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path, engine='openpyxl')
    elif file_path.endswith('.csv'):
        if encoding and sep:
            df = pd.read_csv(file_path, encoding=encoding, sep=sep, index_col=False)
        else:
            df = pd.read_csv(file_path)
    else:
        messagebox.showerror("Error", "Unsupported file type selected.")
        return None, None
    return file_path, df

def old_akta():
    filetypes = [("Excel files", "*.xls *.xlsx"), ("CSV files", "*.csv")]
    file_path, df = select_file(filetypes)
    aktachoice = 0
    if df is not None:
        messagebox.showinfo("Success", f"Loaded file: {file_path}\n\nFirst rows:\n{df.head()}")
    root.quit()

def mpacc_akta():
    filetypes = [("CSV files", "*.csv")]
    file_path, df = select_file(filetypes, encoding="utf_16_le", sep='\t')
    aktachoice = 1
    if df is not None:
        messagebox.showinfo("Success", f"Loaded file: {file_path}\n\nFirst rows:\n{df.head()}")
    root.quit()

root = tk.Tk()
root.title("AKTA Data Loader")
root.geometry("300x150")
# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
icon_path = os.path.join(script_dir, "..", "data", "GUI-bin", "Picture1.ico")
root.iconbitmap(icon_path)
label = tk.Label(root, text="Which AKTA is the data from?")
label.pack(pady=10)

btn1 = tk.Button(root, text="Old AKTA (Grey AKTA, 290)", command=old_akta)
btn1.pack(pady=5)

btn2 = tk.Button(root, text="MPACC AKTA (newer, white/red)", command=mpacc_akta)
btn2.pack(pady=5)

root.mainloop()