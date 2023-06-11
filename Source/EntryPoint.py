# Copyright DZavodov. All Rights Reserved.

import logging
import argparse
from pathlib import Path
import logging.config
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from Resources.SteamResource import Steam
from Resources.EpicGamesResource import EpicGames
from Resources.MegafonResource import Megafon
from Databases.FirebaseAdapter import FirebaseAdapter
from DAggregatorServer import DAgregatorServer

__logger = logging.getLogger(__name__)
"""  """

def makeFilterLess(level):
	"""  """

	level = getattr(logging, level)

	return lambda record: record.levelno < level

# Entry point.
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-l", "--locale", type=str, default="en", help = "Resources locale.")
	parser.add_argument("--pricesSize", type=int, default=100, help = "Product prises size limit.")
	parser.add_argument("--updatePricesTimeLock", type=int, default=86400, help = "Time in seconds that blocks adding to the price history..")
	parser.add_argument("-t", "--test", help = "Is testing.")
	parser.add_argument("-r", "--resourceNames", nargs='+', help = "Resource classes.")
	parser.add_argument("--productsOffset", type = int, help = "Products offset per resource.")
	parser.add_argument("--productsMax", type = int, help = "Maximum products per resource.")
	arguments = parser.parse_args()

	userLoggersConfigPath = Path("Configs/UserLoggers.json")
	logging.config.dictConfig(json.load(open(userLoggersConfigPath if Path(userLoggersConfigPath).is_file() else "Configs/DefaultLoggers.json", "r")))

	__logger.info(f"Begin {arguments}")

	with open("Configs/FirebaseAPIKey.json") as firibaseApiKeyFile:
		firibaseApiKey = json.load(firibaseApiKeyFile)
	firebase_admin.initialize_app(credentials.Certificate(firibaseApiKey), {
		"databaseURL": f"https://{firibaseApiKey['project_id']}-default-rtdb.firebaseio.com/"
	})
	with open("Configs/ResourcesAPIKeys.json") as APIKeysFile:
		APIKeys = json.load(APIKeysFile)

	resources = [Steam, EpicGames, Megafon]
	if arguments.resourceNames != None:
		argumentResources = []
		for resource in resources:
			for argumentResourceName in arguments.resourceNames:
				if resource.getName() == argumentResourceName:
					argumentResources.append(resource)
		resources = argumentResources

	server = DAgregatorServer(FirebaseAdapter(firebase_admin.db), resources, APIKeys, arguments)
	server.update()
