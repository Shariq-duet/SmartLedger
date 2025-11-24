⭐ SmartLedger — Python-Based Accounting System for Small Businesses

A lightweight, offline, command-line accounting system built using core Python, following double-entry bookkeeping principles. SmartLedger helps small and medium-sized businesses (SMBs) manage accounts, record transactions, track ledgers, and generate automated financial reports — all without databases or internet.

📌 Features Overview
✔️ Account Management

Create and categorize accounts (Assets, Liabilities, Expenses, Revenue, Owner’s Equity)

Validates unique account names

Stores accounts in data/accounts.json

✔️ Journal Entry Recording

Record debit–credit entries with validation (debits = credits)

Auto-generates unique IDs (JE-YYYYMMDD-XXX)

Saves entries in data/journal_entries.json

✔️ Automated Ledger Posting

Updates running balances

Maintains full transaction history per account

Saves data to data/ledger_data.json

✔️ Report Generation

Trial Balance

Income Statement

Balance Sheet

Cash Flow Statement

Ratio Analysis (Profit Margin, Current Ratio, Debt Ratio)

Reports saved under:

data/reports/

✔️ Completely Offline

Uses only JSON and CSV files

No external database required

Works on any system with Python installed

🏗️ Project Structure
smartledger/
│
├── main.py              # Main CLI interface
├── accounts.py          # Account creation & management
├── journal.py           # Journal entry recording
├── ledger.py            # Ledger updates & calculations
├── reports.py           # Report generation
├── utils.py             # File I/O, validation, helpers
│
└── data/
    ├── accounts.json
    ├── journal_entries.json
    ├── ledger_data.json
    └── reports/
        ├── trial_balance.txt
        ├── income_statement.txt
        ├── balance_sheet.txt
        └── cashflow.txt

🚀 How to Run the Application
1. Install Python (3.8+)

Check version:

python --version

2. Clone the Repository
git clone https://github.com/YOUR-USERNAME/SmartLedger.git
cd SmartLedger

3. Run SmartLedger
python main.py

🖥️ Main Menu (CLI Interface)
SMARTLEDGER MAIN MENU
=============================================

1. Create Account
2. Record Journal Entry
3. View Ledger for Account
4. Generate Reports
5. Exit

Enter your choice (1–5):

📊 Reports Included
➡ Trial Balance

Ensures total debits = total credits

➡ Income Statement

Revenue

Expenses

Net profit/loss

➡ Balance Sheet

Assets

Liabilities

Owner’s Equity

➡ Cash Flow Statement

Operating

Investing

Financing activities

➡ Ratio Analysis

Profit Margin

Current Ratio

Debt Ratio

🔧 Tech Details
Storage Format

JSON for accounts, journals, and ledger

TXT output for reports

CSV compatibility possible in future updates

Error Handling

Prevents unbalanced entries

Handles missing data files

Auto-backup support (via utils)

📦 Future Enhancements

GUI using Tkinter or Streamlit

User authentication

Export reports to PDF

Multi-business support

📘 Financial Terms (Quick Reference)
Term	Meaning
Asset	What the company owns
Liability	What the company owes
Revenue	Money earned
Expense	Cost incurred
Debit	Increases Assets/Expenses
Credit	Increases Liabilities/Revenue
Ledger	History of all transactions
Trial Balance	Ensures Dr = Cr
Income Statement	Profit/Loss
Balance Sheet	Snapshot of financial position
👥 Author

Developed by: EXP MS7
Client: Fintrix Technologies
Version: 1.0# SmartLedger
