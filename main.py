import os
import threading
from dotenv import load_dotenv

from PicturesProvider import PicturesProvider
from StoicApp import StoicApp
from TlgBot import TlgBot
from SQLRepo import SQLRepo
from TimersKeeper import TimersKeeper

load_dotenv()
users = SQLRepo(os.environ["db_path"], "users")

picture_name_template = os.environ["pictures_path"] + "/" + os.environ["picture_name_template"]
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
