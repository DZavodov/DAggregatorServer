# Copyright DZavodov. All Rights Reserved.

import logging
import requests
from Resources.ResourceInterface import *
from argparse import Namespace
import re
from Utils import measuredForEach

_logger = logging.getLogger(__name__)
"""  """

class Steam(ResourceInterface):
	"""  """

	def getName():
		return "Steam"

	def getReference():
		return "https://store.steampowered.com/"

	@classmethod
	def getProductPrefix(cls):
		return f"{cls.getReference()}app/"

	@classmethod
	def getProductImagePrefix(cls) -> str:
		return "https://cdn.akamai.steamstatic.com/steam/apps/"

	@classmethod
	def getProducts(cls, APIKey: str, arguments: Namespace):
		products:list[Product] = []

		productsResponse = requests.get(f"https://api.steampowered.com/ISteamApps/GetAppList/v2/?key={APIKey}")

		if productsResponse.status_code != 200:
			_logger.error(f"productsResponse.status_code != 200 {productsResponse}")
			return products

		applist = productsResponse.json().get("applist")
		if not applist:
			_logger.error(f"not applist {productsResponse}")
			return
		apps:list[dict[int, any]] = applist.get("apps")
		if not apps or not isinstance(apps, list):
			_logger.error(f"not apps {applist}")
			return

		if arguments.productsOffset != None:
			apps = apps[arguments.productsOffset:]
		if arguments.productsMax != None:
			apps = apps[:arguments.productsMax]

		def getProductMeasured(app: dict[str, any], data):
			appIdStr = str(app.get("appid"))
			if not appIdStr:
				_logger.error(f"not appId {app}")
				return
			product = Product(appIdStr, app.get("name"))

			productResponse = requests.get(f"{cls.getReference()}api/appdetails?appids={appIdStr}&cc={arguments.locale}&key={APIKey}")
			if productResponse.status_code != 200:
				_logger.debug(f"productResponse.status_code != 200 {productResponse}")
				return

			app = productResponse.json().get(appIdStr)
			if not app:
				_logger.debug(f"not app {productResponse}")
				return

			appData:dict = app.get("data")
			if not appData or not isinstance(appData, dict):
				_logger.debug(f"not appData {app}")
				return

			def getAppPriceFormated(appData):
				appPriceOverview = appData.get("price_overview")
				if not appPriceOverview:
					return None
				return appPriceOverview.get("final_formatted")

			appPriceFormated = getAppPriceFormated(appData)
			if appPriceFormated:
				product.price = float(re.search(r"\d+(?:\.\d+)?", appPriceFormated.replace(u',', u'.')).group())
			else:
				if not appData.get("is_free"):
					_logger.debug(f'not appFinalFormated {app}')
					return

			product.imageRelativeReference = appIdStr + "/header.jpg"
			products.append(product)

		measuredForEach(apps, getProductMeasured, "Steam.getProducts(..) ")

		return products
