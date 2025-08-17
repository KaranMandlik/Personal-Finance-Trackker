import requests

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
        self.api_url = "https://financialmodelingprep.com/api/v3/stock/list"  # Correct API URL for stock list
        self.api_key = "wNkXnjqKPr7v5GBSfIrnFT62RGP5dTMK"  # Replace with your actual API key

    def add_income(self, amount):
        """Add income to the tracker."""
        if amount > 0:
            self.income += amount
            print(f"Income of {amount} added.")
        else:
            print("Invalid income amount.")

    def add_expense(self, category, amount):
        """Add an expense to a specific category."""
        if category in self.expenses and amount > 0:
            self.expenses[category] += amount
            print(f"{category} expense of {amount} added.")
        else:
            print("Invalid category or expense amount.")

    def view_summary(self):
        """Display a summary of income and expenses."""
        total_expenses = sum(self.expenses.values())
        remaining_balance = self.income - total_expenses
        
        print("\n--- Personal Finance Summary ---")
        print(f"Total Income: {self.income}")
        print(f"Total Expenses: {total_expenses}")
        print(f"Remaining Balance: {remaining_balance}")
        
        print("\nExpense Breakdown:")
        for category, amount in self.expenses.items():
            print(f"{category}: {amount}")

        # Suggest investments if remaining balance is greater than a threshold
        if remaining_balance > 1000:  # If remaining balance is over 1000, suggest investments
            print("\nBased on your savings, here are some investment suggestions:")
            self.suggest_investments(remaining_balance)
        else:
            print("\nYou don't have enough savings for investment suggestions.")

    def suggest_investments(self, remaining_balance):
        """Fetch investment suggestions based on the saved money (remaining balance)."""
        try:
            # Correct URL to include API key for authentication
            response = requests.get(f"{self.api_url}?apikey={self.api_key}")
            response.raise_for_status()
            data = response.json()

            # Just an example to show available stocks; in a real scenario, you may filter based on certain criteria
            if data and len(data) > 0:
                print(f"Investment Suggestions for your remaining balance of {remaining_balance}:")
                for i, stock in enumerate(data[:5]):  # Limit to first 5 stocks for simplicity
                    print(f"{i + 1}. Stock: {stock['symbol']} - Name: {stock['name']}")
            else:
                print("No investment suggestions available.")
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred while fetching investment data: {http_err}")
        except Exception as err:
            print(f"An error occurred while fetching investment data: {err}")

def main():
    tracker = PersonalFinanceTracker()

    while True:
        print("\nPersonal Finance Tracker")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Summary")
        print("4. Suggest Investments")
        print("5. Exit")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            income_amount = float(input("Enter income amount: "))
            tracker.add_income(income_amount)
        elif choice == '2':
            print("Expense Categories: Home Rent, EMI, Life Insurance, Groceries, Other")
            category = input("Enter expense category: ")
            expense_amount = float(input("Enter expense amount: "))
            tracker.add_expense(category, expense_amount)
        elif choice == '3':
            tracker.view_summary()
        elif choice == '4':
            remaining_balance = tracker.income - sum(tracker.expenses.values())  # Calculate remaining balance
            tracker.suggest_investments(remaining_balance)  # Pass the calculated balance to the method
        elif choice == '5':
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
