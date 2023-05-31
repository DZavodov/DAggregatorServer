# Copyright DZavodov. All Rights Reserved.

import logging
import time
from collections.abc import Callable

__logger = logging.getLogger(__name__)
"""  """

def intToHMS(value: int):
	"""  """

	return f"{value // 3600 :2}:{(value % 3600) // 60 :2}:{value % 60 :2}"

def measuredForEach(elements: list, functor: Callable[[any, any], None], prefix = "", data = None):
	"""  """

	length = len(elements)
	number = 0

	throbber = ['-', '\\', '|', '/']
	throbberLen = len(throbber)

	startTime = time.time()
	for element in elements:
		number += 1
		print(f"{throbber[number % throbberLen]} {prefix}{number}/{length} {number/length:.2f} [{intToHMS(int((time.time() - startTime) / number * (length - number)))}]", end = "\r")

		functor(element, data)

	__logger.info(f"{prefix}for {length} elements - duration [{intToHMS(int(time.time() - startTime))}]")
