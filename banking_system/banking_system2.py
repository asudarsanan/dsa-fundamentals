
from datetime import timedelta, datetime
import time

class BankingSystem:

    def __init__(self):
        # TODO: implement
        self.accounts = {}
        self.last_operation_time = None
        self.transactions = []
        self.transfers = []

    # TODO: implement interface methods here
    def create_account(self, timestamp: int, account_id: str) -> bool:
        if account_id not in self.accounts:
            self.accounts[account_id] = 0
            self.transactions.append((account_id,0,timestamp,'+'))
            return True
        self.last_operation_time = timestamp
        return False
        
    def deposit(self, timestamp: int, account_id: str, amount: int) -> int | None:
        self.last_operation_time = timestamp
        if account_id not in self.accounts:
            return None
        else:
            self.accounts[account_id] += amount
            self.transactions.append((account_id,amount,timestamp,'+'))
            return self.accounts[account_id]
    
    def pay(self, timestamp: int, account_id: str, amount: int) -> int | None:
        self.last_operation_time = timestamp
        
        if account_id not in self.accounts or self.accounts[account_id] < amount:
            return None
        else:
            self.accounts[account_id] -= amount
            self.transactions.append((account_id,amount,timestamp,'-'))
            return self.accounts[account_id]
            
    def top_activity(self, timestamp: int, n: int) -> list[str]:
        self.last_operation_time = timestamp
        total_transactions = self.transactions
        
        total_value = {}
        for account_id,amount,_,_ in total_transactions:
            if account_id not in total_value:
                total_value[account_id] = 0
            total_value[account_id] += amount
            
        sorted_worth = sorted(
            total_value.items(),
            key=lambda x: (-x[1],x[0])
        )
        results = []
        for account_id,amount in sorted_worth:
            string = f"{account_id}({amount})"
            results.append(string)
        return results[:n]
        
    def transfer(self, timestamp: int, source_account_id: str, target_account_id: str, amount: int) -> str | None:
            self.last_operation_time = timestamp
            
            # Validate accounts and balance
            if source_account_id == target_account_id:
                return None
            elif source_account_id not in self.accounts or target_account_id not in self.accounts:
                return None
            elif self.accounts[source_account_id] < amount:
                return None
            
            # Proceed with transfer
            self.accounts[source_account_id] -= amount
            withheld_amount = amount
            transfer_id = f"transfer{len(self.transfers)+1}"
            created_time = time.time()  # Use current system time for the transfer creation
            
            # Store transfer details
            self.transfers.append({
                'transfer_id': transfer_id,
                'withheld_amount': withheld_amount,
                'source_account_id': source_account_id,
                'target_account_id': target_account_id,
                'status': 'pending',
                'created_time': created_time,
                'timestamp': timestamp
            })
            
            return transfer_id

    def accept_transfer(self, timestamp: int, account_id: str, transfer_id: str) -> bool:
            self.last_operation_time = timestamp
            
            # Find the transfer by ID and check if it's still pending
            transfers_account = [t for t in self.transfers if t['transfer_id'] == transfer_id and t['status'] == 'pending']
            
            if not transfers_account:
                return False
            
            now = time.time()
            for transfer in transfers_account:
                # Check if the transfer is still valid (not expired)
                if now - transfer['created_time'] > timedelta(hours=24).total_seconds():
                    transfer['status'] = 'expired'
                    return False
                
                # If valid, proceed with accepting the transfer
                if transfer['transfer_id'] == transfer_id:
                    self.accounts[account_id] += transfer['withheld_amount']
                    self.transactions.append((account_id, transfer['withheld_amount'], timestamp, '+'))
                    self.transactions.append((transfer['source_account_id'], transfer['withheld_amount'], timestamp, '-'))
                    transfer['status'] = 'completed'
                    return True
            
            return False