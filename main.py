import os
import threading
from dotenv import load_dotenv

from PicturesProvider import PicturesProvider
from StoicApp import StoicApp
from TlgBot import TlgBot
from Repo import Repo
from JsonListKeeper import JsonListKeeper
from TimersKeeper import TimersKeeper

load_dotenv()
users = Repo(JsonListKeeper("users.json"))

picture_name_template = "days/stoicism_{}_{}.png"
run_dir = os.path.dirname(__file__)
picture_provider = PicturesProvider(picture_name_template, run_dir)


update_time = int(os.environ["update_time"])
timer_keeper = TimersKeeper(update_time)

app = StoicApp(timer_keeper, users, picture_provider)

token = os.environ["TLG_BOT_TOKEN"]
bot = TlgBot(token, app)

app.add_observer(bot)


if __name__ == '__main__':
    threading.Thread(target=bot.run_bot).start()
    threading.Thread(target=timer_keeper.run_timer()).start()
