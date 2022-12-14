#
import json
from bank_api import BankAPI
from custom_crypto import CustomCrypto
from logger import CustomLogger
from datetime import datetime
from dateutil.relativedelta import relativedelta
logger = CustomLogger.get_logger_by()

class ATMController:

	def read_card_info(self, encryted_card_info):
		""" Check whether the card info is valid or not
			and store the card info in cache if valid

		Args:
			encryted_card_info (str): encryted_card_info, for simplicity, we only used json string here

		Returns:
			boolean: is_success
			str: error message
			dict: card_info_dict, None if the method failed
		"""
		try:
			_card_info_dict = json.loads( encryted_card_info )
			if self.__is_valid_card_info( _card_info_dict ):
				return True, None, _card_info_dict
			return False, 'invalid card information', None
		except Exception as e:
			logger.error( e )
			return False, str( e ), None

	def authenticate(self, card_number, pin):
		"""authenticate the card and return the access_token if authenticated

		Args:
			pin (str): pin

		Returns:
			boolean: is_success
			str: error message
			str: access_token, None if the method failed
		"""
		try:
			is_success, err_msg, card_number = BankAPI.authenticate( card_number, pin )
			access_token = CustomCrypto.encrpyt( card_number ) if is_success else None
			return is_success, err_msg, access_token
		except Exception as e:
			logger.error( e )
			return False, str(e), None

	def get_account_list( self, access_token ):
		"""get account list by access token

		Args:
			access_token (str): access_token

		Returns:
			boolean: is_success
			str: error message
			list: account_list, None if the method failed
		"""
		try:
			card_number = CustomCrypto.decrypt( access_token )
			return BankAPI.get_account_list( card_number )
		except Exception as e:
			logger.error( e )
			return False, str(e), None

	def get_balance(self, access_token, account_num):
		"""get account balance

		Args:
			access_token (str):
			account_num (str):

		Returns:
			boolean: is_success
			str: error message
			int: balance, None if the method failed
		"""
		try:
			card_number = CustomCrypto.decrypt( access_token )
			return BankAPI.get_account_balance( card_number, account_num )
		except Exception as e:
			logger.error( e )
			return False, str( e ), None

	def withdraw(self, access_token, account_num, amount):
		"""withdraw the amount from the account

		Args:
			access_token (str):
			account_num (str):
			amount (int):

		Returns:
			boolean: is_success
			str: error message
			int: new_balance after withdraw, None if the method failed
		"""
		try:
			card_number = CustomCrypto.decrypt( access_token )
			return BankAPI.withdraw( card_number, account_num, amount)
		except Exception as e:
			logger.error( e )
			return False, str( e ), None

	def deposit(self, access_token, account_num, amount):
		"""deposit the amount from the account

		Args:
			access_token (str):
			account_num (str):
			amount (int):

		Returns:
			boolean: is_success
			str: error message
			int: new_balance after deposit, None if the method failed
		"""
		try:
			card_number = CustomCrypto.decrypt( access_token )
			return BankAPI.deposit( card_number, account_num, amount)
		except Exception as e:
			logger.error( e )
			return False, str( e ), None

	def __is_valid_card_info( self, _card_info_dict ):
		if 'card_number' not in _card_info_dict:
			logger.warning( f'Read Card Failed. card_number not found' )
			return False

		if 'expiry_date' not in _card_info_dict:
			logger.warning( f'Read Card Failed. expiry_date not found' )
			return False

		card_expiry_date = datetime.strptime( _card_info_dict[ 'expiry_date' ], '%m/%y' )
		expiry_date = card_expiry_date + relativedelta(months=1)
		if expiry_date <= datetime.now():
			logger.warning( f'The card is expired. expiry_date = { card_expiry_date }')
			return False

		return True

