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

if __name__ == '__main__':
	unittest.main()