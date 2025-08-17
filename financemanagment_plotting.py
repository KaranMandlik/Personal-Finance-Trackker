import requests
import matplotlib.pyplot as plt

class PersonalFinanceTracker:
    def __init__(self):
        self.income = 0
        self.expenses = {
            "Home Rent": 0,
            "EMI": 0,
            "Life Insurance": 0,
            "Groceries": 0,
            "Other": 0
        }
        self.api_url = "https://financialmodelingprep.com/api/v3/stock/list"
        self.api_key = "wNkXnjqKPr7v5GBSfIrnFT62RGP5dTMK"  # Replace with your actual API key

    def add_income(self, amount):
        if amount > 0:
            self.income += amount
            print(f"Income of {amount} added.")
        else:
            print("Invalid income amount.")

    def add_expense(self):
        print("\nChoose an Expense Category:")
        categories = list(self.expenses.keys())
        for i, category in enumerate(categories, start=1):
            print(f"{i}. {category}")
        
        choice = int(input("Enter the number corresponding to the category: "))
        if 1 <= choice <= len(categories):
            category = categories[choice - 1]
            amount = float(input(f"Enter amount for {category}: "))
            if amount > 0:
                self.expenses[category] += amount
                print(f"{category} expense of {amount} added.")
            else:
                print("Invalid amount.")
        else:
            print("Invalid choice.")

    def view_expenses(self):
        print("\n--- Expense Breakdown ---")
        for category, amount in self.expenses.items():
            print(f"{category}: {amount}")
        
        print("\n1. Edit Expense\n2. Return to Main Menu")
        sub_choice = input("Enter your choice: ")
        if sub_choice == '1':
            category = input("Enter the category to edit: ")
            if category in self.expenses:
                new_amount = float(input(f"Enter new amount for {category}: "))
                self.expenses[category] = new_amount
                print(f"{category} updated to {new_amount}.")
            else:
                print("Invalid category.")

    def view_summary(self):
        total_expenses = sum(self.expenses.values())
        remaining_balance = self.income - total_expenses
        
        print("\n--- Personal Finance Summary ---")
        print(f"Total Income: {self.income}")
        print(f"Total Expenses: {total_expenses}")
        print(f"Remaining Balance: {remaining_balance}")
        
        self.view_expenses()

        if remaining_balance > 1000:
            print("\nBased on your savings, here are some investment suggestions:")
            self.suggest_investments(remaining_balance)
        else:
            print("\nYou don't have enough savings for investment suggestions.")
        
        self.visualize_data()

    def suggest_investments(self, remaining_balance):
        try:
            response = requests.get(f"{self.api_url}?apikey={self.api_key}")
            response.raise_for_status()
            data = response.json()

            if data and len(data) > 0:
                print(f"Investment Suggestions for your remaining balance of {remaining_balance}:")
                for i, stock in enumerate(data[:5]):
                    print(f"{i + 1}. Stock: {stock['symbol']} - Name: {stock['name']}")
            else:
                print("No investment suggestions available.")
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")

    def visualize_data(self):
        categories = list(self.expenses.keys())
        expenses = list(self.expenses.values())

        plt.figure(figsize=(10, 6))
        plt.bar(categories, expenses, color='orange', label='Expenses')
        plt.axhline(y=self.income, color='green', linestyle='--', label='Income')

        plt.xlabel('Categories')
        plt.ylabel('Amount (in $)')
        plt.title('Income vs. Expenses')
        plt.legend()
        plt.grid(axis='y')
        plt.show()


def main():
    tracker = PersonalFinanceTracker()

    while True:
        print("\nPersonal Finance Tracker")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Summary (with Visualization)")
        print("4. View Expenses")
        print("5. Suggest Investments")
        print("6. Exit")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            income_amount = float(input("Enter income amount: "))
            tracker.add_income(income_amount)
        elif choice == '2':
            tracker.add_expense()
        elif choice == '3':
            tracker.view_summary()
        elif choice == '4':
            tracker.view_expenses()
        elif choice == '5':
            remaining_balance = tracker.income - sum(tracker.expenses.values())
            tracker.suggest_investments(remaining_balance)
        elif choice == '6':
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
