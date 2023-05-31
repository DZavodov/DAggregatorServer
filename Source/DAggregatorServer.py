# Copyright DZavodov. All Rights Reserved.

from argparse import Namespace
import logging
from Databases.DatabaseInterface import DatabaseInterface
from Resources.ResourceInterface import ResourceInterface
from datetime import datetime
from Resources.ResourceProduct import ResourceProduct
from Utils import measuredForEach

_logger = logging.getLogger(__name__)
"""  """

class DAgregatorServer():
	"""  """

	def __init__(self, database: DatabaseInterface, resources: list[ResourceInterface], APIKeys: dict[str, str], arguments: Namespace):
		"""  """

		self.__database = database
		"""  """
		self.__resources = resources
		"""  """
		self.__APIKeys = APIKeys
		"""  """
		self.__arguments = arguments
		"""  """

	def update(self):
		"""  """

		def updateResourceMeasured(resource: ResourceInterface, data):
			APIKey:str = self.__APIKeys.get(resource.getName())
			if APIKey == None:
				_logger.error(f"APIKey == None {resource.getName()}")
				return

			_logger.info(resource.getName())

			resourceName = resource.getName()
			if self.__arguments.test:
				resourceName = "test/" + resourceName

			resourceUpdateIndexName = resourceName + "/updateIndex"
			updateIndex = self.__database.get(resourceUpdateIndexName)
			if not updateIndex:
				updateIndex = 0
			updateIndex += 1

			self.__database.set(resourceUpdateIndexName, updateIndex)
			self.__database.set(resourceName + "/productPrefix", resource.getProductPrefix())
			self.__database.set(resourceName + "/productImagePrefix", resource.getProductImagePrefix())

			class SetProductToDatabaseData:
				def __init__(self):
					self.validCounter = 0

			def setProductToDatabaseMeasured(product: ResourceProduct, data: SetProductToDatabaseData):
				if not product.isValid():
					_logger.debug(f"not product.isValid() product = {str(product)}")
					return

				data.validCounter += 1

				productPrices = self.__database.get(f"{resourceName}/data/{product.id}/prices/{self.__arguments.locale}")
				unixTimeStamp = int(round(datetime.utcnow().timestamp()))
				productPrice = {"unixTimeStamp": unixTimeStamp, "value": product.price}
				if not productPrices or len(productPrices) <= 0:
					productPrices = [productPrice]
				else:
					oldProductPrice = productPrices[0]

					oldProductPriceUnixTimeStamp = oldProductPrice.get("unixTimeStamp")
					oldProductPriceValue = oldProductPrice.get("value")

					if not oldProductPriceUnixTimeStamp or oldProductPriceValue == None:
						_logger.error(f"not oldProductPriceUnixTimeStamp or not oldProductPriceValue {productPrices}")
						productPrices = [productPrice]
					else:
						if unixTimeStamp >= oldProductPriceUnixTimeStamp + self.__arguments.updatePricesTimeLock:
							productPrices.insert(0, productPrice)
						elif product.price != oldProductPriceValue:
							productPrices[0] = productPrice

						productPrices = productPrices[:self.__arguments.pricesSize]

				self.__database.set(f"{resourceName}/data/{product.id}/prices/{self.__arguments.locale}", productPrices)
				self.__database.set(f"{resourceName}/data/{product.id}/imageRelativeReference", product.imageRelativeReference)
				self.__database.set(f"{resourceName}/search/{product.id}", {"updateIndex": updateIndex, "name": product.name})

			setProductToDatabaseData = SetProductToDatabaseData()
			measuredForEach(resource.getProducts(APIKey, self.__arguments), setProductToDatabaseMeasured, "DAgregatorServer._updateResource(..) ", setProductToDatabaseData)
			_logger.info(f"Valid products {setProductToDatabaseData.validCounter}")

		measuredForEach(self.__resources, updateResourceMeasured, "DAgregatorServer.update(..) ")

