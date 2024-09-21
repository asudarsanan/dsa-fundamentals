from collections import defaultdict
import time
from typing import List


class BankingSystem():
    def __init__(self):
        self.accounts = {}
        self.transactions = []
        self.scheduled = []
        self.last_operation_time = None

    def create_account(self,timestamp,account_id) -> None:
        if account_id in self.accounts:
            self.last_operation_time = timestamp
            return None
        else:
            self.accounts[account_id] = 0
            self.last_operation_time = timestamp


    def deposit(self, timestamp: int, account_id: str, amount: int) -> None:
        # Add the deposit to the account balance if the account exists
        self.check_scheduled_payments()
        if account_id in self.accounts:
            self.accounts[account_id] += amount
            self.last_operation_time = timestamp
        else:
            self.last_operation_time = timestamp
            return None

    def transfer(self,timestamp,source_account_id,amount,transfer_account_id,is_scheduled=False) -> None:

        self.last_operation_time = timestamp

        if not is_scheduled:
            self.check_scheduled_payments()
        
        if source_account_id not in self.accounts or transfer_account_id not in self.accounts:
            return None
        elif self.accounts[source_account_id] < amount:
            return None
        else:
            self.accounts[source_account_id] -= amount
            self.accounts[transfer_account_id] += amount
            self.transactions.append((source_account_id,amount,timestamp,'-'))
            self.transactions.append((transfer_account_id,amount,timestamp,'+'))
            return self.accounts[source_account_id]
    

    def top_spenders(self,timestamp:int,n:int) -> List[str]:
        self.last_operation_time = timestamp
        filtered_transactions = [t for t in self.transactions if t[2] <= timestamp and t[3] == '-']
        outgoing_total = defaultdict(int)
        for account_id,amount,_,_ in filtered_transactions:
            outgoing_total[account_id] += amount
            if account_id not in outgoing_total:
                outgoing_total[account_id] = amount
        sorted_account = sorted(
                        outgoing_total.items(),
            key=lambda x: (-x[1], x[0])
        )
        results = []
        for account_id,amount in sorted_account:
            string = "{}({})".format(account_id,amount)
            results.append(string)
        return results

        
    def scheduled_payments(self,scheduled_timestamp,source_account_id,target_account_id,amount,status,created_timestamp) -> None:
        self.scheduled.append({'scheduled_timestamp':scheduled_timestamp,
                               'source_account_id':source_account_id,
                               'amount':amount,
                               'target_account_id':target_account_id,
                               'created_timestamp':created_timestamp,
                               'status':status})
        self.last_operation_time = created_timestamp
        

    def check_scheduled_payments(self):
        payments = [ p for p in self.scheduled 
                    if  p['scheduled_timestamp'] <= self.last_operation_time and p['status'] == 'pending']
        for payment in payments:
            response = self.process_scheduled_payments(payment=payment)
            payment.update(response)
        

    def process_scheduled_payments(self,payment):
        source = payment['source_account_id']
        target = payment['target_account_id']
        amount = payment['amount']
        timestamp = payment['scheduled_timestamp']

        process = self.transfer(timestamp=timestamp,source_account_id=source,amount=amount,transfer_account_id=target,is_scheduled=True)
        if process == None:
            payment['status'] = 'failed'
        else:
            payment['status'] = 'completed'
        return payment
    
    def merge_accounts(self,timestamp,account_1,account_2):
        if account_1 not in self.accounts or account_2 not in self.accounts:
            return None
        
        merged_account_id = f"{account_1}_{account_2}"
        merged_balance = self.accounts[account_1] + self.accounts[account_2]
        self.accounts[merged_account_id] = merged_balance

        for transactions in self.transactions:
            if transactions[0] in (account_1,account_2):
                self.transactions.append((merged_account_id,transactions[1],transactions[2],transactions[3]))

        for payment in self.scheduled:
            if (payment['source_account_id'] in (account_1, account_2)) and (payment['target_account_id'] in (account_1, account_2)):
                payment['status'] = 'cancelled'

        outgoing_payments = [p for p in self.scheduled if p['source_account_id'] in (account_1, account_2) and p['status'] == 'pending']
        for payment in outgoing_payments:
            payment['source_account_id'] = merged_account_id
        
        incoming_payments = [p for p in self.scheduled if p['target_account_id'] in (account_1, account_2) and p['status'] == 'pending']
        for payment in incoming_payments:
            payment['target_account_id'] = merged_account_id

        del self.accounts[account_1]
        del self.accounts[account_2]

        self.last_operation_time = timestamp
        return merged_account_id
# Instantiate the banking system
# bank = BankingSystem()

# # Test Case 1: Basic transfer test
# bank.create_account(1, "A123")
# bank.create_account(1, "B456")

# bank.deposit(1, "A123", 500)
# bank.transfer(2, "A123", 200, "B456")  # A123 sends 200 to B456
# bank.transfer(3, "A123", 200, "B456")  # A123 sends another 200 to B456

# print("Test Case 1 - Top Spenders (Limit 2):")
# print(bank.top_spenders(3, 2))  # Output: ['A123(400)']


