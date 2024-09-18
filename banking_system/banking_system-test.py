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
        self.bank.last_operation_time = 5
        self.bank.scheduled_payments(4, "A123", "B456", 100, "pending", 6)
        
        # Check and process the scheduled payment
        self.bank.check_scheduled_payments()

        # Assert that the payment has been processed
        expected_accounts = {'A123': 400, 'B456': 100,'C789': 1000}
        self.assertEqual(self.bank.accounts, expected_accounts)

    def test_case_7_failed_scheduled_payment_due_to_funds(self):
        # Modify balance to test payment failure
        self.bank.last_operation_time = 10
        self.bank.deposit(1, "A123", -400)  # Ensure insufficient funds
        
        # Schedule a payment that should fail
        self.bank.scheduled_payments(9, "A123", "B456", 600, "pending", 10)
        
        # Process scheduled payment, should fail due to insufficient funds
        self.bank.check_scheduled_payments()

        # Assert that the payment failed and accounts remain unchanged
        expected_accounts = {'A123': 100, 'B456': 0,'C789': 1000}
        self.assertEqual(self.bank.accounts, expected_accounts)

        # Assert that the payment status is 'failed'
        self.assertEqual(self.bank.scheduled[0]['status'], 'failed')

    def test_case_8_multiple_scheduled_payments(self):
        # Schedule a payment that will be processed
        self.bank.last_operation_time = 11
        self.bank.scheduled_payments(11, "A123", "B456", 300, "pending", 11)
        
        # Process scheduled payments
        self.bank.check_scheduled_payments()

        # Assert that the payment was processed successfully
        expected_accounts = {'A123': 200,'C789': 1000, 'B456': 300}
        self.assertEqual(self.bank.accounts, expected_accounts)

    def test_case_9_merge_accounts_success(self):
        # Merge two accounts and verify balances
        merged_account = self.bank.merge_accounts(12, "A123", "C789")

        # Assert that a new merged account exists and has the correct balance
        expected_accounts = {merged_account: 1500, 'B456': 0}
        self.assertEqual(self.bank.accounts, expected_accounts)

        # Assert that old accounts were removed
        self.assertNotIn("A123", self.bank.accounts)
        self.assertNotIn("C789", self.bank.accounts)

    def test_case_10_merge_accounts_transactions(self):
        # Perform some transactions before merging accounts
        self.bank.transfer(10, "A123", 200, "B456")  # Debit from A123
        self.bank.transfer(11, "C789", 500, "B456")  # Debit from C789
        
        # Merge accounts and verify the transactions are updated
        merged_account = self.bank.merge_accounts(12, "A123", "C789")

        # Check that the merged account has the updated transactions in the correct format
        expected_transactions = [
            (merged_account, 200, 10, '-'),  # Debit from A123
            (merged_account, 500, 11, '-')   # Debit from C789
        ]
        actual_transactions = [
            (t[0], t[1], t[2], t[3]) for t in self.bank.transactions if t[0] == merged_account
        ]
        self.assertEqual(actual_transactions, expected_transactions)


    def test_case_11_merge_accounts_scheduled_payments(self):
        # Schedule some payments for A123 and C789
        self.bank.scheduled_payments(10, "A123", "B456", 100, "pending", 12)
        self.bank.scheduled_payments(11, "C789", "B456", 200, "pending", 12)
        
        # Merge the accounts
        merged_account = self.bank.merge_accounts(12, "A123", "C789")

        # Check that the scheduled payments are correctly updated
        for payment in self.bank.scheduled:
            if payment['status'] == 'pending':
                self.assertEqual(payment['source_account_id'], merged_account)

    def test_case_12_merge_accounts_fails_for_non_existent_account(self):
        # Try to merge a valid and an invalid account
        result = self.bank.merge_accounts(13, "A123", "Z999")
        
        # Assert that the merge failed and no changes were made
        self.assertIsNone(result)
        self.assertIn("A123", self.bank.accounts)
        self.assertNotIn("Z999", self.bank.accounts)

    def test_case_13_merge_accounts_cancels_scheduled_payments(self):
        # Schedule a payment between the accounts
        self.bank.scheduled_payments(12, "A123", "C789", 100, "pending", 12)
        
        # Merge the accounts
        self.bank.merge_accounts(12, "A123", "C789")

        # Check that the scheduled payment is marked as 'cancelled'
        for payment in self.bank.scheduled:
            self.assertEqual(payment['status'], 'cancelled')


if __name__ == '__main__':
    unittest.main()
