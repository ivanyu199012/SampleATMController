
import json
from logger import CustomLogger
from custom_crypto import CustomCrypto
logger = CustomLogger.get_logger_by()

class BankAPI:

	@classmethod
	def authenticate( self, card_number, pin ):
		with open('db/db.json', 'r') as db_json_file:
			db_dict = json.load( db_json_file )
			if not card_number in db_dict or pin != db_dict[ card_number ][ 'pin' ] :
				return False, "card_number or pin incorrect", None
			if pin == db_dict[ card_number ][ 'pin' ]:
				return True, None, card_number

	@classmethod
	def get_account_list( self, card_number ):
		with open('db/db.json', 'r') as db_json_file:
			db_dict = json.load( db_json_file )
			if not card_number in db_dict:
				return False, "card number not found", None

			account_list = db_dict[ card_number ][ 'accounts' ]
			_account_list = [ { 'account_num': account[ 'account_num' ], 'name': account[ 'name' ] } for account in account_list ]
			return True, None, _account_list


	@classmethod
	def get_account_balance( self, access_token, account_num ):
		is_success = True
		try:
			card_number = CustomCrypto.decrypt( access_token )
			with open('db/db.json', 'r') as db_json_file:
				db_dict = json.load( db_json_file )
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

	@classmethod
	def withdraw( self, access_token, account_num, amout ):
		is_success = True
		new_balance = -1
		try:
			card_number = CustomCrypto.decrypt( access_token )
			with open('db/db.json', 'r+') as db_json_file:
				db_dict = json.load( db_json_file )
				if card_number in db_dict:
					account_list = db_dict[ card_number ][ 'accounts' ]
					account_index = -1
					for i in range( len( account_list ) ):
						if account_list[ i ][ 'account_num' ] == account_num:
							account_index = i
							break

					if account_list[ i ][ 'balance' ] < amout:
						logger.warning( f'Account {account_num} has insufficient balance' )
						return False, None

					new_balance = db_dict[ card_number ][ 'accounts' ][ account_index ][ 'balance' ] - amout
					db_dict[ card_number ][ 'accounts' ][ account_index ][ 'balance' ] = new_balance

					db_json_file.seek( 0 )
					json.dump( db_dict, db_json_file, indent=4, sort_keys=True )
					db_json_file.truncate()

			return is_success, new_balance
		except Exception as e:
			is_success = False
			logger.error( e )
			return is_success, None


	@classmethod
	def deposit( self, access_token, account_num, amout ):
		is_success = True
		new_balance = -1
		try:
			card_number = CustomCrypto.decrypt( access_token )
			with open('db/db.json', 'r+') as db_json_file:
				db_dict = json.load( db_json_file )
				if card_number in db_dict:
					account_list = db_dict[ card_number ][ 'accounts' ]
					account_index = -1
					for i in range( len( account_list ) ):
						if account_list[ i ][ 'account_num' ] == account_num:
							account_index = i
							break

					new_balance = db_dict[ card_number ][ 'accounts' ][ account_index ][ 'balance' ] + amout
					db_dict[ card_number ][ 'accounts' ][ account_index ][ 'balance' ] = new_balance

					db_json_file.seek( 0 )
					json.dump( db_dict, db_json_file, indent=4, sort_keys=True )
					db_json_file.truncate()

			return is_success, new_balance
		except Exception as e:
			is_success = False
			logger.error( e )
			return is_success, None
