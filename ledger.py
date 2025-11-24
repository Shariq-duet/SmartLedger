"""
Ledger Posting Module - Update balances and maintain transaction histories
"""
from utils import (
    load_json, save_json, LEDGER_FILE,
    get_account_by_name
)
from accounts import update_account_balance, load_accounts
from journal import load_journal_entries

def load_ledger_data():
    return load_json(LEDGER_FILE,default={})

def save_ledger_data(ledger_data):
    return save_json(LEDGER_FILE,ledger_data)

def post_journal_entry_to_ledger(je_id, journal_entry):
    date = journal_entry.get("date")
    debits = journal_entry.get("debits", [])  # ✅ Fix: 'debits' plural
    credits = journal_entry.get("credits", [])
    
    ledger_data = load_ledger_data()
    accounts_data = load_accounts()  # Load once for efficiency
    
    # Process debits
    for debit_entry in debits:
        account_name = debit_entry.get("account")
        amount = float(debit_entry.get("amount", 0))
        
        # Get actual account name
        actual_name, account_data = get_account_by_name(account_name, accounts_data)
        if not account_data:
            return False, f"Account '{account_name}' does not exist"
        
        # Update account balance
        success, new_balance = update_account_balance(actual_name, amount, "Debit")
        if not success:
            return False, f"Failed to update balance for account '{actual_name}'"
        
        # Add to ledger history
        if actual_name not in ledger_data:
            ledger_data[actual_name] = []
        
        ledger_data[actual_name].append({
            "date": date,
            "je_id": je_id,
            "entry_type": "Debit",
            "amount": amount,
            "running_balance": new_balance
        })
    
    # Process credits (separate loop!)
    for credit_entry in credits:
        account_name = credit_entry.get("account")
        amount = float(credit_entry.get("amount", 0))
        
        # Get actual account name
        actual_name, account_data = get_account_by_name(account_name, accounts_data)
        if not account_data:
            return False, f"Account '{account_name}' does not exist"
        
        # Update account balance
        success, new_balance = update_account_balance(actual_name, amount, "Credit")
        if not success:
            return False, f"Failed to update balance for account '{actual_name}'"
        
        # Add to ledger history
        if actual_name not in ledger_data:
            ledger_data[actual_name] = []
        
        ledger_data[actual_name].append({
            "date": date,
            "je_id": je_id,
            "entry_type": "Credit",
            "amount": amount,
            "running_balance": new_balance
        })
    
    # Save ledger data
    if save_ledger_data(ledger_data):
        return True, "Ledger updated successfully"
    else:
        return False, "Failed to save ledger data"
def get_account_ledger(account_name):
    """
    Get ledger history for a specific account
    
    Args:
        account_name: Name of account
    
    Returns:
        List of ledger entries or None if account doesn't exist
    """
    accounts_data = load_accounts()
    actual_name, account_data = get_account_by_name(account_name, accounts_data)
    
    if not account_data:
        return None
    
    ledger_data = load_ledger_data()
    return ledger_data.get(actual_name, [])


def rebuild_ledger():
    """
    Rebuild ledger from all journal entries (useful for data integrity)
    
    Returns:
        Tuple (success: bool, message: str)
    """
    # Reset all account balances
    accounts_data = load_accounts()
    for account_name in accounts_data:
        accounts_data[account_name]["balance"] = 0.0
    from utils import save_json, ACCOUNTS_FILE
    save_json(ACCOUNTS_FILE, accounts_data)
    
    # Clear ledger
    ledger_data = {}
    save_ledger_data(ledger_data)
    
    # Re-post all journal entries
    journal_entries = load_journal_entries()
    success_count = 0
    error_count = 0
    
    for je_id, entry in journal_entries.items():
        success, message = post_journal_entry_to_ledger(je_id, entry)
        if success:
            success_count += 1
        else:
            error_count += 1
    
    if error_count == 0:
        return True, f"Ledger rebuilt successfully. Processed {success_count} entries."
    else:
        return False, f"Ledger rebuild completed with errors. Success: {success_count}, Errors: {error_count}"
