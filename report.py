"""
Reports & Analytics Module - Generate accounting reports
"""
from utils import (
    load_json, save_json, REPORTS_DIR, format_currency
)
from accounts import load_accounts
from ledger import load_ledger_data, get_account_ledger
from journal import load_journal_entries
from datetime import datetime

def generate_trial_balance():
    """
    Generate Trial Balance report
    
    Returns:
        Tuple (success: bool, report_data: dict, message: str)
    """
    accounts_data = load_accounts()
    trial_balance = []
    total_debits = 0.0
    total_credits = 0.0
    
    for account_name, account_data in accounts_data.items():
        account_type = account_data.get("type")
        balance = account_data.get("balance", 0.0)

        if account_type in ["Asset", "Expense"]:
            debit_balance = balance if balance >= 0 else 0.0
            credit_balance = abs(balance) if balance < 0 else 0.0
        else:  # Liability, Revenue, Owner's Equity
            debit_balance = abs(balance) if balance < 0 else 0.0
            credit_balance = balance if balance >= 0 else 0.0
        
        trial_balance.append({
            "account": account_name,
            "type": account_type,
            "debit": debit_balance,
            "credit": credit_balance
        })
        total_debits += debit_balance
        total_credits += credit_balance
    
    # Sort by account name (AFTER the loop!)
    trial_balance.sort(key=lambda x: x["account"])
    
    # Create report data dictionary
    report_data = {
        "trial_balance": trial_balance,
        "total_debits": total_debits,
        "total_credits": total_credits,
        "is_balanced": abs(total_debits - total_credits) < 0.01
    }
    
    # Save to file
    report_file = REPORTS_DIR / "trial_balance.txt"
    report_text = format_trial_balance_text(report_data)
    
    try:
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_text)
        return True, report_data, "Trial Balance generated successfully"
    except IOError as e:
        return False, report_data, f"Failed to save report: {e}"

def format_trial_balance_text(report_data):
    """Format trial balance as text"""
    lines = []
    # Header
    lines.append("=" * 80)
    lines.append("TRIAL BALANCE")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("=" * 80)
    
    # Column headers
    lines.append(f"{'Account':<40} {'Type':<20} {'Debit':>15} {'Credit':>15}")
    lines.append("-" * 80)
    
    # Account rows
    for entry in report_data["trial_balance"]:
        # Only show debit or credit if > 0
        debit_str = format_currency(entry["debit"]) if entry["debit"] > 0 else ""
        credit_str = format_currency(entry["credit"]) if entry["credit"] > 0 else ""
        lines.append(f"{entry['account']:<40} {entry['type']:<20} {debit_str:>15} {credit_str:>15}")
    
    # Totals row
    lines.append("-" * 80)
    lines.append(f"{'TOTAL':<40} {'':<20} {format_currency(report_data['total_debits']):>15} {format_currency(report_data['total_credits']):>15}")
    lines.append("=" * 80)
    
    # Balance check
    if report_data["is_balanced"]:
        lines.append("✓ Trial Balance is balanced")
    else:
        lines.append("✗ Trial Balance is NOT balanced")
    
    return "\n".join(lines)

def generate_income_statement():
    """
    Generate Income Statement (Profit & Loss)
    
    Returns:
        Tuple (success: bool, report_data: dict, message: str)
    """
    accounts_data = load_accounts()
    
    total_revenue = 0.0
    total_expenses = 0.0
    
    revenue_accounts = []  # Fix: plural
    expense_accounts = []
    
    for account_name, account_info in accounts_data.items():
        account_type = account_info.get("type")
        balance = account_info.get("balance", 0.0)
        
        if account_type == "Revenue":
            revenue_accounts.append({
                "account": account_name,  # Store account name
                "amount": balance
            })
            total_revenue += balance
        elif account_type == "Expense":
            expense_accounts.append({
                "account": account_name,  # Store account name
                "amount": balance
            })
            total_expenses += balance
    
    net_income = total_revenue - total_expenses
    
    report_data = {
        "revenue_accounts": sorted(revenue_accounts, key=lambda x: x["account"]),  # Sort by name
        "expense_accounts": sorted(expense_accounts, key=lambda x: x["account"]),  # Sort by name
        "total_revenue": total_revenue,  # Add this
        "total_expenses": total_expenses,  # Add this
        "net_income": net_income
    }
    
    # Save to file
    report_file = REPORTS_DIR / "income_statement.txt"
    report_text = format_income_statement_text(report_data)
    
    try:
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_text)
        return True, report_data, "Income Statement generated successfully"
    except IOError as e:
        return False, report_data, f"Failed to save report: {e}"

