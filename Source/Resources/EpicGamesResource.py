# Copyright DZavodov. All Rights Reserved.

import logging
from Resources.ResourceInterface import *
from epicstore_api import EpicGamesStoreAPI
import re

_logger = logging.getLogger(__name__)
"""  """

class EpicGames(ResourceInterface):
	"""  """

	def getName():
		return "EpicGames"

	def getReference():
		return "https://store.epicgames.com/"

	@classmethod
	def getProductPrefix(cls):
		return f"{cls.getReference()}p/"

	@classmethod
	def getProductImagePrefix(cls) -> str:
		"""  """

		return ""

	@classmethod
	def getProducts(cls, APIKey: str, arguments: Namespace):
		products:list[Product] = []

		#todo
		#if arguments.productsMax != None:
		#	apps = apps[:arguments.productsMax]

		api = EpicGamesStoreAPI(country=arguments.locale.upper())
		products: dict[str, Product] = {}
		offset = arguments.productsOffset if arguments.productsOffset != None else 0

		while True:
			xxx = api.fetch_store_games(count = 1000, start = offset)
			games = xxx['data']['Catalog']['searchStore']['elements']
			for game in games:
				if (game.get('productSlug') == None) or (not "title" in game) or (game.get('productSlug') == "[]"):
					continue
				gamePrice = game.get('price')
				gameId = game.get('id')
				if not gamePrice or not gameId:
					continue
				gameTotalPrice = gamePrice.get('totalPrice')
				if not gameTotalPrice:
					continue
				gameFmtPrice = gameTotalPrice.get('fmtPrice')
				if not gameFmtPrice:
					continue
				gameCategories = game.get("categories")
				gameDiscountPrice = gameFmtPrice.get('discountPrice')
				if gameCategories == None or len(gameCategories)<1 or gameDiscountPrice == None:
					continue

				game_thumbnail = None
				for image in game['keyImages']:
					if image['type'] == 'Thumbnail':
						game_thumbnail = image['url']
				
				relativeReference = game['productSlug'].rsplit('/home')[0].replace('/', '--')
				products.update({relativeReference: Product(relativeReference, game['title'],float(re.search(r"\d+(?:\.\d+)?", gameDiscountPrice.replace(u',', u'')).group()), game_thumbnail)})

				
			
			offset += 1000
			if len(games) < 1:
				break



		return products.values()
