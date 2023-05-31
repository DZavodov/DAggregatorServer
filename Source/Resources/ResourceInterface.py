# Copyright DZavodov. All Rights Reserved.

from argparse import Namespace
from Resources.ResourceProduct import ResourceProduct as Product

class ResourceInterface:
	"""  """

	def getName() -> str:
		"""  """

		assert False

	def getReference() -> str:
		"""  """

		assert False

	@classmethod
	def getProductPrefix(cls) -> str:
		"""  """

		assert False

	@classmethod
	def getProductImagePrefix(cls) -> str:
		"""  """

		assert False

	@classmethod
	def getProducts(cls, APIKey: str, arguments: Namespace) -> list[Product]:
		"""  """

		assert False
