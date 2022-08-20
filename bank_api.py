
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
					logger.info( db_dict[ card_number ] )
					return True, CustomCrypto.encrpyt( card_number )
			return False, None
