import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
import string
import pyperclip

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")

        # Variables
        self.length_var = tk.IntVar()
        self.lower_var = tk.BooleanVar()
        self.upper_var = tk.BooleanVar()
        self.digit_var = tk.BooleanVar()
        self.symbol_var = tk.BooleanVar()

        # Default values
        self.length_var.set(12)
        self.lower_var.set(True)
        self.upper_var.set(True)
        self.digit_var.set(True)
        self.symbol_var.set(True)

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Frame
        self.frame = ttk.Frame(self.root, padding=20, style='My.TFrame')
        self.frame.grid(row=0, column=0)

        # Title
        self.label_title = ttk.Label(self.frame, text="Password Generator", font=('Arial', 18, 'bold'), style='Title.TLabel')
        self.label_title.grid(row=0, columnspan=2, pady=10)

        # Password length
        self.label_length = ttk.Label(self.frame, text="Password Length:", style='Label.TLabel')
        self.label_length.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        self.entry_length = ttk.Entry(self.frame, textvariable=self.length_var, width=5, style='Entry.TEntry')
        self.entry_length.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        # Complexity options
        self.label_complexity = ttk.Label(self.frame, text="Complexity:", style='Label.TLabel')
        self.label_complexity.grid(row=2, column=0, padx=10, pady=5, sticky='w')

        self.check_lower = ttk.Checkbutton(self.frame, text="Lowercase Letters", variable=self.lower_var, style='Checkbutton.TCheckbutton')
        self.check_lower.grid(row=3, column=0, padx=10, pady=5, sticky='w')

        self.check_upper = ttk.Checkbutton(self.frame, text="Uppercase Letters", variable=self.upper_var, style='Checkbutton.TCheckbutton')
        self.check_upper.grid(row=4, column=0, padx=10, pady=5, sticky='w')

        self.check_digit = ttk.Checkbutton(self.frame, text="Digits", variable=self.digit_var, style='Checkbutton.TCheckbutton')
        self.check_digit.grid(row=5, column=0, padx=10, pady=5, sticky='w')

        self.check_symbol = ttk.Checkbutton(self.frame, text="Symbols", variable=self.symbol_var, style='Checkbutton.TCheckbutton')
        self.check_symbol.grid(row=6, column=0, padx=10, pady=5, sticky='w')

        # Generate button
        self.btn_generate = ttk.Button(self.frame, text="Generate Password", command=self.generate_password, style='Button.TButton')
        self.btn_generate.grid(row=7, column=0, columnspan=2, pady=10)

        # Generated password
        self.label_password = ttk.Label(self.frame, text="", style='Result.TLabel')
        self.label_password.grid(row=8, column=0, columnspan=2, pady=10)

        # Copy to clipboard button
        self.btn_copy = ttk.Button(self.frame, text="Copy to Clipboard", command=self.copy_to_clipboard, style='Button.TButton')
        self.btn_copy.grid(row=9, column=0, columnspan=2, pady=5)

        # Center the window
        self.root.eval('tk::PlaceWindow %s center' % self.root.winfo_toplevel())

    def generate_password(self):
        length = self.length_var.get()
        password = self.generate_random_password(length)
        self.label_password.config(text=password)

    def generate_random_password(self, length):
        characters = ''
        if self.lower_var.get():
            characters += string.ascii_lowercase
        if self.upper_var.get():
            characters += string.ascii_uppercase
        if self.digit_var.get():
            characters += string.digits
        if self.symbol_var.get():
            characters += string.punctuation

        if not characters:
            messagebox.showerror("Error", "Please select at least one character type.")
            return ""

        password = ''.join(random.choice(characters) for _ in range(length))
        return password

    def copy_to_clipboard(self):
        password = self.label_password.cget("text")
        pyperclip.copy(password)
        messagebox.showinfo("Success", "Password copied to clipboard.")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x400")
    style = ttk.Style(root)
    style.theme_use('clam')

    style.configure('My.TFrame', background='#e3e3e3')
    style.configure('Title.TLabel', font=('Arial', 18, 'bold'), background='#e3e3e3')
    style.configure('Label.TLabel', background='#e3e3e3')
    style.configure('Entry.TEntry', background='#f0f0f0')
    style.configure('Checkbutton.TCheckbutton', background='#e3e3e3')
    style.configure('Button.TButton', font=('Arial', 10, 'bold'), background='#4CAF50', foreground='white')
    style.configure('Result.TLabel', font=('Arial', 12), background='#e3e3e3')

    app = PasswordGenerator(root)
    root.mainloop()
