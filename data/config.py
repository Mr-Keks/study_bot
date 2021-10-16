import string
from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
IP = env.str("ip")
DB_USER = env.str("DB_USER")
DB_PASSWORD = env.str("DB_PASSWORD")
DATABASE = env.str("DATABASE")

key_values = string.ascii_letters + string.digits

POSTGRES_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{IP}/{DATABASE}"
