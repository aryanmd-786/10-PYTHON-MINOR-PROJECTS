import tkinter as tk
from tkinter import ttk, messagebox
import json
import os


class ExpenseTracker:

    def __init__(self, root):

        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("850x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#F3F4F6")

        self.file_name = "transactions.json"
        self.transactions = []

        self.load_data()

        # ==================================================
        # HEADER
        # ==================================================

        header = tk.Frame(
            root,
            bg="#1E3A8A",
            height=90
        )
        header.pack(fill="x")

        title = tk.Label(
            header,
            text="PERSONAL EXPENSE TRACKER",
            font=("Arial", 23, "bold"),
            bg="#1E3A8A",
            fg="white"
        )
        title.pack(pady=25)

        # ==================================================
        # SUMMARY CARDS
        # ==================================================

        summary_frame = tk.Frame(
            root,
            bg="#F3F4F6"
        )
        summary_frame.pack(
            fill="x",
            padx=25,
            pady=20
        )

        # Income
        income_frame = tk.Frame(
            summary_frame,
            bg="#DCFCE7",
            width=240,
            height=90
        )
        income_frame.pack(
            side="left",
            expand=True,
            fill="both",
            padx=5
        )
        income_frame.pack_propagate(False)

        tk.Label(
            income_frame,
            text="TOTAL INCOME",
            font=("Arial", 11, "bold"),
            bg="#DCFCE7",
            fg="#166534"
        ).pack(pady=(15, 5))

        self.income_label = tk.Label(
            income_frame,
            text="₹0.00",
            font=("Arial", 20, "bold"),
            bg="#DCFCE7",
            fg="#166534"
        )
        self.income_label.pack()

        # Expense
        expense_frame = tk.Frame(
            summary_frame,
            bg="#FEE2E2",
            width=240,
            height=90
        )
        expense_frame.pack(
            side="left",
            expand=True,
            fill="both",
            padx=5
        )
        expense_frame.pack_propagate(False)

        tk.Label(
            expense_frame,
            text="TOTAL EXPENSE",
            font=("Arial", 11, "bold"),
            bg="#FEE2E2",
            fg="#991B1B"
        ).pack(pady=(15, 5))

        self.expense_label = tk.Label(
            expense_frame,
            text="₹0.00",
            font=("Arial", 20, "bold"),
            bg="#FEE2E2",
            fg="#991B1B"
        )
        self.expense_label.pack()

        # Balance
        balance_frame = tk.Frame(
            summary_frame,
            bg="#DBEAFE",
            width=240,
            height=90
        )
        balance_frame.pack(
            side="left",
            expand=True,
            fill="both",
            padx=5
        )
        balance_frame.pack_propagate(False)

        tk.Label(
            balance_frame,
            text="BALANCE",
            font=("Arial", 11, "bold"),
            bg="#DBEAFE",
            fg="#1E40AF"
        ).pack(pady=(15, 5))

        self.balance_label = tk.Label(
            balance_frame,
            text="₹0.00",
            font=("Arial", 20, "bold"),
            bg="#DBEAFE",
            fg="#1E40AF"
        )
        self.balance_label.pack()

        # ==================================================
        # INPUT SECTION
        # ==================================================

        input_frame = tk.LabelFrame(
            root,
            text=" Add Transaction ",
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#1E3A8A",
            padx=15,
            pady=12
        )
        input_frame.pack(
            fill="x",
            padx=25,
            pady=5
        )

        # Description
        tk.Label(
            input_frame,
            text="Description:",
            font=("Arial", 10, "bold"),
            bg="white"
        ).grid(
            row=0,
            column=0,
            padx=8,
            pady=8
        )

        self.description_entry = tk.Entry(
            input_frame,
            font=("Arial", 10),
            width=23
        )
        self.description_entry.grid(
            row=0,
            column=1,
            padx=8
        )

        # Amount
        tk.Label(
            input_frame,
            text="Amount:",
            font=("Arial", 10, "bold"),
            bg="white"
        ).grid(
            row=0,
            column=2,
            padx=8
        )

        self.amount_entry = tk.Entry(
            input_frame,
            font=("Arial", 10),
            width=15
        )
        self.amount_entry.grid(
            row=0,
            column=3,
            padx=8
        )

        # Category
        tk.Label(
            input_frame,
            text="Category:",
            font=("Arial", 10, "bold"),
            bg="white"
        ).grid(
            row=1,
            column=0,
            padx=8,
            pady=8
        )

        self.category_box = ttk.Combobox(
            input_frame,
            values=[
                "Food",
                "Travel",
                "Shopping",
                "Education",
                "Bills",
                "Entertainment",
                "Health",
                "Other"
            ],
            state="readonly",
            width=20
        )
        self.category_box.grid(
            row=1,
            column=1,
            padx=8
        )
        self.category_box.set("Food")

        # Type
        tk.Label(
            input_frame,
            text="Type:",
            font=("Arial", 10, "bold"),
            bg="white"
        ).grid(
            row=1,
            column=2,
            padx=8
        )

        self.type_box = ttk.Combobox(
            input_frame,
            values=[
                "Income",
                "Expense"
            ],
            state="readonly",
            width=13
        )
        self.type_box.grid(
            row=1,
            column=3,
            padx=8
        )
        self.type_box.set("Expense")

        # Add button
        add_button = tk.Button(
            input_frame,
            text="ADD TRANSACTION",
            font=("Arial", 10, "bold"),
            bg="#2563EB",
            fg="white",
            width=20,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.add_transaction
        )
        add_button.grid(
            row=0,
            column=4,
            rowspan=2,
            padx=15
        )

        # ==================================================
        # TRANSACTION TABLE
        # ==================================================

        table_frame = tk.LabelFrame(
            root,
            text=" Transaction History ",
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#1E3A8A",
            padx=10,
            pady=10
        )
        table_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=10
        )

        columns = (
            "Description",
            "Category",
            "Type",
            "Amount"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=9
        )

        self.table.heading(
            "Description",
            text="Description"
        )

        self.table.heading(
            "Category",
            text="Category"
        )

        self.table.heading(
            "Type",
            text="Type"
        )

        self.table.heading(
            "Amount",
            text="Amount"
        )

        self.table.column(
            "Description",
            width=250
        )

        self.table.column(
            "Category",
            width=150,
            anchor="center"
        )

        self.table.column(
            "Type",
            width=120,
            anchor="center"
        )

        self.table.column(
            "Amount",
            width=150,
            anchor="center"
        )

        self.table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.table.configure(
            yscrollcommand=scrollbar.set
        )

        # ==================================================
        # BOTTOM BUTTONS
        # ==================================================

        bottom_frame = tk.Frame(
            root,
            bg="#F3F4F6"
        )
        bottom_frame.pack(
            pady=10
        )

        delete_button = tk.Button(
            bottom_frame,
            text="DELETE SELECTED",
            font=("Arial", 10, "bold"),
            bg="#DC2626",
            fg="white",
            width=18,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.delete_transaction
        )
        delete_button.grid(
            row=0,
            column=0,
            padx=8
        )

        clear_button = tk.Button(
            bottom_frame,
            text="CLEAR ALL",
            font=("Arial", 10, "bold"),
            bg="#F59E0B",
            fg="white",
            width=15,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.clear_all
        )
        clear_button.grid(
            row=0,
            column=1,
            padx=8
        )

        # Display existing data
        self.refresh_table()

    # ==================================================
    # ADD TRANSACTION
    # ==================================================

    def add_transaction(self):

        description = self.description_entry.get().strip()
        amount = self.amount_entry.get().strip()
        category = self.category_box.get()
        transaction_type = self.type_box.get()

        if description == "":
            messagebox.showwarning(
                "Missing Information",
                "Please enter a description."
            )
            return

        try:
            amount = float(amount)

            if amount <= 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Invalid Amount",
                "Please enter a valid positive amount."
            )
            return

        transaction = {
            "description": description,
            "amount": amount,
            "category": category,
            "type": transaction_type
        }

        self.transactions.append(transaction)

        self.save_data()
        self.refresh_table()

        self.description_entry.delete(
            0,
            tk.END
        )

        self.amount_entry.delete(
            0,
            tk.END
        )

    # ==================================================
    # REFRESH TABLE
    # ==================================================

    def refresh_table(self):

        for item in self.table.get_children():
            self.table.delete(item)

        total_income = 0
        total_expense = 0

        for transaction in self.transactions:

            amount = transaction["amount"]

            if transaction["type"] == "Income":
                total_income += amount

            else:
                total_expense += amount

            self.table.insert(
                "",
                tk.END,
                values=(
                    transaction["description"],
                    transaction["category"],
                    transaction["type"],
                    f"₹{amount:.2f}"
                )
            )

        balance = total_income - total_expense

        self.income_label.config(
            text=f"₹{total_income:.2f}"
        )

        self.expense_label.config(
            text=f"₹{total_expense:.2f}"
        )

        self.balance_label.config(
            text=f"₹{balance:.2f}"
        )

    # ==================================================
    # DELETE TRANSACTION
    # ==================================================

    def delete_transaction(self):

        selected = self.table.selection()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select a transaction."
            )
            return

        index = self.table.index(
            selected[0]
        )

        del self.transactions[index]

        self.save_data()
        self.refresh_table()

    # ==================================================
    # CLEAR ALL
    # ==================================================

    def clear_all(self):

        if not self.transactions:
            messagebox.showinfo(
                "No Data",
                "There are no transactions."
            )
            return

        answer = messagebox.askyesno(
            "Clear All",
            "Are you sure you want to delete all transactions?"
        )

        if answer:

            self.transactions.clear()

            self.save_data()
            self.refresh_table()

    # ==================================================
    # SAVE DATA
    # ==================================================

    def save_data(self):

        try:

            with open(
                self.file_name,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    self.transactions,
                    file,
                    indent=4
                )

        except OSError:

            messagebox.showerror(
                "Error",
                "Unable to save transaction data."
            )

    # ==================================================
    # LOAD DATA
    # ==================================================

    def load_data(self):

        if not os.path.exists(self.file_name):
            self.transactions = []
            return

        try:

            with open(
                self.file_name,
                "r",
                encoding="utf-8"
            ) as file:

                self.transactions = json.load(file)

        except (json.JSONDecodeError, OSError):

            self.transactions = []


# ==================================================
# MAIN
# ==================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = ExpenseTracker(root)

    root.mainloop()