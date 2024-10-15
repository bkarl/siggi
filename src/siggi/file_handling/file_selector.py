import tkinter as tk
from tkinter import filedialog, ttk, messagebox

from siggi.structs.file_parameters import FileParameters


class DataImportForm:
    def __init__(self):
        # Create the main application window
        self.root = tk.Tk()
        # Run the application
        # Create the main frame for the form
        self.root.title("Data Import Settings")
        self.root.geometry("400x300")

        # Variables to hold form data
        self.file_entry_var = tk.StringVar()
        self.samplerate_var = tk.StringVar(value="10e3")
        self.data_format_var = tk.StringVar()

        # Build the form
        self.create_widgets()

    def run(self):
        self.root.mainloop()

    def create_widgets(self):
        # File selection section
        file_label = ttk.Label(self.root, text="Select File:")
        file_label.pack(pady=5)
        file_entry = ttk.Entry(self.root, textvariable=self.file_entry_var, width=50, state='readonly')
        file_entry.pack(pady=5)
        file_button = ttk.Button(self.root, text="Browse...", command=self.browse_file)
        file_button.pack(pady=5)

        # Sample rate selection section
        samplerate_label = ttk.Label(self.root, text="Sample Rate (Hz):")
        samplerate_label.pack(pady=5)
        samplerate_entry = ttk.Entry(self.root, textvariable=self.samplerate_var)
        samplerate_entry.pack(pady=5)

        # Data format selection section
        data_format_label = ttk.Label(self.root, text="Data Format:")
        data_format_label.pack(pady=5)
        self.data_format_combobox = ttk.Combobox(self.root, values=["Real", "Complex"], state="readonly", textvariable=self.data_format_var)
        self.data_format_combobox.pack(pady=5)

        # OK button to finish the form
        ok_button = ttk.Button(self.root, text="OK", command=self.on_ok)
        ok_button.pack(pady=20)

    def browse_file(self):
        # Open a file dialog to select a file
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_entry_var.set(file_path)
            # Disable data format selection if the file ends with .npy
            if file_path.lower().endswith('.npy'):
                self.data_format_var.set('N/A')
                self.data_format_combobox.config(state='disabled')
            else:
                self.data_format_var.set('')
                self.data_format_combobox.config(state='normal')

    def on_ok(self):
        # Get the values from the form
        file_path = self.file_entry_var.get()
        sample_rate = self.samplerate_var.get()
        data_format = self.data_format_var.get()

        # Validate the form inputs
        if not file_path:
            messagebox.showerror("Error", "Please select a file.")
            return
        try:
            float(self.samplerate_var.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid sample rate.")
            return False
        if data_format not in ["Real", "Complex", "N/A"]:
            messagebox.showerror("Error", "Please select a valid data format.")
            return

        self.root.destroy()

    def get_file_parameters(self):
        # Return the selected values as a dictionary
        return FileParameters.create(fs=float(self.samplerate_var.get()), path=self.file_entry_var.get(), n_samples=0)
