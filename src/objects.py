import datetime
import requests
from apikeys import *


def verifyCountry(countryCode):
    response = requests.get(PUB_HOL + "/AvailableCountries")
    countries = response.json()

    for country in countries:
        if country["countryCode"] == countryCode:
            return True

    return False


class HoliBot:
    def __init__(self):
        self.channel = None
        self.countries = {}
        self.hour = 15

    def setChannel(self, channel):
        self.channel = channel

    def setTime(self, time):
        if 0 <= int(time) <= 24:
            self.hour = int(time)

            return True
        else:
            return False

    def addCountry(self, countryCode, countryObj):
        self.countries.update({countryCode: countryObj})


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

