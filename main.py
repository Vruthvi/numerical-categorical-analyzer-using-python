import customtkinter as tk
import pandas as pd
from tkinter import filedialog
from matplotlib import pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

root = tk.CTk()
root.title("Numerical and Categorical Analysis")
root.geometry("1280x1024")
tk.set_appearance_mode("dark")
tk.set_default_color_theme("dark-blue")

frame1 = tk.CTkFrame(root, fg_color="transparent")
frame1.pack(pady=15, fill="x")

frame2 = tk.CTkFrame(root, fg_color="transparent")
frame2.pack(side="top", padx=0, pady=10, fill="x", anchor="center")

frame3 = tk.CTkFrame(root,fg_color="transparent")
frame3.pack(side="left", padx=20, pady=10, fill="y", anchor="w")

frame4 = tk.CTkFrame(root, width=800, height=200, fg_color="transparent")
frame4.pack(side="top", padx=5, pady=20,anchor="center")
frame4.configure(fg_color="transparent")

def label_heading(text, frame):
    label = tk.CTkLabel(frame, text=text, font=("Times New Roman bold", 25))
    label.pack(anchor="center")
    return label

def label_subhead(text, frame, padx=0,pady=0, anchor="center"):
    label = tk.CTkLabel(frame, text=text, font=("Arial", 16))
    label.pack(padx=padx, pady=pady, anchor=anchor)
    return label

def button(text, frame, command):
    btn = tk.CTkButton(frame, text=text, font=("Arial", 14), command=command)
    btn.pack(pady=10)
    return btn

def change_theme():
    if tk.get_appearance_mode().lower() == "light":
        tk.set_appearance_mode("dark")
        theme_button.configure(fg_color="white",text_color="black",hover_color="white")
    else:
        tk.set_appearance_mode("light")
        theme_button.configure(fg_color="black",text_color="white",hover_color="black")

def get_num_col():
    num_sel = numerical_menu.get()
    if num_sel != "No Data Loaded":
        n = data[num_sel]
        fig, axes = plt.subplots(1, 2, figsize=(12,6))
        fig.suptitle(f"Numerical Analysis of {num_sel}", fontsize=16)
        sns.histplot(n, kde=True, bins=10, color='blue', ax=axes[0])
        axes[0].set_title(f'Histogram of {num_sel}')
        sns.boxplot(n, color='red', ax=axes[1])
        axes[1].set_title(f'Boxplot of {num_sel}')
        fig.tight_layout(rect=[0, 0, 1, 0.95])

        for widget in frame4.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=frame4)
        canvas.draw()
        toolbar=NavigationToolbar2Tk(canvas,frame4)
        toolbar.update()
        canvas.get_tk_widget().pack(fill="both")

def get_cat_col():
    cat_sel = categorical_menu.get()
    if cat_sel != "No Data Loaded":
        categorical_column = data[cat_sel]
        frequency = categorical_column.value_counts()
        
        fig, axes = plt.subplots(1, 2, figsize=(12,6), facecolor="none")
        fig.suptitle(f"Categorical Analysis of {cat_sel}", fontsize=16)
        sns.barplot(x=frequency.index, y=frequency.values, ax=axes[0])
        axes[0].set_title(f'Bar Chart of {cat_sel}')
        axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=45)

        axes[1].pie(frequency, labels=frequency.index, autopct='%1.1f%%', startangle=140)
        axes[1].set_title(f'Pie Chart of {cat_sel}')
        
        fig.tight_layout(rect=[0, 0, 1, 0.95])
        for widget in frame4.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=frame4)
        canvas.draw()
        toolbar=NavigationToolbar2Tk(canvas,frame4)
        toolbar.update()
        canvas.get_tk_widget().pack(fill="x")

def open_csv_file():
    file_path = filedialog.askopenfilename(
        title="Open CSV File",
        filetypes=[("CSV Files", "*.csv")]
    )
    global data, cat_col, num_col
    if file_path:
        try:
            for widget in frame2.winfo_children():
                if isinstance(widget, tk.CTkLabel):
                    widget.destroy()
            for widget in frame4.winfo_children():
                widget.destroy()

            file_label = label_subhead(f"Opened CSV: {file_path}", frame2, padx=0, pady=0, anchor="center")
            file_label.configure(font=("Arial bold", 18))
            data = pd.read_csv(file_path)
            num_col = data.select_dtypes(include=['number']).columns
            cat_col = data.select_dtypes(exclude=['number']).columns
            numerical_menu.set("Select Numerical Column")
            categorical_menu.set("Select Categorical Column")
            numerical_menu.configure(values=list(num_col))
            categorical_menu.configure(values=list(cat_col))
            
        except Exception as e:
            print(f"Error reading file: {e}")

label_heading("Numerical and Categorical Analysis", frame1)

button("Open CSV File", frame2, open_csv_file)

label_subhead("Select the Numerical Column:", frame3, padx=0, pady=5, anchor="w")
numerical_menu = tk.CTkOptionMenu(frame3, values=["No Data Loaded"], font=("Arial", 14))
numerical_menu.pack(pady=10)
numerical_menu.set("Select Numerical Columns")
button("Submit Numerical Column", frame3, get_num_col)

label_subhead("Select the Categorical Column:", frame3, padx=0, pady=5, anchor="w")
categorical_menu = tk.CTkOptionMenu(frame3, values=["No Data Loaded"], font=("Arial", 14))
categorical_menu.pack(pady=10)
categorical_menu.set("Select Categorical Columns")
button("Submit Categorical Column", frame3, get_cat_col)

quit_button = tk.CTkButton(frame3, text="Quit", font=("Arial", 14), command=root.destroy, fg_color="red",hover_color="red")
quit_button.pack(side="bottom", pady=10,anchor="sw")

theme_button = tk.CTkButton(frame3, text="Change Theme", font=("Arial", 14), command=change_theme,fg_color="white",hover_color="white",text_color="black")
theme_button.pack(side="bottom",anchor="sw",pady=15)

root.mainloop()