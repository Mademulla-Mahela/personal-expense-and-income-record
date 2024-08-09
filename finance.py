import json
from datetime import datetime

DATE_FORMAT = "%Y-%m-%d"

# Global dictionary to store transactions
transactions = {}

# global constants for menu choices
READ_TRANSACTION = 1
ADD_TRANSACTION = 2
VIEW_TRANSACTION = 3
UPDATE_TRANSACTION = 4
DELETE_TRANSACTION = 5
DISPLAY_TRANSACTION = 6
QUIT = 7


def main_menu():
    # print choices on the screen
    print()
    print('----------MENU------------')
    print()
    print('1) Read transaction')
    print('2) Add transaction')
    print('3) View transaction')
    print('4) Update transaction')
    print('5) Delete transaction')
    print('6) Display transaction summary')
    print('7) Quit')

    # choice variable controls the loop
    choice = 0

    while choice != QUIT:
        try:
            # get the user choices
            choice = int(input('Enter your choice from menu: '))
            # perform the selection action
            if choice == READ_TRANSACTION:
                read_bulk_transactions()
            elif choice == ADD_TRANSACTION:
                add_to_dictionary()
            elif choice == VIEW_TRANSACTION:
                view_transactions()
            elif choice == UPDATE_TRANSACTION:
                update_transaction()
            elif choice == DELETE_TRANSACTION:
                delete_transaction()
            elif choice == DISPLAY_TRANSACTION:
                display_summary()
            elif choice == QUIT:
                print('Exiting from the program...')
            else:
                print('Please select a number from the menu..!!!')

        except ValueError:
            print("Please enter an integer...!!!")
            continue


# File handling functions
def load_transactions():
    try:
        with open('Transaction.json', 'r') as objects:
            return json.load(objects)
    except FileNotFoundError:
        print('Sorry...!!!\nFile does not exist in the computer...!!!')


def save_transactions():
    with open('Transaction.json', 'w') as stringfile:
        json.dump(transactions, stringfile)


def read_bulk_transactions():
    global transactions

    try:
        with open('transaction.json', 'r') as file:
            for line in file:
                cleared_string = line.strip().split(',')
                print(f'\nCleared String - {cleared_string}')

                if len(cleared_string) >= 4:  # Ensure there are enough elements
                    category, amount, date, i_e_type = cleared_string[:4]

                    # Validate category
                    if not category:
                        print('Category cannot be empty')
                        continue
                    elif category.isdigit():
                        print('Transaction category cannot be a numeral value')
                        continue

                    # Validate amount
                    try:
                        amount = float(amount)
                    except ValueError:
                        print('Amount must be a numeric value')
                        continue
                    # Validate date
                    try:
                        date_conversion = datetime.strptime(date, DATE_FORMAT).date()
                        date_string = date_conversion.strftime(DATE_FORMAT)
                    except ValueError:
                        print('Invalid Date format')
                        continue

                    # Validate income/expense type
                    if i_e_type.lower() not in ['income', 'expense']:
                        print('Invalid income/expense type')
                        continue

                    # Construct transaction data
                    data = {'amount': amount, 'date': date_string, 'type': i_e_type}

                    # Update transactions dictionary
                    transactions.setdefault(category.capitalize(), []).append(data)

            # Save transactions after processing all lines
            save_transactions()
            print('Transactions Added to the JSON file from the text file ')
    except FileNotFoundError:
        print("File not found. Please make sure the file exists.")


def add_to_dictionary():
    global transactions
    # Input transaction description
    description = input("Enter transaction description: ")

    # Input transaction date
    date = input("Enter a date (YYYY-MM-DD): ")
    while True:
        try:
            year = int(date[0:4])  # Extract year from date input
            month = int(date[5:7])  # Extract month from date input
            day = int(date[8:10])  # Extract day from date input
            if 1 <= month <= 12 and 1 <= day <= 31:  # Validate month and day
                break
            else:
                print("Invalid date format. Please check and enter again.")  # If invalid, prompt for input again
                date = input("Enter a date (YYYY-MM-DD): ")
        except (ValueError, IndexError):
            print("Invalid date format.")
            date = input("Enter a date (YYYY-MM-DD): ")

    # Input transaction type
    Type = input("Enter 'e' for Expense or 'i' for Income: ")
    while True:
        if Type.lower() == 'e':
            transaction_type = "Expense"  # Convert input to Expense string
            break
        elif Type.lower() == 'i':
            transaction_type = "Income"  # Convert input to Income string
            break
        else:
            print("Invalid input.")
            Type = input("Enter 'e' for Expense or 'i' for Income again: ")

    try:
        # Input transaction amount
        amount = float(input("Enter transaction amount: "))
        if amount <= 0:
            print("Amount must be greater than 0")
            return
    except ValueError:
        print("Invalid amount input.")
        add_to_dictionary()
        return

    # Create a list for transaction values
    transaction_values = {"amount": amount, "type": transaction_type, "date": date}

    # Add transaction values to the transactions dictionary
    transactions.setdefault(description, []).append(transaction_values)

    # Save transactions to file
    save_transactions()


