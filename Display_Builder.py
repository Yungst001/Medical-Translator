import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import json
import os
from datetime import datetime


class DisplayBuilder:
    """
    This class builds the main visual parts of the app:
    - Left side: Search history
    - Right side: Scrollable results area
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Medication Information Translator")
        self.root.geometry("950x620")
        self.root.minsize(800, 500)

        # File where history is saved
        self.history_file = "search_history.json"

        # Colors
        self.bg_color = "#f5f7fa"
        self.sidebar_color = "#e8eef5"
        self.accent = "#2c5aa0"

        self.root.configure(bg=self.bg_color)

        # Build the layout
        self.create_widgets()
        self.load_history()

    def create_widgets(self):
        """Create all the visual parts of the window"""

        # ---------- TOP BAR (title + search) ----------
        top_frame = tk.Frame(self.root, bg=self.accent, height=60)
        top_frame.pack(fill="x")
        top_frame.pack_propagate(False)

        title_label = tk.Label(
            top_frame,
            text="💊  Medication Information Translator",
            font=("Segoe UI", 16, "bold"),
            bg=self.accent,
            fg="white"
        )
        title_label.pack(side="left", padx=15, pady=12)

        # ---------- MAIN AREA (sidebar + results) ----------
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # LEFT SIDE - History Panel
        left_frame = tk.Frame(main_frame, bg=self.sidebar_color, width=230)
        left_frame.pack(side="left", fill="y", padx=(0, 10))
        left_frame.pack_propagate(False)

        history_title = tk.Label(
            left_frame,
            text="Search History",
            font=("Segoe UI", 12, "bold"),
            bg=self.sidebar_color,
            fg="#333"
        )
        history_title.pack(pady=(12, 5))

        # Listbox for history
        self.history_listbox = tk.Listbox(
            left_frame,
            font=("Segoe UI", 10),
            bg="white",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#ccc",
            selectbackground=self.accent,
            activestyle="none"
        )
        self.history_listbox.pack(fill="both", expand=True, padx=10, pady=5)
        self.history_listbox.bind("<<ListboxSelect>>", self.on_history_select)

        # Clear history button
        clear_btn = tk.Button(
            left_frame,
            text="Clear History",
            font=("Segoe UI", 9),
            bg="#d9534f",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.clear_history
        )
        clear_btn.pack(pady=10, padx=10, fill="x")

        # RIGHT SIDE - Results Panel
        right_frame = tk.Frame(main_frame, bg=self.bg_color)
        right_frame.pack(side="right", fill="both", expand=True)

        # Search bar
        search_frame = tk.Frame(right_frame, bg=self.bg_color)
        search_frame.pack(fill="x", pady=(0, 10))

        self.search_entry = tk.Entry(
            search_frame,
            font=("Segoe UI", 12),
            relief="solid",
            bd=1
        )
        self.search_entry.pack(side="left", fill="x", expand=True, ipady=6)
        self.search_entry.bind("<Return>", lambda e: self.search_clicked())

        search_btn = tk.Button(
            search_frame,
            text="Search",
            font=("Segoe UI", 11, "bold"),
            bg=self.accent,
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=18,
            command=self.search_clicked
        )
        search_btn.pack(side="left", padx=(8, 0))

        # Label above results
        result_label = tk.Label(
            right_frame,
            text="Drug Information",
            font=("Segoe UI", 12, "bold"),
            bg=self.bg_color,
            fg="#333",
            anchor="w"
        )
        result_label.pack(fill="x", pady=(5, 3))

        # ===== SCROLLABLE TEXT AREA (ScrolledText) =====
        # This is the main place where usage, warnings and side effects appear
        self.result_text = scrolledtext.ScrolledText(
            right_frame,
            font=("Segoe UI", 11),
            wrap=tk.WORD,
            relief="solid",
            bd=1,
            bg="white",
            padx=12,
            pady=10
        )
        self.result_text.pack(fill="both", expand=True)

        # Make the text area read-only (user can still select/copy)
        self.result_text.config(state="disabled")

        # Status bar at the bottom
        self.status_label = tk.Label(
            self.root,
            text="Ready. Type a medication name and click Search.",
            font=("Segoe UI", 9),
            bg="#e0e0e0",
            fg="#555",
            anchor="w",
            padx=10
        )
        self.status_label.pack(fill="x", side="bottom")

    # --------------------------------------------------
    # Display Methods
    # --------------------------------------------------
    def show_results(self, medication_data: dict):
        """
        Display the drug information inside the ScrolledText area.
        medication_data should be a dictionary with keys like:
        brand_name, generic_name, indications, warnings, side_effects, dosage
        """
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)

        brand = medication_data.get("brand_name") or "—"
        generic = medication_data.get("generic_name") or "—"
        indications = medication_data.get("indications") or "No information available."
        warnings = medication_data.get("warnings") or "No information available."
        side_effects = medication_data.get("side_effects") or "No information available."
        dosage = medication_data.get("dosage") or "No information available."

        # Build the text that will appear
        content = f"""BRAND NAME: {brand}
