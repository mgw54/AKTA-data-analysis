import numpy as np
import pandas as pd
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename, asksaveasfilename
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib as mpl
import os
import time

#Premilimary setup
#import the latex font first and foremost
mpl.rcParams['font.family']='serif'
mpl.rcParams['mathtext.fontset']='cm'


def get_user_choice():
    print("Which AKTA is the data from?:")
    print("1. Old AKTA (Grey AKTA, 290)")
    print("2. MPACC AKTA (newer, white and red AKTA)")
    choice = input("Enter 1 or 2: ")
    while choice not in ("1", "2"):
        choice = input("Invalid input. Please enter 1 or 2: ")
    return choice

def getAECorSEC():
    print("What data type is this for?:")
    print("1. Anion Exchange Chromatography (AEC)")
    print("2. Size Exclusion Chromatography (SEC)")
    choice = input("Enter 1 or 2: ")
    while choice not in ("1", "2"):
        choice = input("Invalid input. Please enter 1 or 2: ")
    return choice

def fraction_yesorno():
    print("Do you want to display fraction data? (only available for Old AKTA data)")
    print("1. Yes")
    print("2. No")
    choice = input("Enter 1 or 2: ")
    while choice not in ("1", "2"):
        choice = input("Invalid input. Please enter 1 or 2: ")
    return choice

user_choice = get_user_choice()

if user_choice == "1":
    # Old AKTA (290)
    print("You selected Old AKTA (290).")
    file_path = askopenfilename(title="Select the Old AKTA (290) .xls data file", filetypes=[("Excel files", "*.xls *xlsx"), (".csv files", "*.csv")])
    if file_path.endswith('.xls'):
        df = pd.read_excel(file_path, engine='xlrd')
    elif file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path, engine='openpyxl')
    elif file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        print("Unsupported file type selected.")
        exit()
elif user_choice == "2":
    # MPACC AKTA
    print("You selected MPACC AKTA.")
    file_path = askopenfilename(title="Select the MPACC AKTA .CSV data file", filetypes=[("CSV files", "*.csv")])
    df = pd.read_csv((file_path), encoding = "utf_16_le", sep= '\t', index_col=False)


# Check if a file was selected
if not file_path:
    print("No file selected. Exiting.")
    exit()  

# Determine what type of data is in the file
userdata_choice = getAECorSEC()
if userdata_choice == "1":
    # Anion Exchange Chromatography (AEC)
    print("You selected Anion Exchange Chromatography (AEC).")
    data_type = "AEC"
elif userdata_choice == "2":
    # Size Exclusion Chromatography (SEC)
    print("You selected Size Exclusion Chromatography (SEC).")
    data_type = "SEC"
else:
    print("Invalid choice. Exiting.")
    exit()


# Process the data based on the user's choice
if user_choice == "1": 
    pcb_unnamed_x = 5
    pcb_10_y = 10.2
    frac_unnamed_x = 7
    frac_10_y = 10.3
    volsdf = df.tail(-3)["10"]
    A280df = df.tail(-3)["Unnamed: 1"]
    percentbdf = df.tail(-3)[f"Unnamed: {pcb_unnamed_x}"]
    percentbvolsdf = df.tail(-3)[str(pcb_10_y)]
    percentbvolsdf = percentbvolsdf.fillna(0)
    fractiondf = df.tail(-3)[f"Unnamed: {frac_unnamed_x}"]
    fractiondf = fractiondf.fillna(0)
    fractionvolsdf = df.tail(-3)[str(frac_10_y)]
    fractionvolsdf = fractionvolsdf.fillna(0)
    if data_type == 'AEC':
        sumdf1 = pd.DataFrame(data={'vol': volsdf,
                            'A280': A280df,
                            'percentb': percentbdf,
                            'fraction': fractiondf,
                            'fractionvolsdf': fractionvolsdf})
        sumdf1 = sumdf1.fillna(0)
    elif data_type == 'SEC':
        sumdf1 = pd.DataFrame(data={'vol': volsdf,
                            'A280': A280df,
                            'fraction': fractiondf,
                            'fractionvolsdf': fractionvolsdf})
        sumdf1 = sumdf1.fillna(0)
    else:
        print("ERROR: incorrect data type chosen")

