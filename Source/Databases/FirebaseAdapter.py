# Copyright DZavodov. All Rights Reserved.

import logging
from Databases.DatabaseInterface import *

_logger = logging.getLogger(__name__)
"""  """

class FirebaseAdapter(DatabaseInterface):
	"""  """

	def __init__(self, database):
		"""  """

		self.__database = database
		"""  """

	def get(self, key: str):
		return self.__database.reference(f"/{key}").get()

	def set(self, key: str, value):
		self.__database.reference(f"/{key}").set(value)
