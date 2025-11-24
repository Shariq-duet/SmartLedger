"""Account Management Module - Create, categorize, and manage accounts"""
from webbrowser import get
from utils import load_json, save_json, account_exists, get_account_by_name, format_currency, ACCOUNTS_FILE

ACCOUNT_TYPES = ['Asset', 'Liability', 'Revenue', 'Expense', 'Owner\'s Equity']

def load_accounts():
    """Load all accounts from storage"""
    return load_json(ACCOUNTS_FILE, default={})

def save_accounts(accounts_data):
    """Save accounts to storage"""
    return save_json(ACCOUNTS_FILE, accounts_data)

def create_account(name, account_type, initial_balance=0.0):
    """Create a new account"""
    if not name or not name.strip():
        return False, "Account name cannot be empty"
    if account_type not in ACCOUNT_TYPES:
        return False, f"Invalid account type. Must be one of: {', '.join(ACCOUNT_TYPES)}"
    accounts_data = load_accounts()
    if account_exists(name, accounts_data):
        return False, f"Account '{name}' already exists"
    accounts_data[name] = {
        "type": account_type,
        "balance": float(initial_balance)
    }
    if save_accounts(accounts_data):
        return True, f"Account '{name}' created successfully"
    else:
        return False, "Failed to save account"

def get_accounts_by_type(account_type=None):
    """
    Get accounts filtered by type
    
    Args:
        account_type: Optional filter by account type
    
    Returns:
        Dictionary of accounts
    """
    accounts_data = load_accounts()
    
    if account_type:
        # Filter by type - return all accounts of that type
        return {name: data for name, data in accounts_data.items() 
                if data.get("type") == account_type}
    
    # If no filter, return all accounts
    return accounts_data

def get_account_balance(account_name):
    """
    Get current balance of an account
    
    Args:
        account_name: Name of account
    
    Returns:
        Balance (float) or None if account doesn't exist
    """
    accounts_data = load_accounts()
    actual_name , account_data = get_account_by_name(account_name, accounts_data)
    if account_data:
        return account_data.get("balance", 0.0)
    return None

def update_account_balance(account_name,amount,entry_type):
    """
    Update account balance based on transaction
    
    Args:
        account_name: Name of account
        amount: Transaction amount
        entry_type: "Debit" or "Credit"
    
    Returns:
        Tuple (success: bool, new_balance: float or None)
    """
    accounts = load_accounts()
    actual_name , account_data = get_account_by_name(account_name,accounts)
    if not account_data:
        return False,None
    
    account_type = account_data.get("type")
    current_balance = account_data.get("balance", 0.0)
    
    # Calculate new balance based on accounting rules
    if account_type in ["Asset", "Expense"]:
        if entry_type == "Debit":
            new_balance = current_balance + amount
        else:  # Credit
            new_balance = current_balance - amount
    else:  # Liability, Revenue, Owner's Equity
        if entry_type == "Credit":
            new_balance = current_balance + amount
        else:  # Debit
            new_balance = current_balance - amount
    
    accounts[actual_name]["balance"] = new_balance
    
    if save_accounts(accounts):
        return True, new_balance
    else:
        return False, None   



