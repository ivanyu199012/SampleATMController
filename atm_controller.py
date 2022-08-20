#
import json
from logger import CustomLogger
from datetime import datetime
from dateutil.relativedelta import relativedelta
logger = CustomLogger.get_logger_by()

class ATMController:

	card_info_dict = None

	# When reading the card information, the primary source should be encrpyted
	# For simplicity, here we just use the json string for encryted_card_info
	# read_card_info_by is the method to decrpyt the card information
	# and store it in the cache so it can be used later for other operations
	def is_read_card_success(self, encryted_card_info):
		try:
			_card_info_dict = json.loads( encryted_card_info )
			if self.__is_valid_card_info( _card_info_dict ):
				self.card_info_dict = _card_info_dict
				return True
			return False
		except Exception as e:
			logger.error( e )
			return False

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

	def withdraw(self, amount):
		self.atm.withdraw(amount)

	def deposit(self, amount):
		self.atm.deposit(amount)

	def balance(self):
		return self.atm.balance()

	def show_menu(self):
		print("""
		1. Withdraw
		2. Deposit
		3. Balance
		4. Exit
		""")

	def run(self):
		while True:
			self.show_menu()
			choice = int(input("Enter your choice: "))
			if choice == 1:
				amount = int(input("Enter amount to withdraw: "))
				self.withdraw(amount)
			elif choice == 2:
				amount = int(input("Enter amount to deposit: "))
				self.deposit(amount)
			elif choice == 3:
				print("Your balance is: {}".format(self.balance()))
			elif choice == 4:
				break
			else:
				print("Invalid choice")