import datetime
import requests
from apikeys import *


class HolidaySet:
    def __init__(self, countryCode):
        self.year = datetime.datetime.now().year
        self.countryCode = countryCode
        self.data = None

    def setData(self):
        response = requests.get(PUB_HOL + "/publicholidays/{}/{}".format(self.year, self.countryCode),
                                params={'Year': self.year, 'CountryCode': self.countryCode})

        self.data = response.json()

    def announceHolidays(self, currentHolidays):
        pass