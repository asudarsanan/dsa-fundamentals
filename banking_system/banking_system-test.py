import unittest
from banking_system import BankingSystem

class TestBankingSystem(unittest.TestCase):

    def setUp(self):
        # Create a fresh instance of BankingSystem before each test
        self.bank = BankingSystem()

        # Create common accounts and deposit amounts needed for multiple tests
        self.bank.create_account(1, "A123")
        self.bank.create_account(3, "C789")
        self.bank.create_account(2, "B456")  # Created in tests that use B456
        
        # Pre-populate some balances for testing
        self.bank.deposit(4, "A123", 500)
        self.bank.deposit(4, "C789", 1000)

    def set_last_operation_time(self, timestamp):
        """Helper method to set the last_operation_time for scheduled payment tests"""
        self.bank.last_operation_time = timestamp

    def test_case_1_basic_transfer(self):
        # Perform transfers
        self.bank.transfer(5, "A123", 200, "B456")
        self.bank.transfer(6, "A123", 200, "B456")

        # Assert top spenders
        expected_top_spenders = ['A123(400)']
        self.assertEqual(self.bank.top_spenders(6, 2), expected_top_spenders)

    def test_case_2_multiple_accounts_transfers(self):
        # Perform transfers
        self.bank.transfer(5, "C789", 300, "A123")
        self.bank.transfer(6, "C789", 500, "B456")
        self.bank.transfer(5, "A123", 200, "B456")
        self.bank.transfer(6, "A123", 100, "B456")

        # Assert top spenders
        expected_top_spenders = ['C789(800)', 'A123(300)']
        self.assertEqual(self.bank.top_spenders(6, 3), expected_top_spenders)

    def test_case_3_timestamp_filtering(self):
        # Perform additional transfers for timestamp filtering test
        self.bank.transfer(5, "C789", 300, "A123")
        self.bank.transfer(6, "C789", 500, "B456")
        self.bank.transfer(5, "A123", 200, "B456")
        self.bank.transfer(6, "A123", 100, "B456")
        self.bank.transfer(5, "C789", 300, "A123")
        self.bank.transfer(7, "A123", 100, "B456")

        # Assert top spenders with timestamp filtering
        expected_top_spenders = ['C789(800)','A123(300)']
        self.assertEqual(self.bank.top_spenders(6, 2), expected_top_spenders)

    def test_case_4_no_transactions_before_timestamp(self):
        # Assert that no transactions are found before the first timestamp
        expected_top_spenders = []
        self.assertEqual(self.bank.top_spenders(0, 2), expected_top_spenders)

    def test_case_5_less_than_n_accounts_available(self):
        # Perform transfers
        self.bank.transfer(7, "A123", 200, "B456")

        # Assert top spenders when asking for more than available accounts
        expected_top_spenders = ['A123(200)']
        self.assertEqual(self.bank.top_spenders(7, 5), expected_top_spenders)

    def test_case_6_schedule_payment_processes_on_time(self):
        # Schedule a payment
        self.set_last_operation_time(5)
        self.bank.scheduled_payments(4, "A123", "B456", 100, "pending", 6)
        
        # Check and process the scheduled payment
        self.bank.check_scheduled_payments()

        # Assert that the payment has been processed
        expected_accounts = {'A123': 400, 'B456': 100, 'C789': 1000}
        self.assertEqual(self.bank.accounts, expected_accounts)

    def test_case_7_failed_scheduled_payment_due_to_funds(self):
        # Modify balance to test payment failure
        self.set_last_operation_time(10)
        self.bank.deposit(1, "A123", -400)  # Ensure insufficient funds
        
        # Schedule a payment that should fail
        self.bank.scheduled_payments(9, "A123", "B456", 600, "pending", 10)
        
        # Process scheduled payment, should fail due to insufficient funds
        self.bank.check_scheduled_payments()

        # Assert that the payment failed and accounts remain unchanged
        expected_accounts = {'A123': 100, 'B456': 0, 'C789': 1000}
        self.assertEqual(self.bank.accounts, expected_accounts)

        # Assert that the payment status is 'failed'
        self.assertEqual(self.bank.scheduled[0]['status'], 'failed')

    def test_case_8_multiple_scheduled_payments(self):
        # Schedule a payment that will be processed
        self.set_last_operation_time(11)
        self.bank.scheduled_payments(11, "A123", "B456", 300, "pending", 11)
        
        # Process scheduled payments
        self.bank.check_scheduled_payments()

        # Assert that the payment was processed successfully
        expected_accounts = {'A123': 200, 'C789': 1000, 'B456': 300}
        self.assertEqual(self.bank.accounts, expected_accounts)

    # Edge case 1: Merging accounts where one or both accounts do not exist
    def test_merge_accounts_non_existent(self):
        merged_account = self.bank.merge_accounts(12, "A123", "D456")  # D456 doesn't exist
        self.assertIsNone(merged_account)

    # Edge case 2: Merging accounts with zero balances
    def test_merge_zero_balance_accounts(self):
        self.bank.create_account(8, "Z001")
        self.bank.create_account(8, "Z002")
        merged_account = self.bank.merge_accounts(9, "Z001", "Z002")
        expected_balance = 0
        self.assertEqual(self.bank.accounts[merged_account], expected_balance)

    # Edge case 3: Merging accounts with pending scheduled payments
    def test_merge_accounts_with_scheduled_payments(self):
        # Schedule payments before the merge
        self.set_last_operation_time(9)

        # Scheduled payment between merged accounts (should be canceled)
        self.bank.scheduled_payments(10, "A123", "B456", 100, "pending", 10)

        # Scheduled payment not involving merged accounts (should be migrated)
        self.bank.scheduled_payments(10, "A123", "C789", 200, "pending", 10)

        # Merge accounts A123 and B456
        merged_account = self.bank.merge_accounts(12, "A123", "B456")

        # Assert that the payment involving both accounts is canceled
        self.assertEqual(self.bank.scheduled[0]['status'], 'cancelled')

        # Assert that unrelated payments are updated with the merged account
        self.assertEqual(self.bank.scheduled[1]['source_account_id'], merged_account)
        self.assertEqual(self.bank.scheduled[1]['status'], 'pending')


    # Edge case 4: Transfer to the same account
    def test_transfer_to_same_account(self):
        initial_balance = self.bank.accounts["A123"]
        self.bank.transfer(8, "A123", 100, "A123")
        self.assertEqual(self.bank.accounts["A123"], initial_balance)

    # Edge case 5: Merging accounts with negative balances
    def test_merge_negative_balances(self):
        self.bank.deposit(8, "A123", -600)  # Overdrawn account
        merged_account = self.bank.merge_accounts(9, "A123", "C789")
        expected_balance = 500 - 600 + 1000
        self.assertEqual(self.bank.accounts[merged_account], expected_balance)

    # Edge case 6: Scheduled payments after merging source/target accounts
