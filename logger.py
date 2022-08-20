#
from datetime import datetime
from enum import Enum
import logging
from logging.handlers import TimedRotatingFileHandler
import os

class CustomLogger:

	__LOGGER_NAME = "ATM_CONTROLLER_LOG"

	def __new__(self,):
		if not hasattr(self, 'instance'):
			self.instance = super( CustomLogger, self ).__new__(self)

			LOG_FOLDER_NAME = 'log'

			self.__create_folder_if_not_exist( LOG_FOLDER_NAME )

			logFormatter = logging.Formatter( '[ %(asctime)s ][ %(levelname)s ][ %(funcName)s ] %(message)s' )
			customLogger = logging.getLogger( self.__LOGGER_NAME )

			today_date_str = datetime.now().strftime( "%Y-%m-%d" )
			fileHandler = TimedRotatingFileHandler( f'{ LOG_FOLDER_NAME }/{ today_date_str }.log', when='D', interval=1, backupCount=30, encoding='utf-8' )
			fileHandler.setFormatter( logFormatter )
			customLogger.addHandler( fileHandler )

			consoleHandler = logging.StreamHandler()
			consoleHandler.setFormatter( logFormatter )
			customLogger.addHandler( consoleHandler )
			customLogger.setLevel( logging.INFO )
			customLogger.propagate = False

		return self.instance

	@classmethod
	def get_logger_by( self ):
		# Init logger if needed
		self()
		return logging.getLogger( self.__LOGGER_NAME )

	@classmethod
	def __create_folder_if_not_exist(self, path):
		if not os.path.exists( path ):
			os.makedirs( path )
