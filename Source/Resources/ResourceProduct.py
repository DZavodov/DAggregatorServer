# Copyright DZavodov. All Rights Reserved.

class ResourceProduct(object):
	"""  """

	def __init__(self, identificator: str, name: str, price = .0, imageRelativeReference = ""):
		"""  """

		self.id = identificator
		self.name = name
		self.price = price
		self.imageRelativeReference = imageRelativeReference

	def isValid(self) -> bool:
		"""  """

		return self.id and self.name and self.price >= 0 and self.imageRelativeReference
