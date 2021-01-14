import tgAuth
from extensions import Bot


tgbot = Bot(tgAuth.TOKEN)
tgbot.poll()


