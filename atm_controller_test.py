import json
import unittest
from atm_controller import ATMController


class TestATMController(unittest.TestCase):

	def setUp(self):
		print ( f"Method: { self._testMethodName }" )
		self.atm_controller = ATMController()

	def test_is_read_card_success( self ):
		""" expect to get card_info """
		is_success = self.atm_controller.is_read_card_success("{ 'card_number': '123456789', 'expiry_date': '12/20' }")
		self.assertEqual( is_success, True, 'card read failed' )

if __name__ == '__main__':
	unittest.main()