import requests
import telepot
from telepot.loop import MessageLoop
from pprint import pprint
import time
import yaml

from bearer_auth import BearerAuth

global bot
global TOKEN
global productAvail
currentAvail = False

stream = open("config.yaml", 'r')
config = yaml.load(stream, Loader=yaml.FullLoader)

TOKEN = config["BOT_TOKEN"]
bot = telepot.Bot(TOKEN)


def handle(msg):
    pprint(msg)


MessageLoop(bot, handle).run_as_thread()
print('Listening ...')


def checkF1Availability(status="A", msg="Product is available!"):
    url = 'https://api.singaporegp.sg/api/v2/tickets/details/2/401?lang=en'
    r = requests.get(url, auth=BearerAuth(config["auth_token"]))

    if str(r.status_code)[0] == "4" or str(r.status_code)[0] == "5":
        print(f"Error: {r.status_code}")
    else:
        if r.json()["ticket"]["ticketStatus"] == status:
            bot.sendMessage(config["OWNER_CHAT_ID"], msg)
            return True
    return False


# check once to notify user that bot is running
checkF1Availability("S", "Product is still unavailable!")
# Keep the program running.
while True:
    # current state false
    if currentAvail == False:
        # calling check function to see if status change to "A" then show message
        currentAvail = checkF1Availability("A", "Product is available!")

    time.sleep(1)