def format_income_statement_text(report_data):
    """Format income statement as text"""
    lines = []
    # Header
    lines.append("=" * 80)
    lines.append("INCOME STATEMENT")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("=" * 80)
    
    # Revenue section
    lines.append("\nREVENUE:")
    lines.append("-" * 80)
    for account in report_data["revenue_accounts"]:
        lines.append(f"  {account['account']:<50} {format_currency(account['amount']):>20}")
    
    lines.append("-" * 80)
    lines.append(f"  {'Total Revenue':<50} {format_currency(report_data['total_revenue']):>20}")
    
    # Expenses section
    lines.append("\nEXPENSES:")
    lines.append("-" * 80)
    for account in report_data["expense_accounts"]:
        lines.append(f"  {account['account']:<50} {format_currency(account['amount']):>20}")
    
    lines.append("-" * 80)
    lines.append(f"  {'Total Expenses':<50} {format_currency(report_data['total_expenses']):>20}")
    
    # Net Income/Loss
    lines.append("\n" + "=" * 80)
    net_label = "Net Income" if report_data["net_income"] >= 0 else "Net Loss"
    lines.append(f"  {net_label:<50} {format_currency(abs(report_data['net_income'])):>20}")
    lines.append("=" * 80)
    
    return "\n".join(lines)

def generate_balance_sheet():

    """
    Generate Balance Sheet
    
    Returns:
        Tuple (success: bool, report_data: dict, message: str)
    """
    accounts_data = load_accounts()
    
    assets = []
    liabilities = []
    equity = []
    
    total_assets = 0.0
    total_liabilities = 0.0
    total_equity = 0.0
    
    for account_name, account_info in accounts_data.items():
        account_type = account_info.get("type")
        balance = account_info.get("balance", 0.0)
        
        if account_type == "Asset":
            assets.append({
                "account": account_name,
                "amount": balance
            })
            total_assets += balance
        elif account_type == "Liability":
            liabilities.append({
                "account": account_name,
                "amount": balance
            })
            total_liabilities += balance
        elif account_type == "Owner's Equity":  # Fix: Check specifically
            equity.append({
                "account": account_name,
                "amount": balance
            })
            total_equity += balance
    
    # Add retained earnings (net income from income statement)
    income_success, income_data, _ = generate_income_statement()
    if income_success and income_data:
        net_income = income_data.get("net_income", 0.0)
        if net_income != 0:
            equity.append({
                "account": "Retained Earnings (Net Income)",
                "amount": net_income
            })
            total_equity += net_income
    
    report_data = {
        "assets": sorted(assets, key=lambda x: x["account"]),  # Sort
        "liabilities": sorted(liabilities, key=lambda x: x["account"]),  # Sort
        "equity": sorted(equity, key=lambda x: x["account"]),  # Sort
        "total_assets": total_assets,  # Add totals
        "total_liabilities": total_liabilities,
        "total_equity": total_equity,
        "is_balanced": abs(total_assets - (total_liabilities + total_equity)) < 0.01  # Check balance
    }
    
    # Save to file
    report_file = REPORTS_DIR / "balance_sheet.txt"
    report_text = format_balance_sheet_text(report_data)
    
    try:
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_text)
        return True, report_data, "Balance Sheet generated successfully"
    except IOError as e:
        return False, report_data, f"Failed to save report: {e}"

