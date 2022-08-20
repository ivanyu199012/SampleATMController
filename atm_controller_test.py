import json
import unittest
from atm_controller import ATMController


class TestATMController(unittest.TestCase):

	def setUp(self):
		print ( f"Method: { self._testMethodName }" )
		self.atm_controller = ATMController()

	def test_is_read_card_success( self ):
		""" expect to get card_info """
		is_success = self.atm_controller.is_read_card_success('{ "card_number": "123456789", "expiry_date": "12/22" }')
		self.assertEqual( is_success, True, 'card read failed' )

	def test_is_read_card_failed_1( self ):
		""" expect to failed because no card number """
		is_success = self.atm_controller.is_read_card_success('{ "expiry_date": "12/22" }')
		self.assertEqual( is_success, False, 'card read should not be read success in this case' )

	def test_is_read_card_failed_2( self ):
		""" expect to failed because no expiry date """
		is_success = self.atm_controller.is_read_card_success('{ "card_number": "123456789" }')
		self.assertEqual( is_success, False, 'card read should not be read success in this case' )

	def test_is_read_card_failed_3( self ):
		""" expect to failed because card is expired """
		is_success = self.atm_controller.is_read_card_success('{ "card_number": "123456789", "expiry_date": "12/21" }')
		self.assertEqual( is_success, False, 'card read should not be read success in this case' )

	def test_authenticate( self ):
		""" expect to success """
		self.atm_controller.is_read_card_success('{ "card_number": "4024007180059403", "expiry_date": "12/22" }')
		is_authenticated, access_token = self.atm_controller.authenticate( "1234" )
		self.assertEqual( is_authenticated, True, 'pin is incorrect or no this card information' )
		self.assertEqual( access_token != "", True, 'no access token return' )

	def test_authenticate_wrong_pin( self ):
		""" expect to failed because of wrong pin """
		self.atm_controller.is_read_card_success('{ "card_number": "4024007180059403", "expiry_date": "12/22" }')
		is_authenticated, access_token = self.atm_controller.authenticate( "1245" )
		self.assertEqual( is_authenticated, False, 'pin should not be correct' )
		self.assertEqual( access_token is None, True, 'access token should not exist' )

	def test_get_account_list( self ):
		""" expect to success to get account list """
		self.atm_controller.is_read_card_success('{ "card_number": "4024007180059403", "expiry_date": "12/22" }')
		_, access_token = self.atm_controller.authenticate( "1234" )
		is_success, account_list = self.atm_controller.get_account_list( access_token )
		self.assertEqual( is_success, True, 'get_account_list method failed' )
		self.assertEqual( len( account_list ), 3, 'account list length is not correct' )

	def test_get_account_balance( self ):
		""" expect to success to get account balance """
		self.atm_controller.is_read_card_success('{ "card_number": "4024007180059403", "expiry_date": "12/22" }')
		_, access_token = self.atm_controller.authenticate( "1234" )
		is_success, account_balance = self.atm_controller.get_balance( access_token, "73282088" )
		self.assertEqual( is_success, True, 'get_account_balance method failed' )
		self.assertEqual( account_balance, 10001, 'account balance is not correct' )



if __name__ == '__main__':
	unittest.main()