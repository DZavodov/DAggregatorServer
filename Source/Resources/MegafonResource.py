# Copyright DZavodov. All Rights Reserved.

import logging
from Resources.ResourceInterface import *
from bs4 import BeautifulSoup
import requests
import hashlib

_logger = logging.getLogger(__name__)
"""  """

class Megafon(ResourceInterface):
	"""  """

	def getName():
		return "Megafon"

	def getReference():
		return "https://mordovia.shop.megafon.ru"

	@classmethod
	def getProductPrefix(cls):
		return cls.getReference()

	@classmethod
	def getProductImagePrefix(cls) -> str:
		"""  """

		return cls.getReference()

	@classmethod
	def getProducts(cls, APIKey: str, arguments: Namespace):
		products:list[Product] = []

		headers = {
			'X-Requested-With': 'XMLHttpRequest',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 OPR/98.0.0.0 (Edition Yx GX)'
		}
		session = requests.session()
		session.headers.update(headers)

		for search in ["mobile","notebooks/laptops"]:
			page = session.get(f'https://mordovia.shop.megafon.ru/{search}?show_all')

			for rawProduct in BeautifulSoup(page.text, 'html.parser').find_all('div', class_='b-goods-list__item'):
				rawPrice = rawProduct.find('span', class_='b-price-good-list__value b-price__value')
				if not rawPrice:
					continue
				price = float(rawPrice.text.replace(' ' , ''))
				
				products.append(Product(hashlib.sha256((rawProduct.a.text).encode('utf-32', "ignore")).hexdigest(), rawProduct.a.text, price, rawProduct.find('div', class_='b-good__photo-wrap photoWrap').img['data-lazy']))
			

		return products