def format_balance_sheet_text(report_data):
    """Format balance sheet as text"""
    lines = []
    # Header
    lines.append("=" * 80)
    lines.append("BALANCE SHEET")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("=" * 80)
    
    # Assets section
    lines.append("\nASSETS:")
    lines.append("-" * 80)
    for asset in report_data["assets"]:
        lines.append(f"  {asset['account']:<50} {format_currency(asset['amount']):>20}")
    lines.append("-" * 80)
    lines.append(f"  {'Total Assets':<50} {format_currency(report_data['total_assets']):>20}")
    
    # Liabilities section
    lines.append("\nLIABILITIES:")
    lines.append("-" * 80)
    for liability in report_data["liabilities"]:
        lines.append(f"  {liability['account']:<50} {format_currency(liability['amount']):>20}")
    lines.append("-" * 80)
    lines.append(f"  {'Total Liabilities':<50} {format_currency(report_data['total_liabilities']):>20}")
    
    # Owner's Equity section
    lines.append("\nOWNER'S EQUITY:")
    lines.append("-" * 80)
    for eq in report_data["equity"]:
        lines.append(f"  {eq['account']:<50} {format_currency(eq['amount']):>20}")
    lines.append("-" * 80)
    lines.append(f"  {'Total Owners Equity':<50} {format_currency(report_data['total_equity']):>20}")
    
    # Total Liabilities + Equity
    lines.append("\n" + "=" * 80)
    total_liab_equity = report_data["total_liabilities"] + report_data["total_equity"]
    lines.append(f"  {'Total Liabilities + Equity':<50} {format_currency(total_liab_equity):>20}")
    lines.append("=" * 80)
    
    # Balance check
    if report_data["is_balanced"]:
        lines.append("✓ Balance Sheet is balanced")
    else:
        lines.append("✗ Balance Sheet is NOT balanced")
    
    return "\n".join(lines)

def generate_cash_flow():
    """
    Generate Cash Flow Statement
    
    Returns:
        Tuple (success: bool, report_data: dict, message: str)
    """
    journal_entries = load_journal_entries()
    accounts_data = load_accounts()
    
    # Find Cash account (look for account with "cash" in the name)
    cash_account = None
    for account_name, account_info in accounts_data.items():
        if account_info.get("type") == "Asset" and "cash" in account_name.lower():
            cash_account = account_name
            break
    
    if not cash_account:
        return False, {}, "No Cash account found"
    
    # Get cash ledger entries
    cash_ledger = get_account_ledger(cash_account)
    
    if not cash_ledger:
        return False, {}, "No cash transactions found"
    
    # Categorize transactions
    operating = []
    investing = []
    financing = []
    
    # Loop through cash ledger entries
    for entry in cash_ledger:
        je_id = entry.get("je_id")
        journal_entry = journal_entries.get(je_id, {})
        narration = journal_entry.get("narration", "").lower()
        
        entry_data = {
            "date": entry.get("date"),
            "je_id": je_id,
            "narration": journal_entry.get("narration", ""),
            "amount": entry.get("amount"),
            "type": entry.get("entry_type")
        }
        
        # Categorize based on keywords in narration
        if any(keyword in narration for keyword in ["loan", "capital", "equity", "investment"]):
            financing.append(entry_data)
        elif any(keyword in narration for keyword in ["equipment", "asset", "property", "building"]):
            investing.append(entry_data)
        else:
            operating.append(entry_data)
    
    # Calculate totals
    # Debit increases cash (positive), Credit decreases cash (negative)
    operating_cash = sum(e["amount"] if e["type"] == "Debit" else -e["amount"] for e in operating)
    investing_cash = sum(e["amount"] if e["type"] == "Debit" else -e["amount"] for e in investing)
    financing_cash = sum(e["amount"] if e["type"] == "Debit" else -e["amount"] for e in financing)
    
    net_cash_flow = operating_cash + investing_cash + financing_cash
    
    report_data = {
        "cash_account": cash_account,
        "operating": operating,
        "investing": investing,
        "financing": financing,
        "operating_cash": operating_cash,
        "investing_cash": investing_cash,
        "financing_cash": financing_cash,
        "net_cash_flow": net_cash_flow
    }
    
    # Save to file
    report_file = REPORTS_DIR / "cashflow.txt"
    report_text = format_cash_flow_text(report_data)
    
    try:
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_text)
        return True, report_data, "Cash Flow Statement generated successfully"
    except IOError as e:
        return False, report_data, f"Failed to save report: {e}"


