#
import json
from bank_api import BankAPI
from logger import CustomLogger
from datetime import datetime
from dateutil.relativedelta import relativedelta
logger = CustomLogger.get_logger_by()

class ATMController:

	card_info_dict = None

	def is_read_card_success(self, encryted_card_info):
		""" Check whether the card info is valid or not
			and store the card info in cache if valid

		Args:
			encryted_card_info (str): encryted_card_info

		Returns:
			boolean: is_success
		"""
		try:
			_card_info_dict = json.loads( encryted_card_info )
			if self.__is_valid_card_info( _card_info_dict ):
				self.card_info_dict = _card_info_dict
				return True
			return False
		except Exception as e:
			logger.error( e )
			return False

	def authenticate(self, pin):
		"""authenticate the card and return the access_token if authenticated

		Args:
			pin (str): pin

		Returns:
			boolean: is_success
			str: access_token
		"""
		return BankAPI.authenticate( self.card_info_dict[ 'card_number' ], pin )

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


	def get_account_list( self, access_token ):
		return BankAPI.get_account_list( access_token )

	def get_balance(self, access_token, account_num):
		return BankAPI.get_account_balance( access_token, account_num )

	def withdraw(self, access_token, account_num, amount):
		return BankAPI.withdraw( access_token, account_num, amount)

	def deposit(self, access_token, account_num, amount):
		return BankAPI.deposit( access_token, account_num, amount)

