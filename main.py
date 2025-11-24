from datetime import datetime

from accounts import create_account, load_accounts
from journal import create_journal_entry, get_journal_entries
from ledger import get_account_ledger, post_journal_entry_to_ledger
from report import (
    generate_trial_balance,
    generate_income_statement,
    generate_balance_sheet,
    generate_cash_flow,
    generate_ratio_analysis
)

def main():
    while True:
        print("\nSMARTLEDGER MAIN MENU ================================")
        print("1. Create Account")
        print("2. Record Journal Entry")
        print("3. View Ledger for Account")
        print("4. Generate Reports")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ").strip()
        if choice == "1":
            create_account_cli()
        elif choice == "2":
            record_journal_entry_cli()
        elif choice == "3":
            view_ledger_cli()
        elif choice == "4":
            generate_reports_cli()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-5.")

def create_account_cli():
    print("\n--- Create New Account ---")
    name = input("Account name: ").strip()
    account_type = input("Account type (Asset, Liability, Revenue, Expense, Owner's Equity): ").strip()
    initial_balance = input("Initial balance (leave blank for 0): ").strip()
    
    if not name:
        print("Account name is required.")
        return
    
    try:
        initial_balance = float(initial_balance) if initial_balance else 0.0
    except ValueError:
        print("Invalid balance. Using 0.0")
        initial_balance = 0.0
    
    success, message = create_account(name, account_type, initial_balance)
    print(message)     

def record_journal_entry_cli():
    print("\n--- Record Journal Entry ---")
    date = input("Date (YYYY-MM-DD): ").strip()
    narration = input("Narration: ").strip()

    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
        print(f"Using today's date: {date}")

    debits = []
    credits = []

    print("\nEnter debit lines (blank account to stop):")
    while True:
        account = input("  Debit account: ").strip()
        if not account:
            break
        amount = input("  Amount: ").strip()
        try:
            amount = float(amount)
        except ValueError:
            print("  Invalid amount, try again.")
            continue
        debits.append({"account": account, "amount": amount})

    print("\nEnter credit lines (blank account to stop):")
    while True:
        account = input("  Credit account: ").strip()
        if not account:
            break
        amount = input("  Amount: ").strip()
        try:
            amount = float(amount)
        except ValueError:
            print("  Invalid amount, try again.")
            continue
        credits.append({"account": account, "amount": amount})

    success, je_id, message = create_journal_entry(date, narration, debits, credits)
    print(message)

    if success:
        journal_entries = get_journal_entries()
        entry = journal_entries.get(je_id)
        ledger_success, ledger_message = post_journal_entry_to_ledger(je_id, entry)
        print("Ledger:", ledger_message if ledger_success else f"Ledger error: {ledger_message}")

def view_ledger_cli():
    print("\n--- Account Ledger ---")
    account_name = input("Account name: ").strip()
    if not account_name:
        print("Account name is required.")
        return

    ledger_entries = get_account_ledger(account_name)
    if ledger_entries is None:
        print(f"Account '{account_name}' not found.")
        return

    if not ledger_entries:
        print(f"No transactions for '{account_name}'.")
        return

    print(f"\nLedger for {account_name}:")
    print("-" * 60)
    for entry in ledger_entries:
        date = entry.get("date", "")
        je_id = entry.get("je_id", "")
        entry_type = entry.get("entry_type", "")
        amount = entry.get("amount", 0)
        running = entry.get("running_balance", 0)
        print(f"{date} | {je_id} | {entry_type:<6} | Amount: {amount:.2f} | Balance: {running:.2f}")

def generate_reports_cli():
    print("\n--- Generate Reports ---")
    print("1. Trial Balance")
    print("2. Income Statement")
    print("3. Balance Sheet")
    print("4. Cash Flow Statement")
    print("5. Ratio Analysis")
    print("6. Back to Main Menu")
    report_choice = input("Choose a report (1-6): ").strip()

    report_map = {
        "1": ("Trial Balance", generate_trial_balance),
        "2": ("Income Statement", generate_income_statement),
        "3": ("Balance Sheet", generate_balance_sheet),
        "4": ("Cash Flow Statement", generate_cash_flow),
        "5": ("Ratio Analysis", generate_ratio_analysis),
    }

    if report_choice == "6":
        return

    if report_choice not in report_map:
        print("Invalid report choice.")
        return

    report_name, report_fn = report_map[report_choice]
    print(f"\nGenerating {report_name}...")
    success, data, message = report_fn()
    print(message)
    if success and data:
        display_report_summary(report_name, data)
        
def display_report_summary(report_name, data):
    if report_name == "Trial Balance":
        print(f"Total Debits: {data['total_debits']:.2f}")
        print(f"Total Credits: {data['total_credits']:.2f}")
        print("Balanced" if data["is_balanced"] else "Not balanced")
    elif report_name == "Income Statement":
        print(f"Revenue: {data['total_revenue']:.2f}")
        print(f"Expenses: {data['total_expenses']:.2f}")
        print(f"Net Income: {data['net_income']:.2f}")
    elif report_name == "Balance Sheet":
        print(f"Assets: {data['total_assets']:.2f}")
        print(f"Liabilities: {data['total_liabilities']:.2f}")
        print(f"Equity: {data['total_equity']:.2f}")
        print("Balanced" if data["is_balanced"] else "Not balanced")
    elif report_name == "Cash Flow Statement":
        print(f"Operating: {data['operating_cash']:.2f}")
        print(f"Investing: {data['investing_cash']:.2f}")
        print(f"Financing: {data['financing_cash']:.2f}")
        print(f"Net Cash Flow: {data['net_cash_flow']:.2f}")
    elif report_name == "Ratio Analysis":
        print(f"Profit Margin: {data['profit_margin']:.2f}%")
        print(f"Debt Ratio: {data['debt_ratio']:.2f}%")
        print(f"ROA: {data['roa']:.2f}%")
        print(f"ROE: {data['roe']:.2f}%")            


if __name__ == "__main__":
    main()