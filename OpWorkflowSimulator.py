import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import csv

def initialize_csv():
    try:
        with open("transaction_log.csv", mode="x", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Account Status", "Amount", "Country", "Decision"])
    except FileExistsError:
        pass 

def process_transaction():
    account_status = account_entry.get().strip().lower()
    country = country_entry.get().strip().title()
    try:
        amount = float(amount_entry.get().strip())
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number for amount.")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if account_status != "yes":
        decision = "Rejected - Inactive Account"
    else:
        high_risk_countries = ["North Korea", "Iran", "Syria", "Russia"]
        high_value = amount > 100000
        is_high_risk = country in high_risk_countries

        if high_value and is_high_risk:
            decision = "Escalated - High Risk + High Value"
        elif high_value:
            decision = "Hold - High Value"
        elif is_high_risk:
            decision = "Escalated - High Risk Country"
        else:
            decision = "Approved"

    
    messagebox.showinfo("Decision", f"Transaction Decision:\n{decision}")

    with open("transaction_log.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, account_status, amount, country, decision])

    # Clear inputs
    account_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    country_entry.delete(0, tk.END)

# Initialize CSV file
initialize_csv()

# GUI Setup
window = tk.Tk()
window.title("Operations Workflow Simulator")
window.geometry("400x300")

tk.Label(window, text="Account Active? (yes/no):").pack(pady=5)
account_entry = tk.Entry(window)
account_entry.pack()

tk.Label(window, text="Transaction Amount (INR):").pack(pady=5)
amount_entry = tk.Entry(window)
amount_entry.pack()

tk.Label(window, text="Client Country:").pack(pady=5)
country_entry = tk.Entry(window)
country_entry.pack()

tk.Button(window, text="Process Transaction", command=process_transaction, bg="#C6176E", fg="white").pack(pady=20)

window.mainloop()