def view_transactions():
    if transactions:  # Check if transactions list is not empty
        for description, transaction_list in transactions.items():  # Loop through transactions
            for transaction_data in transaction_list:
                transaction_dict = {
                    'Amount': transaction_data['amount'],
                    'Description': description,
                    'Type': transaction_data['type']
                }
                if 'date' in transaction_data:
                    transaction_dict['Date'] = transaction_data['date']
                else:
                    transaction_dict['Date'] = 'Not specified'

                print(', '.join([f'{key}: {value}' for key, value in transaction_dict.items()]))
    else:
        print("No transactions available.")  # If transactions list is empty, print message


def update_transaction():
    view_transactions()  # Display transactions for reference
    if transactions:  # Check if transactions dictionary is not empty
        try:
            while True:
                description = input(
                    "Enter the description of transaction to update: ")  # Input description of transaction to update
                if description in transactions:
                    break
                else:
                    print("Transaction not found. Please enter a valid description.")

            transaction_list = transactions[description]  # Get the transaction data list for the given description

            try:
                amount = float(input("Enter transaction amount: "))  # Input transaction amount
                if amount <= 0:
                    print("Amount must be greater than 0")
                    return
            except ValueError:
                print("Invalid amount.")
                return

            Type = input("Enter 'e' for Expense or 'i' for Income: ")  # Input new transaction type
            while True:
                if Type.lower() == 'e':
                    transaction_type = "Expense"  # Convert input to Expense string
                    break
                elif Type.lower() == 'i':
                    transaction_type = "Income"  # Convert input to Income string
                    break
                else:
                    print("Invalid input")
                    Type = input("Enter 'e' for Expense or 'i' for Income again: ")

            date = input("Enter a date (YYYY-MM-DD): ")  # Input new transaction date
            while True:
                try:
                    year = int(date[0:4])  # Extract year from date input
                    month = int(date[5:7])  # Extract month from date input
                    day = int(date[8:10])  # Extract day from date input
                    if 1 <= month <= 12 and 1 <= day <= 31:  # Validate month and day
                        break
                    else:
                        print("Invalid date. Please enter again.")
                        date = input("Enter a date (YYYY-MM-DD): ")
                except ValueError:
                    print("Invalid date format.")
                    date = input("Enter a date (YYYY-MM-DD): ")

            # Update transaction data list
            for transaction_data in transaction_list:
                transaction_data.update({"amount": amount, "type": transaction_type, "date": date})

            save_transactions()  # Save transactions to file
            print("Transaction updated successfully.")  # Print success message
        except Exception as e:
            print("Error:", e)  # Print error message if any exception occurs
    else:
        print("No transactions available to update.")  # If transactions dictionary is empty, print message


def delete_transaction():
    view_transactions()  # Display transactions for reference
    if transactions:  # Check if transactions dictionary is not empty
        try:
            while True:
                description = input(
                    "Enter the description of transaction to delete: ")  # Input description of transaction to delete
                if description in transactions:
                    break
                else:
                    print("Transaction not found. Please enter a valid description.")

            del transactions[description]  # Delete transaction from transactions dictionary
            save_transactions()  # Save transactions to file
            print("Transaction deleted successfully.")  # Print success message
        except Exception as e:
            print("Error:", e)  # Print error message if any exception occurs
    else:
        print("No transactions available to delete.")  # If transactions dictionary is empty, print message


def display_summary():
    total_income = 0
    total_expense = 0

    for transaction_list in transactions.values():
        for transaction_data in transaction_list:
            if 'type' in transaction_data and 'amount' in transaction_data:
                if transaction_data['type'] == 'Income':
                    total_income += transaction_data['amount']
                elif transaction_data['type'] == 'Expense':
                    total_expense += transaction_data['amount']

    total_balance = total_income - total_expense
    print(f"Total income: {total_income}")
    print(f"Total expense: {total_expense}")
    print(f"Balance: {total_balance}")


if __name__ == "__main__":
    main_menu()