def test_scheduled_payments_after_merge(self):
    # Set the operation time and schedule payments
    self.set_last_operation_time(9)

    # Schedule a payment between the merging accounts (should be canceled)
    self.bank.scheduled_payments(10, "A123", "B456", 100, "pending", 10)
    
    # Schedule unrelated payments (should be migrated to the merged account)
    self.bank.scheduled_payments(11, "C789", "A123", 200, "pending", 11)
    self.bank.scheduled_payments(11, "B456", "C789", 300, "pending", 11)

    # Merge accounts A123 and B456
    merged_account = self.bank.merge_accounts(12, "A123", "B456")

    # Assert that the payment between merged accounts is canceled
    self.assertEqual(self.bank.scheduled[0]['status'], 'cancelled')
    
    # Assert that unrelated payments are migrated to the merged account
    self.assertEqual(self.bank.scheduled[1]['target_account_id'], merged_account)  # A123 merged into A123_B456
    self.assertEqual(self.bank.scheduled[2]['source_account_id'], merged_account)  # B456 merged into A123_B456

    # Ensure the status of migrated payments remains unchanged
    self.assertEqual(self.bank.scheduled[1]['status'], 'pending')
    self.assertEqual(self.bank.scheduled[2]['status'], 'pending')

if __name__ == '__main__':
    unittest.main()
