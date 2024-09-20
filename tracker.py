import tkinter as tk
from tkinter import ttk, messagebox
import json

class FinanceTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Tracker")
        self.root.geometry('1260x600')
        self.transactions = {}
        self.add_new_frame_visible = False
        self.search_frame = None
        self.sort_by_column_frame = None
        self.balance_label = None
        self.create_widgets()
        self.load_transactions("transactions.json")
        self.create_sort_by_column_frame()

    def create_widgets(self):
        title_label = tk.Label(self.root, text='PERSONAL FINANCE TRACKER', font=('Calibri', 30, 'bold'), bg='Aqua', fg='Black', bd=10, relief='groove')
        title_label.pack(fill=tk.X)

        self.person_frame = tk.LabelFrame(self.root, text='Transaction Name', font=('Calibri', 18, 'bold'), bg='DarkCyan', fg='Black', bd=8, relief='groove')
        self.person_frame.pack(fill=tk.X, padx=10, pady=10)

        self.person_entry = tk.Entry(self.person_frame, font=('Calibri', 15), bd=7, width=40)
        self.person_entry.pack(side=tk.LEFT, padx=10)

        add_button = tk.Button(self.person_frame, text='Add Transaction', font=('Calibri', 18, 'bold'), activeforeground='Salmon', command=self.display_transactions)
        add_button.pack(side=tk.LEFT, padx=8)

        search_button = tk.Button(self.person_frame, text='Search Transaction', font=('Calibri', 18, 'bold'), activeforeground='Salmon', command=self.search_transactions)
        search_button.pack(side=tk.LEFT, padx=8)

        self.add_new_frame = tk.LabelFrame(self.root, text='Add New Transaction Detail', font=('Calibri', 18, 'bold'), bg='DarkCyan', fg='Black', bd=8, relief='groove')

        amount_label = tk.Label(self.add_new_frame, text='Enter the Amount of Transaction', font=('Calibri', 15))
        amount_label.grid(row=0, column=0, padx=10)
        self.amount_entry = tk.Entry(self.add_new_frame, font=('Calibri', 15), width=20)
        self.amount_entry.grid(row=0, column=1)

        account_label = tk.Label(self.add_new_frame, text='Choose The Type of Transaction', font=('Calibri', 15))
        account_label.grid(row=1, column=0, padx=10, pady=10)

        self.transaction_type_var = tk.StringVar()
        self.income_radio = tk.Radiobutton(self.add_new_frame, text="Income", variable=self.transaction_type_var, value="Income")
        self.expenses_radio = tk.Radiobutton(self.add_new_frame, text="Expenses", variable=self.transaction_type_var, value="Expense")
        self.transaction_type_var.set("Income")
        self.income_radio.grid(row=1, column=1)
        self.expenses_radio.grid(row=1, column=2)

        date_label = tk.Label(self.add_new_frame, text='Choose The Date of Transaction', font=('Calibri', 15))
        date_label.grid(row=2, column=0, padx=10, pady=10)

        year = list(range(2019, 2028))
        self.date_year_combobox = ttk.Combobox(self.add_new_frame, value=year, state="readonly")
        self.date_year_combobox.set("Year")
        self.date_year_combobox.grid(row=2, column=1, padx=2, pady=10)

        month = list(range(1, 13))
        self.date_month_combobox = ttk.Combobox(self.add_new_frame, value=month, state="readonly")
        self.date_month_combobox.set("Month")
        self.date_month_combobox.grid(row=2, column=2, padx=2, pady=10)

        day = list(range(1, 32))
        self.date_day_combobox = ttk.Combobox(self.add_new_frame, value=day, state="readonly")
        self.date_day_combobox.set("Day")
        self.date_day_combobox.grid(row=2, column=3, padx=10, pady=10)

        self.add_data_button = tk.Button(self.add_new_frame, text='Add Data', font=('Calibri', 18, 'bold'), activeforeground='Salmon', command=self.validate_and_add_data)
        self.cancel_button = tk.Button(self.add_new_frame, text='Cancel', font=('Calibri', 18, 'bold'), activeforeground='Salmon', command=self.cancel_add_data)

        self.add_data_button.grid(row=3, column=0, padx=8)
        self.cancel_button.grid(row=3, column=1, padx=8)

        self.add_new_frame.pack(fill=tk.X, padx=10, pady=10)
        self.add_new_frame.pack_forget()

    def load_transactions(self, filename):
        try:
            with open(filename, 'r') as file:
                self.transactions = json.load(file)
        except FileNotFoundError:
            self.transactions = {}

    def display_transactions(self):
        if self.sort_by_column_frame:
            self.sort_by_column_frame.pack_forget()

        self.add_new_frame.pack(fill=tk.X, padx=10, pady=10)
        self.add_new_frame_visible = True

        for widget in [self.person_frame.winfo_children()[1], self.person_frame.winfo_children()[2]]:
            widget.config(state='disabled')

    def validate_and_add_data(self):
        person_entry_value = self.person_entry.get().capitalize()
        amount_entry_value = self.amount_entry.get()
        account_value = self.transaction_type_var.get()
        date_value = f"{self.date_year_combobox.get()}-{self.date_month_combobox.get()}-{self.date_day_combobox.get()}"

        try:
            amount_entry_value = float(amount_entry_value)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid amount.")
            return

        if person_entry_value not in self.transactions:
            self.transactions[person_entry_value] = []
        self.transactions[person_entry_value].append({"amount": amount_entry_value, "account": account_value, "date": date_value})

        with open("transactions.json", "w") as file:
            json.dump(self.transactions, file, indent=4)

        messagebox.showinfo("Success", "Transaction added successfully.")

        self.person_entry.delete(0, 'end')
        self.amount_entry.delete(0, 'end')
        self.transaction_type_var.set("Income")
        self.date_year_combobox.set("Year")
        self.date_month_combobox.set("Month")
        self.date_day_combobox.set("Day")

        for widget in [self.person_frame.winfo_children()[1], self.person_frame.winfo_children()[2]]:
            widget.config(state='normal')

        self.add_new_frame.pack_forget()
        self.add_new_frame_visible = False

        self.create_sort_by_column_frame()

    def search_transactions(self):
        def close_search_frame():
            if self.search_frame:
                self.search_frame.pack_forget()
                self.person_entry.delete(0, tk.END)

        if self.sort_by_column_frame:
            self.sort_by_column_frame.pack_forget()

        query = self.person_entry.get().capitalize()
        if query in self.transactions:
            if self.search_frame:
                self.search_frame.destroy()
            self.search_frame = tk.Frame(self.root)
            self.search_frame.pack(fill=tk.X, padx=10, pady=10)

            tree = ttk.Treeview(self.search_frame, columns=("Amount", "Account", "Date"), show='headings')
            tree.heading("Amount", text="Amount")
            tree.heading("Account", text="Account")
            tree.heading("Date", text="Date")
            tree.pack(fill=tk.X)

            for data in self.transactions[query]:
                account_type = "Income" if data["account"] == "Income" else "Expense"
                tree.insert("", tk.END, values=(data["amount"], account_type, data.get("date", "")))

            close_button = tk.Button(self.search_frame, text='Close', font=('Calibri', 18, 'bold'), activeforeground='Salmon', command=close_search_frame)
            close_button.pack(side=tk.BOTTOM)

        else:
            messagebox.showinfo("Transaction Not Found", f"No transaction found with the name '{query}'.")
            self.create_sort_by_column_frame()

    def create_sort_by_column_frame(self):
        if self.sort_by_column_frame:
            self.sort_by_column_frame.destroy()

        self.sort_by_column_frame = tk.LabelFrame(self.root, text='Transaction Detail', font=('Calibri', 18, 'bold'), bg='DarkCyan', fg='Black', bd=8, relief='groove')
        self.sort_by_column_frame.pack(fill=tk.X, padx=10, pady=10)

        self.tree = ttk.Treeview(self.sort_by_column_frame, columns=("Transaction Name", "Amount", "Account", "Date"), show='headings')
        self.tree.heading("Transaction Name", text="Transaction Name")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Account", text="Account")
        self.tree.heading("Date", text="Date")
        self.tree.pack(fill=tk.BOTH, expand=1)

        self.balance_label = tk.Label(self.sort_by_column_frame, text="Balance: Rs 0.00", font=('Calibri', 16), bg='DarkCyan', fg='White')
        self.balance_label.pack(pady=5)

        self.update_balance()

        for name, details in self.transactions.items():
            for data in details:
                account_type = "Income" if data["account"] == "Income" else "Expense"
                date_value = data.get("date", "")
                self.tree.insert("", tk.END, values=(name, data["amount"], account_type, date_value))

        delete_button = tk.Button(self.sort_by_column_frame, text="Delete", command=self.delete_transaction)
        delete_button.pack(side=tk.RIGHT, padx=5)
        
        update_button = tk.Button(self.sort_by_column_frame, text="Update", command=self.update_transaction)
        update_button.pack(side=tk.RIGHT, padx=5)

    def update_balance(self):
        balance = 0.0
        for name, details in self.transactions.items():
            for data in details:
                if data["account"] == "Income":
                    balance += data["amount"]
                else:
                    balance -= data["amount"]
        self.balance_label.config(text=f"Balance: Rs. {balance:.2f}")

    def delete_transaction(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select a transaction to delete.")
            return

        confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete this transaction?")
        if not confirmation:
            return

        for item in selected_items:
            values = self.tree.item(item, "values")
            if not values:
                continue

            transaction_name = values[0]
            amount = float(values[1])
            account = "Income" if values[2] == "Income" else "Expense"
            date = values[3]

            if transaction_name in self.transactions:
                transactions = self.transactions[transaction_name]
                for transaction in transactions:
                    if transaction["amount"] == amount and transaction["account"] == account and transaction.get("date", "") == date:
                        transactions.remove(transaction)
                        if not transactions:
                            del self.transactions[transaction_name]
                        self.tree.delete(item)
                        break

        with open("transactions.json", "w") as file:
            json.dump(self.transactions, file, indent=4)

        messagebox.showinfo("Success", "Transaction deleted successfully.")
        self.update_balance()

    def update_transaction(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select a transaction to update.")
            return

        for item in selected_items:
            values = self.tree.item(item, "values")
            if not values:
                continue

            transaction_name = values[0]
            amount = float(values[1])
            account = "Income" if values[2] == "Income" else "Expense"
            date = values[3]

            update_dialog = tk.Toplevel(self.root)
            update_dialog.title("Update Transaction")

            amount_label = tk.Label(update_dialog, text="New Amount:", font=('Calibri', 15))
            amount_label.grid(row=0, column=0, padx=10, pady=5)
            amount_entry = tk.Entry(update_dialog, font=('Calibri', 15), width=20)
            amount_entry.grid(row=0, column=1)
            amount_entry.insert(tk.END, str(amount))

            account_label = tk.Label(update_dialog, text="Account Type:", font=('Calibri', 15))
            account_label.grid(row=1, column=0, padx=10, pady=5)

            transaction_type_var = tk.StringVar()
            income_radio = tk.Radiobutton(update_dialog, text="Income", variable=transaction_type_var, value="Income")
            expenses_radio = tk.Radiobutton(update_dialog, text="Expenses", variable=transaction_type_var, value="Expense")
            transaction_type_var.set(account)
            income_radio.grid(row=1, column=1)
            expenses_radio.grid(row=1, column=2)

            ok_button = tk.Button(update_dialog, text="OK", font=('Calibri', 14, 'bold'), command=lambda: update_dialog_ok())
            ok_button.grid(row=2, column=0, columnspan=3, pady=10)

            def update_dialog_ok():
                new_amount = amount_entry.get()
                new_account = transaction_type_var.get()

                try:
                    new_amount = float(new_amount)
                except ValueError:
                    messagebox.showerror("Invalid Input", "Please enter a valid numerical amount.")
                    return

                updated_transaction = {"amount": new_amount, "account": new_account, "date": date}

                if transaction_name in self.transactions:
                    transactions = self.transactions[transaction_name]
                    for transaction in transactions:
                        if transaction["amount"] == amount and transaction["account"] == account and transaction.get("date", "") == date:
                            transaction.update(updated_transaction)
                            break

                with open("transactions.json", "w") as file:
                    json.dump(self.transactions, file, indent=4)

                messagebox.showinfo("Success", "Transaction(s) updated successfully.")
                update_dialog.destroy()
                self.update_balance()

    def cancel_add_data(self):
        self.person_entry.delete(0, 'end')
        self.amount_entry.delete(0, 'end')
        self.transaction_type_var.set("Income")
        self.date_year_combobox.set("Year")
        self.date_month_combobox.set("Month")
        self.date_day_combobox.set("Day")

        for widget in [self.person_frame.winfo_children()[1], self.person_frame.winfo_children()[2]]:
            widget.config(state='normal')

        self.add_new_frame.pack_forget()
        self.add_new_frame_visible = False

        self.create_sort_by_column_frame()

def main():
    root = tk.Tk()
    app = FinanceTrackerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