def format_cash_flow_text(report_data):
    """Format cash flow statement as text"""
    lines = []
    lines.append("=" * 80)
    lines.append("CASH FLOW STATEMENT")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"Cash Account: {report_data['cash_account']}")
    lines.append("=" * 80)
    
    lines.append("\nOPERATING ACTIVITIES:")
    lines.append("-" * 80)
    for entry in report_data["operating"]:
        amount_str = format_currency(entry["amount"]) if entry["type"] == "Debit" else format_currency(-entry["amount"])
        lines.append(f"  {entry['date']} - {entry['narration']:<40} {amount_str:>20}")
    lines.append("-" * 80)
    lines.append(f"  {'Net Cash from Operating Activities':<50} {format_currency(report_data['operating_cash']):>20}")
    
    lines.append("\nINVESTING ACTIVITIES:")
    lines.append("-" * 80)
    for entry in report_data["investing"]:
        amount_str = format_currency(entry["amount"]) if entry["type"] == "Debit" else format_currency(-entry["amount"])
        lines.append(f"  {entry['date']} - {entry['narration']:<40} {amount_str:>20}")
    lines.append("-" * 80)
    lines.append(f"  {'Net Cash from Investing Activities':<50} {format_currency(report_data['investing_cash']):>20}")
    
    lines.append("\nFINANCING ACTIVITIES:")
    lines.append("-" * 80)
    for entry in report_data["financing"]:
        amount_str = format_currency(entry["amount"]) if entry["type"] == "Debit" else format_currency(-entry["amount"])
        lines.append(f"  {entry['date']} - {entry['narration']:<40} {amount_str:>20}")
    lines.append("-" * 80)
    lines.append(f"  {'Net Cash from Financing Activities':<50} {format_currency(report_data['financing_cash']):>20}")
    
    lines.append("\n" + "=" * 80)
    lines.append(f"  {'Net Increase/Decrease in Cash':<50} {format_currency(report_data['net_cash_flow']):>20}")
    lines.append("=" * 80)
    
    return "\n".join(lines)


def generate_ratio_analysis():
    """
    Generate Financial Ratio Analysis
    
    Returns:
        Tuple (success: bool, report_data: dict, message: str)
    """
    # Get income statement data
    income_success, income_data, _ = generate_income_statement()
    if not income_success:
        return False, {}, "Failed to generate income statement"
    
    # Get balance sheet data
    balance_success, balance_data, _ = generate_balance_sheet()
    if not balance_success:
        return False, {}, "Failed to generate balance sheet"
    
    # Extract values
    total_revenue = income_data.get("total_revenue", 0.0)
    net_income = income_data.get("net_income", 0.0)
    total_expenses = income_data.get("total_expenses", 0.0)
    total_assets = balance_data.get("total_assets", 0.0)
    total_liabilities = balance_data.get("total_liabilities", 0.0)
    total_equity = balance_data.get("total_equity", 0.0)
    
    # Calculate ratios
    profit_margin = (net_income / total_revenue * 100) if total_revenue > 0 else 0.0
    debt_ratio = (total_liabilities / total_assets * 100) if total_assets > 0 else 0.0
    current_ratio = 1.0  # Simplified - would need current assets/liabilities breakdown
    
    # Calculate ROA (Return on Assets)
    roa = (net_income / total_assets * 100) if total_assets > 0 else 0.0
    
    # Calculate ROE (Return on Equity)
    roe = (net_income / total_equity * 100) if total_equity > 0 else 0.0
    
    report_data = {
        "profit_margin": profit_margin,
        "debt_ratio": debt_ratio,
        "current_ratio": current_ratio,
        "roa": roa,
        "roe": roe,
        "total_revenue": total_revenue,
        "net_income": net_income,
        "total_assets": total_assets,
        "total_liabilities": total_liabilities,
        "total_equity": total_equity
    }
    
    return True, report_data, "Ratio Analysis generated successfully"

    