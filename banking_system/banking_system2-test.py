import unittest
import time
from datetime import timedelta
from banking_system2 import BankingSystem  # Assuming BankingSystem is imported from its module


class TestBankingSystem(unittest.TestCase): 

    def setUp(self):
        # Setup before every test
        self.banking_system = BankingSystem()

    def test_create_account_success(self):
        # Test creating a new account
        timestamp = int(time.time())
        result = self.banking_system.create_account(timestamp, "acc1")
        self.assertTrue(result)
        self.assertIn("acc1", self.banking_system.accounts)
        self.assertEqual(self.banking_system.accounts["acc1"], 0)

    def test_create_account_duplicate(self):
        # Test creating a duplicate account
        timestamp = int(time.time())
        self.banking_system.create_account(timestamp, "acc1")
        result = self.banking_system.create_account(timestamp, "acc1")
        self.assertFalse(result)  # Should return False for duplicate account

    def test_deposit_success(self):
        # Test depositing money into an existing account
        timestamp = int(time.time())
        self.banking_system.create_account(timestamp, "acc1")
        new_balance = self.banking_system.deposit(timestamp, "acc1", 500)
        self.assertEqual(new_balance, 500)

    def test_deposit_non_existent_account(self):
        # Test depositing to a non-existent account
        timestamp = int(time.time())
        result = self.banking_system.deposit(timestamp, "acc2", 500)
        self.assertIsNone(result)  # None is returned for non-existent accounts

    def test_pay_success(self):
        # Test successful payment from an account
        timestamp = int(time.time())
        self.banking_system.create_account(timestamp, "acc1")
        self.banking_system.deposit(timestamp, "acc1", 500)
        new_balance = self.banking_system.pay(timestamp, "acc1", 200)
        self.assertEqual(new_balance, 300)

    def test_pay_insufficient_balance(self):
        # Test payment failure due to insufficient balance
        timestamp = int(time.time())
        self.banking_system.create_account(timestamp, "acc1")
        self.banking_system.deposit(timestamp, "acc1", 100)
        result = self.banking_system.pay(timestamp, "acc1", 200)
        self.assertIsNone(result)  # None should be returned if balance is insufficient

    def test_pay_non_existent_account(self):
        # Test payment from a non-existent account
        timestamp = int(time.time())
        result = self.banking_system.pay(timestamp, "acc2", 100)
        self.assertIsNone(result)  # None should be returned if account doesn't exist

    def test_top_activity(self):
        # Test top activity feature
        timestamp = int(time.time())
        self.banking_system.create_account(timestamp, "acc1")
        self.banking_system.create_account(timestamp, "acc2")
        self.banking_system.deposit(timestamp, "acc1", 500)
        self.banking_system.deposit(timestamp, "acc2", 300)
        result = self.banking_system.top_activity(timestamp, 1)
        self.assertEqual(result, ['acc1(500)'])  # Should show acc1 as top activity

    def test_transfer_success(self):
        # Test a successful transfer between two accounts
        timestamp = int(time.time())
        self.banking_system.create_account(timestamp, "acc1")
        self.banking_system.create_account(timestamp, "acc2")
        self.banking_system.deposit(timestamp, "acc1", 500)

        transfer_id = self.banking_system.transfer(timestamp, "acc1", "acc2", 200)
        self.assertIsNotNone(transfer_id)  # Transfer ID should be returned
        self.assertEqual(self.banking_system.accounts["acc1"], 300)

    def test_transfer_same_account(self):
        # Test transfer to the same account should fail
        timestamp = int(time.time())
        self.banking_system.create_account(timestamp, "acc1")
        self.banking_system.deposit(timestamp, "acc1", 500)
        transfer_id = self.banking_system.transfer(timestamp, "acc1", "acc1", 200)
        self.assertIsNone(transfer_id)  # Should return None for self-transfer

    def test_transfer_insufficient_funds(self):
        # Test transfer failure due to insufficient funds
        timestamp = int(time.time())
        self.banking_system.create_account(timestamp, "acc1")
        self.banking_system.create_account(timestamp, "acc2")
        self.banking_system.deposit(timestamp, "acc1", 100)
        transfer_id = self.banking_system.transfer(timestamp, "acc1", "acc2", 200)
        self.assertIsNone(transfer_id)  # Should return None for insufficient funds

    def test_accept_transfer_success(self):
        # Test accepting a transfer
        timestamp = int(time.time())
        self.banking_system.create_account(timestamp, "acc1")
        self.banking_system.create_account(timestamp, "acc2")
        self.banking_system.deposit(timestamp, "acc1", 500)

        transfer_id = self.banking_system.transfer(timestamp, "acc1", "acc2", 200)
        self.assertIsNotNone(transfer_id)

        accepted = self.banking_system.accept_transfer(timestamp + 100, "acc2", transfer_id)
        self.assertTrue(accepted)
        self.assertEqual(self.banking_system.accounts["acc2"], 200)

    def test_accept_transfer_expired(self):
        # Test accepting an expired transfer (older than 24 hours)
        timestamp = int(time.time())
        self.banking_system.create_account(timestamp, "acc1")
        self.banking_system.create_account(timestamp, "acc2")
        self.banking_system.deposit(timestamp, "acc1", 500)

        transfer_id = self.banking_system.transfer(timestamp, "acc1", "acc2", 200)
        self.assertIsNotNone(transfer_id)

        # Simulate transfer acceptance after more than 24 hours
        future_time = timestamp + timedelta(hours=25).total_seconds()
        accepted = self.banking_system.accept_transfer(int(future_time), "acc2", transfer_id)
        self.assertFalse(accepted)  # Transfer should be expired

    def test_accept_transfer_invalid_id(self):
        # Test accepting a transfer with an invalid ID
        timestamp = int(time.time())
        self.banking_system.create_account(timestamp, "acc1")
        self.banking_system.create_account(timestamp, "acc2")
        self.banking_system.deposit(timestamp, "acc1", 500)

        transfer_id = self.banking_system.transfer(timestamp, "acc1", "acc2", 200)
        self.assertIsNotNone(transfer_id)

        accepted = self.banking_system.accept_transfer(timestamp + 100, "acc2", "invalid_transfer_id")
        self.assertFalse(accepted)  # Should return False for invalid transfer ID


if __name__ == "__main__":
    unittest.main()
