import logging
from datetime import datetime
import json


def MainWork(mainPath):

    URLArr = []

    csPath = mainPath + '/CloudService.log'

    logging.basicConfig(filename=csPath, level=logging.INFO)

    logging.info("Starting... %s" % (datetime.today()))
    # time.sleep(max(0, 60-(time.time() % 60)))
    logging.info("Started... %s" % (datetime.today()))

    ConfigFilesPath = mainPath + '/ConfigFiles/'

    # Get URL and  folders path
    logging.info("Loading URL and  folders path... %s" % (datetime.today()))
    with open(ConfigFilesPath + 'URLs.json') as f:
        URLs = json.loads(f.read())

    URLArr.append(URLs[0]["urlLB"])
    URLArr.append(URLs[0]["urlMO"])
    URLArr.append(URLs[0]["urlLF"])

    return URLArr