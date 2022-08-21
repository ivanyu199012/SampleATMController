import json
import unittest
from atm_controller import ATMController


class TestATMController(unittest.TestCase):

	def setUp(self):
		print ( f"Method: { self._testMethodName }" )
		self.atm_controller = ATMController()

	def test_success_read_card_info( self ):
		""" expect to get card_info """
		card_num = "123456789"
		expiry_date = "12/22"
		encryted_card_info = f'{{ "card_number": "{ card_num }", "expiry_date": "{ expiry_date }" }}'

		is_success, _, card_info_dict = self.atm_controller.read_card_info( encryted_card_info )

		self.assertEqual( is_success, True, 'card read failed' )
		self.assertEqual( card_info_dict['card_number'], "123456789", 'card number is not correct' )

	def test_failed_read_card_info_1( self ):
		""" expect to failed because no card number """
		wrong_card_info = '{ "expiry_date": "12/22" }'

		is_success, err_msg, _  = self.atm_controller.read_card_info( wrong_card_info )

		self.assertEqual( is_success, False, 'card read should not be read success in this case' )
		self.assertEqual( err_msg, "invalid card information", 'err_msg is not correct' )

	def test_failed_read_card_info_2( self ):
		""" expect to failed because no expiry date """
		wrong_card_info = '{ "card_number": "123456789" }'

		is_success, err_msg, _  = self.atm_controller.read_card_info( wrong_card_info )

		self.assertEqual( is_success, False, 'card read should not be read success in this case' )
		self.assertEqual( err_msg, "invalid card information", 'err_msg is not correct' )

	def test_failed_read_card_info_3( self ):
		""" expect to failed because card is expired """
		wrong_card_info = '{ "card_number": "123456789", "expiry_date": "12/21" }'

		is_success, err_msg, _  = self.atm_controller.read_card_info( wrong_card_info )

		self.assertEqual( is_success, False, 'card read should not be read success in this case' )
		self.assertEqual( err_msg, "invalid card information", 'err_msg is not correct' )

	def test_authenticate( self ):
		""" expect to success """
		card_number = "4024007180059403"
		pin = "1234"

		is_authenticated, _, access_token = self.atm_controller.authenticate( card_number, pin )

		self.assertEqual( is_authenticated, True, 'pin is incorrect or no this card information' )
		self.assertEqual( access_token is not None, True, 'no access token return' )

	def test_authenticate_wrong_pin( self ):
		""" expect to failed because of wrong pin """
		card_number = "4024007180059403"
		wrong_pin = "1245"

		is_authenticated, err_msg, access_token = self.atm_controller.authenticate( card_number, wrong_pin )

		self.assertEqual( is_authenticated, False, 'pin should not be correct' )
		self.assertEqual( err_msg, "card_number or pin incorrect", 'err_msg is incorrect' )
		self.assertEqual( access_token is None, True, 'access token should not exist' )

	def test_get_account_list( self ):
		""" expect to success to get account list """
		card_number = "4024007180059403"
		pin = "1234"

		is_authenticated, _, access_token = self.atm_controller.authenticate( card_number, pin )
		self.assertEqual( is_authenticated, True, 'pin is incorrect or no this card information' )

		is_success, _, account_list = self.atm_controller.get_account_list( access_token )
		self.assertEqual( is_success, True, 'get_account_list method failed' )
		self.assertEqual( len( account_list ), 3, 'account list length is not correct' )

	def test_get_account_balance( self ):
		""" expect to success to get account balance """
		card_number = "4024007180059403"
		pin = "1234"
		account_num = "73282088"

		is_authenticated, _, access_token = self.atm_controller.authenticate( card_number, pin )
		self.assertEqual( is_authenticated, True, 'pin is incorrect or no this card information' )

		is_success, account_balance = self.atm_controller.get_balance( access_token, account_num )
		self.assertEqual( is_success, True, 'get_account_balance method failed' )
		self.assertEqual( account_balance, 10001, 'account balance is not correct' )

	def test_get_account_balance( self ):
		""" expect to success to get account balance """
		card_number = "4024007180059403"
		pin = "1234"
		account_num = "73282088"

		is_authenticated, _, access_token = self.atm_controller.authenticate( card_number, pin )
		self.assertEqual( is_authenticated, True, 'pin is incorrect or no this card information' )

		is_success, account_balance = self.atm_controller.get_balance( access_token, account_num )
		self.assertEqual( is_success, True, 'get_account_balance method failed' )
		self.assertEqual( account_balance >= 0, True, 'account balance is not correct' )

	def test_withdraw( self ):
		""" expect to withdraw success """
		card_number = "4024007180059403"
		pin = "1234"
		account_num = "73282088"
		amount = 10

		is_authenticated, _, access_token = self.atm_controller.authenticate( card_number, pin )
		self.assertEqual( is_authenticated, True, 'pin is incorrect or no this card information' )

		is_success, account_balance = self.atm_controller.get_balance( access_token, account_num )
		self.assertEqual( is_success, True, 'get_account_balance method failed' )

		is_success, new_account_balance = self.atm_controller.withdraw( access_token, account_num, amount )
		self.assertEqual( is_success, True, 'withdraw method failed' )
		self.assertEqual( new_account_balance, account_balance - amount, 'account balance is not correct' )

	def test_deposit( self ):
		""" expect to deposit success """
		card_number = "4024007180059403"
		pin = "1234"
		account_num = "73282088"
		amount = 10

		is_authenticated, _, access_token = self.atm_controller.authenticate( card_number, pin )
		self.assertEqual( is_authenticated, True, 'pin is incorrect or no this card information' )

		is_success, account_balance = self.atm_controller.get_balance( access_token, account_num )
		self.assertEqual( is_success, True, 'get_account_balance method failed' )

		is_success, new_account_balance = self.atm_controller.deposit( access_token, account_num, amount )
		self.assertEqual( is_success, True, 'deposit method failed' )
		self.assertEqual( new_account_balance, account_balance + amount, 'account balance is not correct' )


if __name__ == '__main__':
	unittest.main()