# # Test Case 2: Multiple accounts with transfers
# bank.create_account(4, "C789")
# bank.deposit(4, "C789", 1000)
# bank.transfer(5, "C789", 300, "A123")  # C789 sends 300 to A123
# bank.transfer(6, "C789", 500, "B456")  # C789 sends 500 to B456

# print("Test Case 2 - Top Spenders (Limit 3):")
# print(bank.top_spenders(6, 3))  # Output: ['C789(800)', 'A123(400)']


# # Test Case 3: Test timestamp filtering
# bank.transfer(7, "A123", 100, "B456")  # A123 sends 100 to B456 at timestamp 7

# print("Test Case 3 - Top Spenders up to timestamp 5 (Limit 2):")
# print(bank.top_spenders(5, 2))  # Output: ['A123(400)', 'C789(300)']


# # Test Case 4: No transactions before the timestamp
# print("Test Case 4 - Top Spenders with no transactions before timestamp 0 (Limit 2):")
# print(bank.top_spenders(0, 2))  # Output: []


# # Test Case 5: Less than 'n' accounts available
# print("Test Case 5 - Top Spenders (Limit 5):")
# print(bank.top_spenders(7, 5))  # Output: ['C789(800)', 'A123(500)']

# # --- Adding Scheduled Payments Tests ---

# # Test Case 6: Scheduled payment succeeds
# bank.create_account(8, "D101")
# bank.deposit(8, "D101", 600)
# bank.scheduled_payments(10, "D101", "B456", 400, "pending", 9)

# print("Test Case 6 - Before scheduled payment (Timestamp 9):")
# print(bank.top_spenders(9, 3))  # Output: ['C789(800)', 'A123(500)']

# # Simulate time passing and scheduled payment triggering at timestamp 10
# bank.check_scheduled_payments()
# print("Test Case 6 - After scheduled payment (Timestamp 10):")
# print(bank.top_spenders(10, 3))  # Output: ['C789(800)', 'A123(500)', 'D101(400)']


# # Test Case 7: Scheduled payment fails due to insufficient funds
# bank.create_account(11, "E202")
# bank.scheduled_payments(12, "E202", "A123", 1000, "pending", 11)  # Insufficient funds

# # Simulate time passing and attempting to process the scheduled payment
# bank.check_scheduled_payments()
# print("Test Case 7 - After failed scheduled payment (Timestamp 12):")
# print(bank.top_spenders(12, 3))  # Output: ['C789(800)', 'A123(500)', 'D101(400)']


# # Test Case 8: Multiple scheduled payments processed at once
# bank.create_account(13, "F303")
# bank.deposit(13, "F303", 1500)
# bank.scheduled_payments(15, "F303", "B456", 500, "pending", 14)
# bank.scheduled_payments(16, "F303", "A123", 400, "pending", 14)

# # Process all scheduled payments at timestamp 16
# bank.check_scheduled_payments()
# print("Test Case 8 - After multiple scheduled payments (Timestamp 16):")
# print(bank.top_spenders(16, 5))  # Output: ['C789(800)', 'F303(900)', 'A123(900)', 'D101(400)']


# # Test Case 9: Scheduled payment before the deposit is made
# bank.create_account(17, "G404")
# bank.scheduled_payments(18, "G404", "B456", 500, "pending", 17)

# # Simulate time passing before the scheduled payment (no deposit yet)
# bank.check_scheduled_payments()
# print("Test Case 9 - Before deposit (Timestamp 18):")
# print(bank.top_spenders(18, 5))  # Output: ['C789(800)', 'F303(900)', 'A123(900)', 'D101(400)']

# # Now, make a deposit that allows the payment to succeed
# bank.deposit(19, "G404", 600)
# bank.check_scheduled_payments()
# print("Test Case 9 - After deposit and processing scheduled payment (Timestamp 19):")
# print(bank.top_spenders(19, 5))  # Output: ['C789(800)', 'F303(900)', 'A123(900)', 'D101(400)', 'G404(500)']


# # Test Case 10: Scheduled payment partially processed (multiple payments at once)
# bank.create_account(20, "H505")
# bank.deposit(20, "H505", 300)
# bank.scheduled_payments(21, "H505", "A123", 100, "pending", 20)  # Succeeds
# bank.scheduled_payments(22, "H505", "B456", 300, "pending", 21)  # Fails due to

    def accept_transfer(self, timestamp: int, account_id: str, transfer_id: str) -> bool:
        self.last_operation_time = timestamp
        
        if transfer_id not in self.transfers:
            return False
        transfers_account = [t for t in self.transfers if t[transfer_id] == transfer_id  and t[status] == 'pending']
        now = time.time()
        if len(transfers_account) == 0:
            return False
        for tranfers in transfers_account:
            
            if  now - tranfers['created_time'] - now < timedelta(hours=24): 
                transfers['status'] = 'expired'
            elif tranfers['transfer_id'] == transfer_id:
                self.accounts[account_id]  += tranfers['withheld_amount']
                self.transactions.append((account_id,tranfers['withheld_amount'],timestamp,'+'))
                self.transactions.append((tranfers['source_account_id'],tranfers['withheld_amount'],timestamp,'-'))
                return True
                
    
        
        return False



