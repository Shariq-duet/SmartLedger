"""
Journal Entry Recording Module - Record debit-credit transactions
"""
from datetime import datetime
from utils import (
    load_json, save_json, JOURNAL_FILE,
    validate_amount, validate_balanced_entry, account_exists
)
from accounts import load_accounts

def load_journal_entries():
     """Load journal data from storage"""
     return load_json(JOURNAL_FILE,default={})
def save_journal_entries(entries_data):
     """Save journal data to storage"""
     return save_json(JOURNAL_FILE,entries_data)

def generate_je_id(date=None):
    """
    Generate unique Journal Entry ID (JE-YYYYMMDD-XXX)
    
    Args:
        date: Date for JE ID (default: today)
    
    Returns:
        Journal Entry ID string
    """
    if date is None:
        date = datetime.now()
    elif isinstance(date, str):  # ✅ Use elif
        date = datetime.strptime(date, "%Y-%m-%d")

    
    date_str = date.strftime("%Y%m%d")

    # Load all journal entries
    entries = load_journal_entries()

    # Start with sequence 1
    sequence = 1

    # Loop until we find an available ID
    while True:
        je_id = f"JE-{date_str}-{sequence:03d}"  # Format: JE-20231215-001
        
        # Check if this ID already exists
        if je_id not in entries:
            return je_id  # Found an available ID!
        
        # If it exists, try next sequence number
        sequence += 1
def create_journal_entry(date, narration, debits, credits):
    """
    Create a new journal entry with validation
    
    Args:
        date: Transaction date (YYYY-MM-DD)
        narration: Description of transaction
        debits: List of dicts with 'account' and 'amount'
        credits: List of dicts with 'account' and 'amount'
    
    Returns:
        Tuple (success: bool, je_id: str or None, message: str)

    """
    try:
        datetime.strptime(date,"%Y-%m-%d")
    except ValueError:
        return False, None, "Invalid date format. Use YYYY-MM-DD"

    if not narration or not narration.strip():
        return False, None ,"Narration can not be Empty"

    if not debits or not credits:
        return False,None,"Debit and credit must be filled"

    for entry in debits:
        if not validate_amount(entry.get('amount')):
            return False, None, f"Invalid debit amount: {entry.get('amount')}"
    
    for entry in credits:
        if not validate_amount(entry.get('amount')):
            return False, None, f"Invalid credit amount: {entry.get('amount')}"
    # Validate accounts exist
    accounts_data = load_accounts()
    
    for entry in debits:
        account_name = entry.get('account')
        if not account_exists(account_name, accounts_data):
            return False, None, f"Debit account '{account_name}' does not exist"
    
    for entry in credits:
        account_name = entry.get('account')
        if not account_exists(account_name, accounts_data):
            return False, None, f"Credit account '{account_name}' does not exist"
    
    is_valid,total_debits,total_credits=validate_balanced_entry(debits,credits)
    if not is_valid:
        return False,None,f"Unbalanced entry: Debits (${total_debits:.2f}) != Credits (${total_credits:.2f})"
    
    je_id=generate_je_id(date)

    entry_data = {
     "date": date,
     "narration": narration,
     "debits": debits,
     "credits": credits
      }
        # Step 9: Load entries, add new entry, save
    entries = load_journal_entries()
    entries[je_id] = entry_data

    if save_journal_entries(entries):
        return True, je_id, f"Journal entry '{je_id}' created successfully"
    else:
        return False, None, "Failed to save journal entry"

def get_journal_entries(date_filter=None):
    """
    Get journal entries, optionally filtered by date
    
    Args:
        date_filter: Optional date filter (YYYY-MM-DD)
    
    Returns:
        Dictionary of journal entries
    """
    entries = load_journal_entries()
    
    if date_filter:
        return {je_id: data for je_id, data in entries.items() 
                if data.get("date") == date_filter}
    
    return entries

def get_journal_entry(je_id):
    """
    Get a specific journal entry by ID
    
    Args:
        je_id: Journal Entry ID
    
    Returns:
        Entry data or None
    """
    entries = load_journal_entries()
    return entries.get(je_id)
    