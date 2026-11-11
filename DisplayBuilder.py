import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime


class DisplayBuilder:
    """
    Builds and manages the medicine information display
    and search history for the application.
    """

    HISTORY_FILE = "search_history.json"

    def __init__(self, root):
        self.root = root

        # Create the medicine information display
        self.info_text = tk.Text(
            root,
            wrap=tk.WORD,
            height=22,
            width=65,
            font=("Arial", 10)
        )

        self.info_text.pack(
            pady=10,
            padx=20,
            fill=tk.BOTH,
            expand=True
        )

        # Load previous search records
        self.history = self.load_history()

    def display_information(self, information):
        """Display medicine information in the results area."""

        self.info_text.delete("1.0", tk.END)
        self.info_text.insert(tk.END, str(information))

    def load_history(self):
        """Load saved medicine searches from a JSON file."""

        if not os.path.exists(self.HISTORY_FILE):
            return []

        try:
            with open(
                self.HISTORY_FILE,
                "r",
                encoding="utf-8"
            ) as file:
                data = json.load(file)

            if isinstance(data, list):
                return [
                    item for item in data
                    if isinstance(item, dict)
                ]

            return []

        except (json.JSONDecodeError, OSError):
            return []

    def save_history(self):
        """Save search history to the JSON file."""

        try:
            with open(
                self.HISTORY_FILE,
                "w",
                encoding="utf-8"
            ) as file:
                json.dump(
                    self.history,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

        except OSError as error:
            messagebox.showerror(
                "History Error",
                f"Unable to save search history: {error}"
            )

    def add_to_history(self, drug_name, information):
        """Save a successful medicine search."""

        record = {
            "drug_name": drug_name,
            "information": information,
            "date": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

        # Remove an older record of the same medicine
        self.history = [
            item for item in self.history
            if item.get("drug_name", "").lower()
            != drug_name.lower()
        ]

        # Add the latest search at the beginning
        self.history.insert(0, record)

        # Keep only the latest 50 searches
        self.history = self.history[:50]

        self.save_history()

    def show_history(self):
        """Display previous medicine searches in a new window."""

        # Refresh history from the saved file
        self.history = self.load_history()

        if not self.history:
            messagebox.showinfo(
                "Search History",
                "No previous searches found."
            )
            return

        history_window = tk.Toplevel(self.root)
        history_window.title("Search History")
        history_window.geometry("450x400")

        tk.Label(
            history_window,
            text="Previous Medicine Searches",
            font=("Arial", 13, "bold")
        ).pack(pady=10)

        history_list = tk.Listbox(
            history_window,
            font=("Arial", 10),
            width=55,
            height=15
        )

        history_list.pack(
            padx=10,
            pady=10,
            fill=tk.BOTH,
            expand=True
        )

        # Display saved medicine names and dates
        for record in self.history:
            name = record.get("drug_name", "Unknown")
            date = record.get("date", "Unknown date")

            history_list.insert(
                tk.END,
                f"{name} - {date}"
            )

        def view_selected():
            selection = history_list.curselection()

            if not selection:
                messagebox.showwarning(
                    "Select Search",
                    "Please select a medicine from the history."
                )
                return

            record = self.history[selection[0]]

            self.display_information(
                record.get(
                    "information",
                    "No information saved."
                )
            )

            history_window.destroy()

        tk.Button(
            history_window,
            text="View Selected Search",
            command=view_selected
        ).pack(pady=10)
