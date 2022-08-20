from cryptography.fernet import Fernet

class CustomCrypto:

	fernet = Fernet( ( 'BurBW0Tx9oUgzvGQWX9QSLdeY3PJIM4ywyv9J7x6hUM=' ).encode() )

	@classmethod
	def decrypt( cls,  encrypted_str ):
		return cls.fernet.decrypt( encrypted_str.encode() ).decode()

	@classmethod
	def encrpyt( cls,  str ):
		return cls.fernet.encrypt( str.encode() ).decode()