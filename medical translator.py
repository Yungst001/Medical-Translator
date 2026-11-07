import tkinter as tk
from tkinter import font

def submit_drug():
    #Show the drug info are when submit is pressed
    info_text.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

def view_history():
    #placeholder for the history button logic
    pass

#main window setup
root = tk.Tk()
root.title("Medical Information Translator")
root.geometry("500x600")

#Header
header_font = font.Font(family="Ariel", size=16, weight="bold")
header_label = tk.Label(root, text="Medical Information Translator", font=header_font)
header_label.pack(pady=20)

#Input Section
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

prompt_label = tk.Label(input_frame, text="Enter drug name", font=("Arial", 12))
prompt_label.pack()

drug_entry = tk.Entry(input_frame, width=40, font=("Arial", 12))
drug_entry.pack(pady=5)

submit_button = tk.Button(input_frame, text="Submit", command=submit_drug)
submit_button.pack(side=tk.RIGHT, padx=5)

#Drug info area
info_text = tk.Text(root, wrap=tk.WORD, height=15, width=50, font=("Arial", 11))

#Bottom Area
bottom_frame = tk.Frame(root)
bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=20)

history_button = tk.Button = tk.Button(bottom_frame, text="History", command=view_history)
history_button.pack(side=tk.LEFT)

root.mainloop()
