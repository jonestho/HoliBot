import discord
from discord.ext import commands, tasks
from googlesearch import search
from objects import *
import numpy as np
import pycountry_convert

client = commands.Bot(command_prefix="hb:", intents=discord.Intents.all())
clientData = HoliBot()

dateTime = datetime.datetime.now()
currentHour = dateTime.hour


@client.event
async def on_ready():
    print("----------------------------------------")
    print("HoliBot is now ready to receive commands")
    print("----------------------------------------")

    send_message.start()


@client.command()
async def channel(ctx):
    clientData.setChannel(ctx.channel)
    await clientData.channel.send("All messages from HoliBot will be sent here!")


@client.command()
async def time(ctx, hour):
    result = clientData.setTime(hour)

    if result:
        await ctx.send("Time for holiday updates successfully set!")
    else:
        await ctx.send("Oops! This is an invalid hour. Please try again with a number from 0 to 24")


@client.command()
async def add(ctx, countryCode):
    if clientData.channel is not None:
        ctx = clientData.channel

    result = verifyCountry(countryCode)

    if result:
        holidaySet = HolidaySet(countryCode)

        if countryCode not in clientData.countries:
            holidaySet.setData()
            clientData.addCountry(countryCode, holidaySet.data)

            await ctx.send("Successfully added holidays from the provided Country!")
        else:
            await ctx.send("Oops, this country has already been added!")

    else:
        await ctx.send("Oops! An error occurred. Please try a different country code.")


@client.command()
async def info(ctx):
    if clientData.channel is not None:
        ctx = clientData.channel

    await ctx.send("Hello, I am the HoliBot! I send messages/notifications that honor the many International Holidays "
                   "that exist. Using the \"hb:\" prefix, you can set the time zone, find information about the "
                   "current holiday, and more! I hope you enjoy what I have to offer and thank you for adding me to "
                   "your server :)")


@client.command()
async def _help(ctx):
    await ctx.send("Hello! Here are the descriptions of each discord command:\n\n"
                   "**channel** - Set the channel that HoliBot will send messages to.\n"
                   "**time <hour>** - Set the hour for when HoliBot will check and send notifications out.\n"
                   "   TIP: <hour> must be in 24 Hour Time format, e.g., hb:time 15\n"
                   "**add <code>** - Include national holidays based on the provided country code."
                   "   E.g., hb:add US\n"
                   "**info** - A brief description of the HoliBot.\n")


@tasks.loop(hours=1.0)
async def send_message():
    def filterHolidays(selected):
        if dateTime.date() == selected["date"]:
            return True

    def showHolidayMessage(selected):
        countryName = pycountry_convert.country_alpha2_to_country_name(selected["countryCode"])
        source = ""

        for link in search(holiday["name"], tld="co.in", num=10, stop=10, pause=2):
            if link is not None:
                source = link
                break

        if selected["global"]:
            return "Today is {}! If you would like to know more about this holiday, follow the link below!\n{}".format(
                selected["name"], source)
        else:
            if countryName[-1] == 's' or countryName[-1] == 'c':
                return "Today is {}! This is also known as \"{}\" in the {}. If you would like to learn more about " \
                       "this holiday, follow the link below!\n{}".format(selected["name"], selected["localName"]
                                                                         , countryName, source)
            else:
                return "Today is {}! This is also known as \"{}\" in {}. If you would like to learn more about " \
                       "this holiday, follow the link below!\n{}".format(selected["name"], selected["localName"]
                                                                         , countryName, source)

    currentHolidays = []

    if currentHour == clientData.hour:
        if clientData.channel is not None and len(clientData.countries.keys()) > 0:
            for country in clientData.countries.keys():
                countryHolidays = clientData.countries[country]
                currentHolidays.append(list(filter(filterHolidays, countryHolidays)))

            currentHolidays = np.ravel(currentHolidays)

            for holiday in currentHolidays:
                await clientData.channel.send(showHolidayMessage(holiday))


client.run(HOLIBOT)
