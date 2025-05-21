import csv
import os
from datetime import datetime
from collections import defaultdict

def initialize_file():
    filename = 'expenses.csv'

    if not os.path.exists(filename) or os.stat(filename).st_size == 0:
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Amount", "Description"])
        print(f"Created or reset {filename} with headers.\n")

    

def add_expense():
    while True:
        date = input("Enter date (DD-MM-YYYY): ")
        try:
            date_obj = datetime.strptime(date, "%d-%m-%Y")
            break
        except ValueError:
            print("Invalid date format. Please use DD-MM-YYYY.\n")
    
    category = input("Enter category: ")
    try:
        amount = float(input("Enter amount (TL): "))
    except ValueError:
        print("WRONG!! Enter a number.")
        return
    description = input("Enter description if you want: ")
    
    with open('expenses.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount, description])
    print(f"✅ Expense of {amount:.2f} TL added successfully!\n")
    

def view_expenses():
    try:
        with open('expenses.csv', mode='r') as file:
            reader = csv.reader(file)
            next(reader)
            expenses = list(reader)
            
            if not expenses:
                print("No expenses found!\n")
                return
            
            print(".\nYour Expenses: ")
            print("-" * 50)
            for row in expenses:
                date, category, amount, description = row
                print(f"{date} | {category:<10} | {float(amount):>8.2f} TL | {description}")
            print("-"*50 + "\n")
    except FileNotFoundError:
        print("No expenses file found. Please add an expense.")
        

def show_summary():
    category_totals = defaultdict(float)

    try:
        with open('expenses.csv', mode='r') as file:
            reader = csv.DictReader(file)
            if reader.fieldnames != ["Date", "Category", "Amount", "Description"]:
                print("⚠️ CSV file format is invalid. Please check headers.\n")
                return

            for row in reader:
                category = row["Category"]
                try:
                    amount = float(row["Amount"])
                    category_totals[category] += amount
                except ValueError:
                    continue

        if not category_totals:
            print("No expenses to summarize.\n")
            return

        print("\nSummary by Category:")
        print("-" * 35)
        for category, total in category_totals.items():
            print(f"{category:<15} : {total:>8.2f} TL")
        print("-" * 35 + "\n")

    except FileNotFoundError:
        print("No expenses file found. Please add some expenses first.\n")

    pass


def remove_expense():
    try:
        with open('expenses.csv', mode='r') as file:
            reader=csv.reader(file)
            rows=list(reader)
            
        if len(rows) <= 1:
            print("No expenses to remove.\n")
            return
        
        print("\nExpenses:")
        print("-" * 60)
        for i, row in enumerate(rows[1:], start=1):  
            date, category, amount, description = row
            print(f"{i}. {date} | {category:<10} | {float(amount):>8.2f} TL | {description}")
        print("-" * 60)
        
        index = input("Enter the number of the expense to remove: ")
        if not index.isdigit() or not (1 <= int(index) < len(rows)):
            print("❌ Invalid selection.\n")
            return
        
        removed = rows.pop(int(index))
        with open('expenses.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

        print(f"✅ Removed: {removed[0]} | {removed[1]} | {removed[2]} TL | {removed[3]}\n")

    except FileNotFoundError:
        print("❌ No expense file found.\n")
        

def edit_expense():
    try:
        with open('expenses.csv', mode='r') as file:
            reader = csv.reader(file)
            rows = list(reader)

        if len(rows) <= 1:
            print("No expenses to edit.\n")
            return

        # Display all expenses
        print("\nExpenses:")
        print("-" * 60)
        for i, row in enumerate(rows[1:], start=1):
            date, category, amount, description = row
            print(f"{i}. {date} | {category:<10} | {float(amount):>8.2f} TL | {description}")
        print("-" * 60)

        # Ask which one to edit
        index = input("Enter the number of the expense to edit: ")
        if not index.isdigit() or not (1 <= int(index) < len(rows)):
            print("❌ Invalid selection.\n")
            return

        index = int(index)
        old_row = rows[index]

        # Prompt for new values (press enter to keep old)
        print("Leave a field blank to keep the current value.")
        new_date = input(f"Enter new date (YYYY-MM-DD) [{old_row[0]}]: ") or old_row[0]
        new_category = input(f"Enter new category [{old_row[1]}]: ") or old_row[1]
        
        new_amount_input = input(f"Enter new amount (TL) [{old_row[2]}]: ")
        new_amount = old_row[2]  # Default
        if new_amount_input:
            try:
                new_amount = str(float(new_amount_input))
            except ValueError:
                print("Invalid amount. Keeping previous value.")

        new_description = input(f"Enter new description [{old_row[3]}]: ") or old_row[3]

        # Update the selected row
        rows[index] = [new_date, new_category, new_amount, new_description]

        # Save changes
        with open('expenses.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

        print("✅ Expense updated successfully!\n")

    except FileNotFoundError:
        print("❌ No expenses file found.\n")


def main():
    initialize_file()
    while True:
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Summary by Category")
        print("4. Remove Expense")
        print("5. Edit Expense")
        print("6. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            show_summary()
        elif choice == '4':
            remove_expense()
        elif choice == '5':
            edit_expense()
        elif choice == '6':
            print("Exiting!!! See ya!!")
            break
        else:
            print("Invalid choice.")
            
if __name__ == "__main__":
    main()
            
