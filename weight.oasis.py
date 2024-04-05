import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import os

# Constants for BMI categories
BMI_CATEGORIES = {
    (0, 18.5): "Underweight",
    (18.5, 24.9): "Normal weight",
    (25, 29.9): "Overweight",
    (30, float('inf')): "Obese"
}

class BMIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator")

        # Initialize user data
        self.user_data = self.load_user_data()

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Style
        style = ttk.Style()
        style.configure('TButton', font=('calibri', 12, 'bold'), borderwidth='4')
        style.configure('TLabel', font=('calibri', 14, 'bold'))
        style.configure('Title.TLabel', font=('calibri', 24, 'bold'))
        
        # Frame
        self.frame = ttk.Frame(self.root, padding=(20, 10))
        self.frame.grid(row=0, column=0)

        # Title
        self.label_title = ttk.Label(self.frame, text="BMI Calculator", style='Title.TLabel')
        self.label_title.grid(row=0, columnspan=2, pady=10)

        # Labels
        self.label_name = ttk.Label(self.frame, text="Name:")
        self.label_name.grid(row=1, column=0, padx=10, pady=10, sticky='e')

        self.label_weight = ttk.Label(self.frame, text="Weight (kg):")
        self.label_weight.grid(row=2, column=0, padx=10, pady=10, sticky='e')

        self.label_height = ttk.Label(self.frame, text="Height (m):")
        self.label_height.grid(row=3, column=0, padx=10, pady=10, sticky='e')

        # Entry fields
        self.entry_name = ttk.Entry(self.frame, font=('calibri', 12))
        self.entry_name.grid(row=1, column=1, padx=10, pady=10)

        self.entry_weight = ttk.Entry(self.frame, font=('calibri', 12))
        self.entry_weight.grid(row=2, column=1, padx=10, pady=10)

        self.entry_height = ttk.Entry(self.frame, font=('calibri', 12))
        self.entry_height.grid(row=3, column=1, padx=10, pady=10)

        # Calculate BMI button
        self.btn_calculate = ttk.Button(self.frame, text="Calculate BMI", command=self.calculate_bmi)
        self.btn_calculate.grid(row=4, columnspan=2, pady=10)

        # BMI result label
        self.label_result = ttk.Label(self.frame, text="")
        self.label_result.grid(row=5, columnspan=2, pady=10)

        # Add user button
        self.btn_add_user = ttk.Button(self.frame, text="Add User", command=self.add_user)
        self.btn_add_user.grid(row=6, column=0, padx=10, pady=10, sticky='w')

        # View history button
        self.btn_view_history = ttk.Button(self.frame, text="View History", command=self.view_history)
        self.btn_view_history.grid(row=6, column=1, padx=10, pady=10, sticky='e')

    def calculate_bmi(self):
        try:
            weight = float(self.entry_weight.get())
            height = float(self.entry_height.get())

            if weight <= 0 or height <= 0:
                messagebox.showerror("Error", "Weight and height must be positive numbers.")
                return

            bmi = weight / (height ** 2)
            self.display_bmi_result(bmi)
            self.save_bmi_data(self.entry_name.get(), bmi)

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numerical values for weight and height.")

    def display_bmi_result(self, bmi):
        for category_range, category_name in BMI_CATEGORIES.items():
            if category_range[0] <= bmi < category_range[1]:
                result_text = f"Your BMI is {bmi:.2f}, which is {category_name}."
                self.label_result.config(text=result_text)
                break

    def add_user(self):
        # Save current user's BMI data
        self.save_bmi_data(self.entry_name.get(), None)

        # Reset input fields
        self.entry_weight.delete(0, tk.END)
        self.entry_height.delete(0, tk.END)
        self.entry_name.delete(0, tk.END)
        self.label_result.config(text="")

    def view_history(self):
        # Plot BMI history for the selected user
        user_name = self.entry_name.get()
        bmi_history = self.user_data["bmi_history"].get(user_name, [])
        if bmi_history:
            dates = list(range(1, len(bmi_history) + 1))
            plt.plot(dates, bmi_history)
            plt.xlabel("Days")
            plt.ylabel("BMI")
            plt.title(f"BMI History for {user_name}")
            plt.grid(True)
            plt.show()
        else:
            messagebox.showinfo("Info", f"No BMI history available for {user_name}.")

    def save_bmi_data(self, user_name, bmi):
        # Save BMI data for the current user
        if "bmi_history" not in self.user_data:
            self.user_data["bmi_history"] = {}
        if user_name not in self.user_data["bmi_history"]:
            self.user_data["bmi_history"][user_name] = []
        if bmi is not None:
            self.user_data["bmi_history"][user_name].append(bmi)
        self.save_user_data()

    def save_user_data(self):
        # Save user data to file
        with open("user_data.json", "w") as file:
            json.dump(self.user_data, file)

    def load_user_data(self):
        # Load user data from file, if exists
        if os.path.exists("user_data.json"):
            with open("user_data.json", "r") as file:
                return json.load(file)
        else:
            return {"bmi_history": {}}

if __name__ == "__main__":
    root = tk.Tk()
    app = BMIApp(root)
    root.mainloop()
