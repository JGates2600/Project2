import sys
import csv
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel,
                             QComboBox, QTableWidget, QTableWidgetItem, QWidget, QFileDialog, QMessageBox, QBoxLayout,
                             QLineEdit)
from PyQt6.QtCore import Qt

#sets up first gui window to input income
class IncomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enter Income")
        self.setGeometry(300, 300, 250, 150)

        self.layout = QVBoxLayout()

        self.label = QLabel("Enter Income")
        self.layout.addWidget(self.label)

        self.income_input = QLineEdit()
        self.layout.addWidget(self.income_input)

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_window)
        self.layout.addWidget(self.next_button)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    #validates input and opens next window if it passes - positive numbers only
    def next_window(self):
        try:
            self.income = float(self.income_input.text())
            if self.income < 0:
                raise ValueError("Income cannot be negative")

            self.expense_window = ExpenseWindow(self.income)
            self.expense_window.show()
            self.close()
        except ValueError:
            QMessageBox.warning(self, "Error", "Enter a positive number for Income")


#sets up the second GUI window to select from a dropdown and input expenses
class ExpenseWindow(QMainWindow):
    def __init__(self, income):
        super().__init__()
        self.income = income
        self.expenses = []

        self.setWindowTitle("Enter Expenses")
        self.setGeometry(300, 300, 250, 150)

        self.layout = QVBoxLayout()

        self.label = QLabel("Select Expenses and Enter Amount")
        self.layout.addWidget(self.label)

        self.category_dropdown = QComboBox()
        self.category_dropdown.addItems(["Rent", "Utilities", "Food/Drink", "Other"])
        self.layout.addWidget(self.category_dropdown)

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Enter Amount")
        self.layout.addWidget(self.amount_input)

        self.add_button = QPushButton("Add Expense")
        self.add_button.clicked.connect(self.add_expense)
        self.layout.addWidget(self.add_button)

        self.next_button = QPushButton("Calculate Budget")
        self.next_button.clicked.connect(self.next_window)
        self.layout.addWidget(self.next_button)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    #validates expense amount/ category - appends list and clears input field
    def add_expense(self):
        try:
            amount = float (self.amount_input.text())
            if amount <= 0:
                raise ValueError("Amount cannot be negative")

            category = self.category_dropdown.currentText()
            self.expenses.append((category, amount))
            QMessageBox.information(self, "Expenses", "Expenses added successfully")
            self.amount_input.clear()
        except ValueError:
            QMessageBox.warning(self, "Error", "Enter a positive number for Amount")

    #opens the final results window
    def next_window(self):
        self.result_window = ResultWindow(self.income, self.expenses)
        self.result_window.show()
        self.close()

#sets up the final results window to summarize income, expenses and balance based on previous input - also diplays via table
class ResultWindow(QMainWindow):
    def __init__(self, income, expenses):
        super().__init__()
        self.income = income
        self.expenses = expenses

        self.setWindowTitle("Results")
        self.setGeometry(300, 300, 250, 150)

        self.layout = QVBoxLayout()

        #Income/expense summary
        self.income_label = QLabel(f"Total Income: {self.income:.2f}")
        self.layout.addWidget(self.income_label)

        total_expenses = sum(amount for _, amount in self.expenses)
        self.expenses_label = QLabel(f"Total Expenses: {total_expenses:.2f}")
        self.layout.addWidget(self.expenses_label)

        balance = self.income - total_expenses
        self.balance_label = QLabel(f"Balance: {balance:.2f}")
        self.layout.addWidget(self.balance_label)

        #expense table
        self.expense_table = QTableWidget()
        self.expense_table.setRowCount(len(self.expenses))
        self.expense_table.setColumnCount(2)
        self.expense_table.setHorizontalHeaderLabels(["Category", "Amount"])

        for i, (category, amount) in enumerate(self.expenses):
            self.expense_table.setItem(i, 0, QTableWidgetItem(category))
            self.expense_table.setItem(i, 1, QTableWidgetItem(f"$ {amount:.2f}"))

        self.layout.addWidget(self.expense_table)

        #save button
        self.save_button = QPushButton("Save Results to CSV")
        self.save_button.clicked.connect(self.save_to_csv)
        self.layout.addWidget(self.save_button)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    #provides the option to save the results via csv
    def save_to_csv(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "CSV (*.csv)")

        if file_path:
            try:
                with open(file_path, "w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(["Category", "Amount"])
                    writer.writerows(self.expenses)

                QMessageBox.information(self, "Results", "File saved successfully")
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e))




#launches the application - starts GUI loop
if __name__ == '__main__':
    app = QApplication(sys.argv)
    income_window = IncomeWindow()
    income_window.show()
    sys.exit(app.exec())