if user_choice ==2:
    # For MPACC AKTA, we need to handle the data differently to the old AKTA
    # The MPACC AKTA data has a different structure, so we need to extract the relevant columns
    # and create a DataFrame with the relevant data.
    volsdf = df.tail(-3)["Chrom.1"]
    A280df = df.tail(-3)["Unnamed: 1"]
    percentbdf = df.tail(-3)["Unnamed: 5"]
    percentbdf = percentbdf.fillna(0)
    percentbvolsdf = df.tail(-3)["Chrom.1.2"]
    percentbvolsdf = percentbvolsdf.fillna(0)
    if data_type == 'AEC':
        sumdf1 = pd.DataFrame(data={'vol': volsdf,
                            'A280': A280df, 'percentbvols' : percentbvolsdf,
                            'percentb': percentbdf,})
        sumdf1 = sumdf1.fillna(0)
    elif data_type == 'SEC':
        sumdf1 = pd.DataFrame(data={'vol': volsdf,
                            'A280': A280df})
        sumdf1 = sumdf1.fillna(0)
    else:
        print("ERROR: incorrect data type chosen")

userfrac_choice = fraction_yesorno()
fraction_boolean = userfrac_choice == "1"


def show_scalable_plot(df):
    def update_plot(*args):
        try:
            width = float(width_var.get())
            height = float(height_var.get())
            x_min = float(xmin.get())
            x_max = float(xmax.get())
            y_min = float(ymin.get())
            y_max = float(ymax.get())
            x_inc = float(increment_x.get())
            y_inc = float(increment_y.get())
        except ValueError:
            return  # Ignore invalid input

        fig.set_size_inches(width, height)
        fig.clf()  # Clear the entire figure, including all axes

        # Recreate axes
        ax = fig.add_subplot(111)
        ax.plot(df['vol'], df['A280'], color="darkred", linewidth=2.5)
        ax.set_xlabel("Elution Volume (mL)", fontsize=14)
        ax.set_ylabel("Absorbance at 280 nm (mAU)", color="darkred", fontsize=14)
        ax.set_title(title_var.get(), fontsize=20) 

        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)
        ax.set_xticks(np.arange(x_min, x_max + x_inc, x_inc))
        ax.set_yticks(np.arange(y_min, y_max + y_inc, y_inc))

        # Gridlines
        grid_increment = 2
        def generate_number_list(min_val, max_val, increment):
            return list(np.arange(min_val, max_val + increment, increment))
        ax.set_xticks(
            generate_number_list(x_min, x_max, grid_increment),
            minor=True
        )
        ax.tick_params(which='minor', length=0.5, color='r')
        ax.grid(True, which='minor', axis='x')
        ax.grid(True, which='major', axis='x')

        # Plot %B if AEC
        if data_type == 'AEC':
            ax2 = ax.twinx()
            ax2.plot(df['vol'], df['percentb'], color="midnightblue", linewidth=2.5)
            ax2.set_ylabel("Buffer B Concentration (%)", color="midnightblue", fontsize=14)
            ax2.set_ylim(0, 100)
            ax2.tick_params(axis='y', labelcolor="midnightblue")

        if fraction_boolean:
            ax3 = ax.twiny()
            ax3.set_xlim(ax.get_xlim())
            new_tick_locations = np.array(df['fractionvolsdf'])
            ax3.set_xticks(new_tick_locations)
            ax3.set_xticklabels(df['fraction'], fontsize=10, rotation=90)
            ax3.set_xlabel(r"Elution Fractions", fontsize=14, fontname='DejaVu Sans')
    # --------------------------------------------
        canvas.draw()

    def save_and_exit():
        file_path = asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png"), ("JPEG Image", "*.jpg"), ("All Files", "*")]
        )
        if file_path:
            fig.savefig(file_path, bbox_inches='tight')
            plot_win.destroy()

    # Create Tkinter window
    plot_win = tk.Tk()
    plot_win.title("Customise Your Graph")

    # Default figure size and axis settings
    width_var = tk.StringVar(value="16")
    height_var = tk.StringVar(value="9")
    xmin = tk.StringVar(value="0")
    xmax = tk.StringVar(value="120")
    ymin = tk.StringVar(value="-10")
    ymax = tk.StringVar(value="100")
    increment_x = tk.StringVar(value="20")
    increment_y = tk.StringVar(value="10")
    title_var = tk.StringVar(value="Custom Plot Title")

    # Create matplotlib figure
    fig, ax = plt.subplots(figsize=(float(width_var.get()), float(height_var.get())))
    ax.plot(df['vol'], df['A280'])
    ax.set_xlabel("Elution Volume (mL)", fontsize=14)
    ax.set_ylabel("Absorbance at 280 nm (mAU)", color="darkred", fontsize=14)
    ax.set_title(title_var.get(), fontsize=20)
    ax.set_xlim(float(xmin.get()), float(xmax.get()))
    ax.set_ylim(float(ymin.get()), float(ymax.get()))
    ax.set_xticks(np.arange(float(xmin.get()), float(xmax.get()) + float(increment_x.get()), float(increment_x.get())))
    ax.set_yticks(np.arange(float(ymin.get()), float(ymax.get()) + float(increment_y.get()), float(increment_y.get())))

    # Insert gridlines into the graph
    grid_increment = 2
    def generate_number_list(min_val, max_val, increment):
        return list(np.arange(min_val, max_val + increment, increment))
    ax.set_xticks(
        generate_number_list(float(xmin.get()), float(xmax.get()), grid_increment),
        minor=True
    )
    ax.tick_params(which='minor', length=0.5, color='r')
    plt.grid(True, which='minor', axis='x')
    plt.grid(True, which='major', axis='x')

    print("A280 data plotted. Plotting %B...")
    # twin object for two different y-axis on the sample plot
    ax2=ax.twinx()
    # make a plot
    ax.plot(volsdf,
            A280df,
            color="darkred", linewidth = 2.5)
    # make a plot with different y-axis using second axis object
    if data_type == 'AEC':
        plt.axis([xmin.get(), xmax.get(), 0, 100])
        ax2.plot(percentbvolsdf, percentbdf,color="midnightblue", linewidth = 2.5)
        ax2.set_ylabel("Buffer B Concentration (%)",color="midnightblue",fontsize=14)

        plt.xticks(np.arange(float(xmin.get()), float(xmax.get()), float(increment_x.get())))
    else: print("No %B values shown, data_type == SEC")

    print("%B plotted. plotting elution fractions...")


    # Embed the plot in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=plot_win)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # Controls for width, height, and axis limits
    controls = tk.Frame(plot_win)
    controls.pack(side=tk.BOTTOM, fill=tk.X)

    for label_text, var in [
        ("Width:", width_var), ("Height:", height_var),
        ("X min:", xmin), ("X max:", xmax), ("X inc:", increment_x),
        ("Y min:", ymin), ("Y max:", ymax), ("Y inc:", increment_y)
    ]:
        tk.Label(controls, text=label_text).pack(side=tk.LEFT)
        ttk.Entry(controls, textvariable=var, width=5).pack(side=tk.LEFT)
    tk.Label(controls, text="Title:").pack(side=tk.LEFT)
    ttk.Entry(controls, textvariable=title_var, width=20).pack(side=tk.LEFT)

    # Save button
    save_btn = tk.Button(controls, text="Save Plot", command=save_and_exit)
    save_btn.pack(side=tk.LEFT)

    # Update plot when any value changes
    for var in [width_var, height_var, xmin, xmax, ymin, ymax, increment_x, increment_y,
                 title_var]:
        var.trace_add("write", update_plot)

    plot_win.mainloop()

# Example usage after you have your DataFrame ready:
show_scalable_plot(sumdf1)