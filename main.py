import tkinter as tk
from tkinter import font, messagebox
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from translator import translate_drug_info
from api_client import get_drug_information
import socket


def check_internet_connection():
    """Return True when an internet connection can be reached."""
    try:
        # A short timeout prevents the application from waiting too long.
        with urlopen("https://www.google.com", timeout=5) as response:
            return response.status == 200
    except (URLError, HTTPError, TimeoutError, socket.timeout, OSError):
        return False


def submit_drug():
    """Validate the medicine name and check the internet before lookup."""
    drug_name = drug_entry.get().strip()

    # Error 1: The user submitted an empty or whitespace-only entry.
    if not drug_name:
        messagebox.showwarning(
            "Missing medicine name",
            "Please enter a medicine name before clicking Submit."
        )
        drug_entry.focus_set()
        return

    # Error 2: The user has no internet connection.
    submit_button.config(state=tk.DISABLED, text="Checking...")
    root.update_idletasks()

    try:
        if not check_internet_connection():
            messagebox.showerror(
                "No internet connection",
                "The internet connection is unavailable. Please check your network and try again."
            )
            return

        fda_text = get_drug_information(drug_name)
        friendly_text = translate_drug_info(drug_name, fda_text)
        
        info_text.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        info_text.delete("1.0", tk.END)
        info_text.insert(tk.END, friendly_text)

    except Exception as error:
        # Safety net for unexpected errors so the app displays a message
        # instead of closing without explanation.
        messagebox.showerror(
            "Application error",
            f"Something went wrong while processing your request.\n\nDetails: {error}"
        )
    finally:
        submit_button.config(state=tk.NORMAL, text="Submit")


def view_history():
    # Placeholder for the history button logic.
    messagebox.showinfo("History", "The search history feature is not available yet.")


# Main window setup
root = tk.Tk()
root.title("Medical Information Translator")
root.geometry("500x600")

# Header
header_font = font.Font(family="Arial", size=16, weight="bold")
header_label = tk.Label(root, text="Medical Information Translator", font=header_font)
header_label.pack(pady=20)

# Input section
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

prompt_label = tk.Label(input_frame, text="Enter drug name", font=("Arial", 12))
prompt_label.pack()

drug_entry = tk.Entry(input_frame, width=40, font=("Arial", 12))
drug_entry.pack(pady=5)

submit_button = tk.Button(input_frame, text="Submit", command=submit_drug)
submit_button.pack(side=tk.RIGHT, padx=5)

# Drug information area
info_text = tk.Text(root, wrap=tk.WORD, height=15, width=50, font=("Arial", 11))

# Bottom area
bottom_frame = tk.Frame(root)
bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=20)

history_button = tk.Button(bottom_frame, text="History", command=view_history)
history_button.pack(side=tk.LEFT)

root.mainloop()
