
import json
from logger import CustomLogger
from custom_crypto import CustomCrypto
logger = CustomLogger.get_logger_by()

class BankAPI:

	@classmethod
	def authenticate( self, card_number, pin ):
		with open('db/db.json', 'r') as db_json_str:
			db_dict = json.load( db_json_str )
			if card_number in db_dict:
				if pin == db_dict[ card_number ][ 'pin' ]:
					return True, CustomCrypto.encrpyt( card_number )
			return False, None

	@classmethod
	def get_account_list( self, access_token ):
		is_success = True
		try:
			card_number = CustomCrypto.decrypt( access_token )
			with open('db/db.json', 'r') as db_json_str:
				db_dict = json.load( db_json_str )
				if card_number in db_dict:
					account_list = db_dict[ card_number ][ 'accounts' ]
					_account_list = []
					for account in account_list:
						_account_list.append( { 'account_num': account[ 'account_num' ], 'name': account[ 'name' ] } )
					return is_success, _account_list
		except Exception as e:
			is_success = False
			logger.error( e )
			return is_success, None

	@classmethod
	def get_account_balance( self, access_token, account_num ):
		is_success = True
		try:
			card_number = CustomCrypto.decrypt( access_token )
			with open('db/db.json', 'r') as db_json_str:
				db_dict = json.load( db_json_str )
				if card_number in db_dict:
					account_list = db_dict[ card_number ][ 'accounts' ]
					account_balance = 0
					for account in account_list:
						if account[ 'account_num' ] == account_num:
							account_balance = account[ 'balance' ]
							break
					return is_success, account_balance
		except Exception as e:
			is_success = False
			logger.error( e )
			return is_success, None
