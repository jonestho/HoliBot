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