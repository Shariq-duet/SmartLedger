import json
import os
import datetime as dt
from pathlib import Path

#Data directory path
DATA_DIR = Path("data")
ACCOUNTS_FILE = DATA_DIR / "accounts.json"
JOURNAL_FILE = DATA_DIR / "journal_entries.json"
LEDGER_FILE = DATA_DIR / "ledger_data.json"
REPORTS_DIR = DATA_DIR / "reports"

def ensure_dir_real():
    """Ensure data directory exists"""
    DATA_DIR.mkdir(exist_ok=True)
    REPORTS_DIR.mkdir(exist_ok=True)

def load_json(filepath,default=None):
    """
    Safely load JSON data from file
    Args:
        filepath: Path to JSON file
        default: Default value if file doesn't exist or is invalid
    Returns:
        Loaded data or default value
    """
    if default is None:
        default = {}
    ensure_dir_real()
    if not filepath.exists():
        return default
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading {filepath}: {e}")
        return default
    
def save_json(filepath, data):
    """
    Safely save data to JSON file with backup
    Args:
        filepath: Path to JSON file
        data: Data to save
    """
    ensure_dir_real()
    if filepath.exists():
        backup=f"{filepath.stem}_{dt.datetime.now().strftime('%Y%m%d')}.json"
        backup_path=DATA_DIR / backup
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                backup_data=json.load(f)
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not create backup: {e}")
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"Error saving {filepath}: {e}")
        return False

def validate_amount(amount):
    """
    Validate that amount is positive
    Args:
        amount: Amount to validate
    Returns:
        True if valid, False otherwise
    """
    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Amount must be positive")
        else:
            return True
    except (ValueError, TypeError) as e:
        print(f"Error validating amount: {e}")
        return False
def validate_balanced_entry(debits, credits):
    """
    Validate that total debits equal total credits
    Args:
        debits: List of debit entries with 'amount' key
        credits: List of credit entries with 'amount' key
    Returns:
        True if valid, False otherwise and tuple of total debits and total credits
    """
    sum_debit = sum(debit.get('amount', 0) for debit in debits)
    sum_credit = sum(credit.get('amount', 0) for credit in credits)
    is_equal = abs(sum_debit - sum_credit) < 0.01
    if is_equal:
        return True, sum_debit, sum_credit
    else:
        return False, sum_debit, sum_credit
    
def format_currency(amount):
    """
    Format amount as currency with 2 decimal places
    Args:
        amount: Amount to format
    Returns:
        Formatted string (e.g., "$1,000.00")
    """
    try:
        amount = float(amount)
        return f"${amount:,.2f}"
    except (ValueError, TypeError):
        return "$0.00"
    
def account_exists(account_name, accounts_data):
    """
    Check if account exists in accounts data
    Args:
        account_name: Name of account to check
        accounts_data: Dictionary of accounts data
    Returns:
        True if account exists, False otherwise
    """
    account_name_lower = account_name.lower()
    for name in accounts_data.keys():
        if name.lower() == account_name_lower:
            return True
    return False
    
def get_account_by_name(account_name, accounts_data):
    """
    Get account data by name (case-insensitive)
    Args:
        account_name: Name of account to get
        accounts_data: Dictionary of accounts data
    Returns:
        Tuple (account_name, account_data) or (None, None)
    """
    account_name_lower = account_name.lower()
    for name, data in accounts_data.items():
        if name.lower() == account_name_lower:
            return name, data
    return None, None