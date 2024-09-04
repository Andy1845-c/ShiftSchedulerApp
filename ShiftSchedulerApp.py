import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class ShiftSchedulerApp:
    def __init__(self, root):
        # Initialize the main window
        self.root = root
        self.root.title("Shift Scheduler and Bonus Calculator")
        self.shifts = []  # List to store shift details

        # Set background color for the window
        self.root.configure(bg='pink')  # background color

        # Create and place widgets for employee name input
        tk.Label(root, text="Employee Name:", bg='lightgray', fg='darkorange').grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.employee_entry = tk.Entry(root, bg='white', bd=2, relief='groove')
        self.employee_entry.grid(row=0, column=1, padx=10, pady=10)

        # Create and place widgets for date input
        tk.Label(root, text="Date (YYYY-MM-DD):", bg='lightgray', fg='darkorange').grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.date_entry = tk.Entry(root, bg='white', bd=2, relief='groove')
        self.date_entry.grid(row=1, column=1, padx=10, pady=10)

        # Create and place widgets for start time input
        tk.Label(root, text="Start Time (HH:MM):", bg='lightgray', fg='darkorange').grid(row=2, column=0, padx=10, pady=10, sticky='e')
        self.start_entry = tk.Entry(root,bg='white', bd=2, relief='groove')
        self.start_entry.grid(row=2, column=1, padx=10, pady=10)

        # Create and place widgets for end time input
        tk.Label(root, text="End Time (HH:MM):", bg='lightgray', fg='darkorange').grid(row=3, column=0, padx=10, pady=10, sticky='e')
        self.end_entry = tk.Entry(root, bg='white', bd=2, relief='groove')
        self.end_entry.grid(row=3, column=1, padx=10, pady=10)

        # Button to add a shift entry
        self.add_shift_button = tk.Button(root, text="Add Shift", command=self.add_shift, bg='lightcoral', fg='white', relief='raised')
        self.add_shift_button.grid(row=4, column=0, columnspan=2, pady=10, ipadx=5)

        # Create and place widgets for maximum hours per week input
        tk.Label(root, text="Maximum Hours per Week:", bg='lightgray', fg='darkorange').grid(row=5, column=0, padx=10, pady=10, sticky='e')
        self.max_hours_entry = tk.Entry(root,  bg='white', bd=2, relief='groove')
        self.max_hours_entry.grid(row=5, column=1, padx=10, pady=10)

        # Create and place widgets for bonus per hour input
        tk.Label(root, text="Bonus per Hour:", bg='lightgray',  fg='darkorange').grid(row=6, column=0, padx=10, pady=10, sticky='e')
        self.bonus_entry = tk.Entry(root,  bg='white', bd=2, relief='groove')
        self.bonus_entry.grid(row=6, column=1, padx=10, pady=10)

        # Button to calculate results
        self.calculate_button = tk.Button(root, text="Calculate", command=self.calculate, bg='tomato', fg='white', relief='raised')
        self.calculate_button.grid(row=7, column=0, columnspan=2, pady=10, ipadx=5)

        # Button to show help
        self.help_button = tk.Button(root, text="Help", command=self.show_help, bg='salmon', fg='white', relief='raised')
        self.help_button.grid(row=8, column=0, columnspan=2, pady=10, ipadx=5)

    def add_shift(self):
        # Retrieve and validate input values
        employee = self.employee_entry.get()
        date = self.date_entry.get()
        start = self.start_entry.get()
        end = self.end_entry.get()

        if not (employee and date and start and end):
            messagebox.showerror("Input Error", "All fields must be filled out.")
            return

        try:
            # Validate date and time format
            datetime.strptime(date, '%Y-%m-%d')
            datetime.strptime(start, '%H:%M')
            datetime.strptime(end, '%H:%M')
        except ValueError:
            messagebox.showerror("Input Error", "Date or time format is incorrect.")
            return

        # Add shift to the list
        self.shifts.append({'employee': employee, 'day': date, 'start': start, 'end': end})
        messagebox.showinfo("Success", "Shift added successfully!")

        # Clear input fields
        self.employee_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.start_entry.delete(0, tk.END)
        self.end_entry.delete(0, tk.END)

    def calculate(self):
        try:
            # Retrieve and validate maximum hours and bonus
            max_hours_per_week = float(self.max_hours_entry.get())
            bonus_per_hour = float(self.bonus_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Maximum hours and bonus must be numbers.")
            return

        # Compute hours worked, identify overworked employees, and calculate bonuses
        hours_worked = self.compute_hours_worked()
        overworked_employees = self.identify_overworked_employees(hours_worked, max_hours_per_week)
        bonuses = self.calculate_bonuses(hours_worked, bonus_per_hour)

        # Create result text to display
        result_text = "Total Hours Worked by Each Employee:\n"
        for employee, hours in hours_worked.items():
            result_text += f"{employee}: {hours:.2f} hours\n"

        result_text += "\nEmployees Who Worked More Than Maximum Allowed Hours:\n"
        for employee, hours in overworked_employees.items():
            result_text += f"{employee}: {hours:.2f} hours\n"

        result_text += "\nBonuses for Each Employee:\n"
        for employee, bonus in bonuses.items():
            result_text += f"{employee}: R{bonus:.2f}\n"

        # Show the results in a message box
        messagebox.showinfo("Results", result_text)

    def show_help(self):
        help_text = (
            "Welcome to the Shift Scheduler and Bonus Calculator!\n\n"
            "1. Enter the employee's name, date, start time, and end time for each shift.\n"
            "2. Click 'Add Shift' to save the shift details.\n"
            "3. Enter the maximum hours an employee can work per week and the bonus per hour.\n"
            "4. Click 'Calculate' to see the total hours worked, identify overworked employees, and calculate bonuses.\n"
            "5. If you need further assistance, feel free to ask for help again."
        )
        messagebox.showinfo("Help", help_text)

    def calculate_hours(self, start_time, end_time):
        # Calculate hours worked between start and end times
        start = datetime.strptime(start_time, '%H:%M')
        end = datetime.strptime(end_time, '%H:%M')
        delta = end - start
        return delta.seconds / 3600

    def compute_hours_worked(self):
        # Compute total hours worked for each employee
        hours_worked = {}
        for shift in self.shifts:
            employee = shift['employee']
            hours = self.calculate_hours(shift['start'], shift['end'])
            if employee in hours_worked:
                hours_worked[employee] += hours
            else:
                hours_worked[employee] = hours
        return hours_worked

    def identify_overworked_employees(self, hours_worked, max_hours):
        # Identify employees who worked more than the maximum allowed hours
        overworked = {emp: hours for emp, hours in hours_worked.items() if hours > max_hours}
        return overworked

    def calculate_bonuses(self, hours_worked, bonus_per_hour):
        # Calculate bonuses for each employee based on hours worked
        bonuses = {emp: hours * bonus_per_hour for emp, hours in hours_worked.items()}
        return bonuses

# Create the main window and start the application
root = tk.Tk()
app = ShiftSchedulerApp(root)
root.mainloop()
