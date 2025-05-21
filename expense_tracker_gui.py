import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from datetime import datetime
from collections import defaultdict

CSV_FILE = 'expenses.csv'
edit_index = None  # to track the index of the item being edited

# Ensure CSV file exists with headers
def initialize_file():
    if not os.path.exists(CSV_FILE) or os.stat(CSV_FILE).st_size == 0:
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Amount", "Description"])

# Add expense to CSV
def add_expense(date, category, amount, description):
    try:
        datetime.strptime(date, "%d-%m-%Y")
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid date (DD-MM-YYYY) and amount.")
        return

    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount, description])
    messagebox.showinfo("Success", "Expense added successfully!")
    clear_fields()
    show_expenses()

# Clear input fields
def clear_fields():
    date_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    desc_entry.delete(0, tk.END)

# Display all expenses in the table
def show_expenses():
    for row in tree.get_children():
        tree.delete(row)

    try:
        with open(CSV_FILE, mode='r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                date, category, amount, description = row
                amount_with_unit = f"{float(amount):.2f} TL"
                tree.insert("", "end", values=(date, category, amount_with_unit, description))

    except:
        pass

# Remove selected expense
def remove_expense():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("No selection", "Please select an expense to remove.")
        return

    index = tree.index(selected[0])
    with open(CSV_FILE, mode='r') as file:
        rows = list(csv.reader(file))

    del rows[index + 1]  # Skip header

    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    show_expenses()
    messagebox.showinfo("Removed", "Expense removed successfully.")

# Load selected expense into fields for editing
def load_selected_for_edit():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("No selection", "Please select an expense to edit.")
        return

    global edit_index
    edit_index = tree.index(selected[0])
    values = tree.item(selected[0], 'values')

    date_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    desc_entry.delete(0, tk.END)

    date_entry.insert(0, values[0])
    category_entry.insert(0, values[1])
    amount_entry.insert(0, values[2])
    desc_entry.insert(0, values[3])

    add_button.config(text="Save Changes", command=save_edited_expense)

# Save changes to selected expense
def save_edited_expense():
    global edit_index
    try:
        new_date = date_entry.get()
        new_category = category_entry.get()
        new_amount = float(amount_entry.get())
        new_desc = desc_entry.get()
        datetime.strptime(new_date, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Invalid input", "Check date and amount format.")
        return

    with open(CSV_FILE, mode='r') as file:
        rows = list(csv.reader(file))

    rows[edit_index + 1] = [new_date, new_category, new_amount, new_desc]

    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    show_expenses()
    clear_fields()
    add_button.config(text="Add Expense", command=lambda: add_expense(
        date_entry.get(), category_entry.get(), amount_entry.get(), desc_entry.get()
    ))
    messagebox.showinfo("Updated", "Expense updated successfully.")

# Show summary by category
def show_summary():
    totals = defaultdict(float)
    try:
        with open(CSV_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                totals[row["Category"]] += float(row["Amount"])
    except:
        return

    summary_text = "\n".join([f"{cat}: {amt:.2f} TL" for cat, amt in totals.items()])
    messagebox.showinfo("Summary by Category", summary_text or "No data to summarize.")

# ---------------- GUI SETUP ----------------

initialize_file()
root = tk.Tk()
root.title("Expense Tracker")

# Input Form
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

tk.Label(input_frame, text="Date (DD-MM-YYYY):").grid(row=0, column=0, padx=5, pady=2)
tk.Label(input_frame, text="Category:").grid(row=1, column=0, padx=5, pady=2)
tk.Label(input_frame, text="Amount (TL):").grid(row=2, column=0, padx=5, pady=2)
tk.Label(input_frame, text="Description:").grid(row=3, column=0, padx=5, pady=2)

date_entry = tk.Entry(input_frame)
category_entry = tk.Entry(input_frame)
amount_entry = tk.Entry(input_frame)
desc_entry = tk.Entry(input_frame)

date_entry.grid(row=0, column=1, padx=5)
category_entry.grid(row=1, column=1, padx=5)
amount_entry.grid(row=2, column=1, padx=5)
desc_entry.grid(row=3, column=1, padx=5)

add_button = tk.Button(input_frame, text="Add Expense", command=lambda: add_expense(
    date_entry.get(), category_entry.get(), amount_entry.get(), desc_entry.get()
))
add_button.grid(row=4, column=0, columnspan=2, pady=10)

# Expense Table
tree = ttk.Treeview(root, columns=("Date", "Category", "Amount", "Description"), show="headings")
for col in ("Date", "Category", "Amount", "Description"):
    tree.heading(col, text=col)
    tree.column(col, width=120)
tree.pack(pady=10)

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=5)

tk.Button(button_frame, text="Show Summary", command=show_summary).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Remove Selected", command=remove_expense).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Edit Selected", command=load_selected_for_edit).grid(row=0, column=2, padx=5)

# Load existing data
show_expenses()

root.mainloop()