GENERIC NAME: {generic}

{'='*55}

WHAT IT IS USED FOR
{indications}

{'='*55}

WARNINGS
{warnings}

{'='*55}

SIDE EFFECTS
{side_effects}

{'='*55}

HOW TO TAKE IT
{dosage}
"""
        self.result_text.insert(tk.END, content)
        self.result_text.config(state="disabled")

        # Update status
        name = brand if brand != "—" else generic
        self.status_label.config(text=f"Showing results for: {name}")

    def show_message(self, message: str):
        """Show a simple message in the results area"""
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, message)
        self.result_text.config(state="disabled")

    # --------------------------------------------------
    # History Methods
    # --------------------------------------------------
    def load_history(self):
        """Load past searches and show them in the sidebar listbox"""
        self.history_listbox.delete(0, tk.END)

        if not os.path.exists(self.history_file):
            return

        try:
            with open(self.history_file, "r") as f:
                history = json.load(f)

            for item in history:
                name = item.get("brand_name") or item.get("generic_name") or item.get("query_name", "Unknown")
                time = item.get("timestamp", "")[:16]
                display = f"{name}  ({time})"
                self.history_listbox.insert(tk.END, display)

        except Exception as e:
            print("Could not load history:", e)

    def add_to_history(self, medication_data: dict):
        """
        Add a new search to the history file and refresh the sidebar.
        This is called after a successful search.
        """
        # Load existing history
        history = []
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r") as f:
                    history = json.load(f)
            except:
                history = []

        # Create entry
        entry = {
            "query_name": medication_data.get("query_name", ""),
            "brand_name": medication_data.get("brand_name"),
            "generic_name": medication_data.get("generic_name"),
            "indications": medication_data.get("indications", ""),
            "warnings": medication_data.get("warnings", ""),
            "side_effects": medication_data.get("side_effects", ""),
            "dosage": medication_data.get("dosage", ""),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
        }

        # Put newest at the top
        history.insert(0, entry)

        # Keep only last 30 searches
        history = history[:30]

        # Save
        with open(self.history_file, "w") as f:
            json.dump(history, f, indent=4)

        # Refresh the listbox
        self.load_history()

    def on_history_select(self, event):
        """When user clicks an item in the history list"""
        selection = self.history_listbox.curselection()
        if not selection:
            return

        index = selection[0]

        try:
            with open(self.history_file, "r") as f:
                history = json.load(f)

            if index < len(history):
                data = history[index]
                self.show_results(data)
                self.search_entry.delete(0, tk.END)
                self.search_entry.insert(0, data.get("query_name", ""))

        except Exception as e:
            messagebox.showerror("Error", f"Could not load that search.\n{e}")

    def clear_history(self):
        """Clear all history after asking the user"""
        confirm = messagebox.askyesno("Clear History", "Are you sure you want to delete all search history?")
        if confirm:
            with open(self.history_file, "w") as f:
                json.dump([], f)
            self.history_listbox.delete(0, tk.END)
            self.status_label.config(text="History cleared.")

    # --------------------------------------------------
    # Search button (placeholder - other members will connect the real search)
    # --------------------------------------------------
    def search_clicked(self):
        """
        This is called when the user clicks Search.
        For now it just shows a sample result so the display can be tested.
        Later your teammates will replace this with the real FDA + AI code.
        """
        query = self.search_entry.get().strip()

        if not query:
            messagebox.showwarning("Empty", "Please type a medication name first.")
            return

        # Sample data so you can test the display
        sample = {
            "query_name": query,
            "brand_name": query.title(),
            "generic_name": query.lower(),
            "indications": f"{query.title()} is commonly used to treat pain, inflammation, or other conditions. Always follow the instructions given by your doctor or pharmacist.",
            "warnings": "Do not take more than the recommended dose. Talk to your doctor if you are pregnant, breastfeeding, or have any medical conditions. Keep out of reach of children.",
            "side_effects": "Possible side effects include stomach upset, dizziness, headache, or allergic reactions. Contact a doctor if side effects are severe.",
            "dosage": "Take as directed on the package or by your healthcare provider. Do not exceed the maximum daily dose."
        }

        self.show_results(sample)
        self.add_to_history(sample)
        self.status_label.config(text=f"Results shown for: {query}")


# ---------- Run the window ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = DisplayBuilder(root)
    root.mainloop()
