import string
from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

#BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
BOT_TOKEN = "1886026763:AAEE-0KEz33QsG2Mpx-eHrubKn8vYE7v7Mg"
IP = env.str("ip")
DB_USER = env.str("DB_USER")
DB_PASSWORD = env.str("DB_PASSWORD")
DATABASE = env.str("DATABASE")

key_values = string.ascii_letters + string.digits

POSTGRES_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{IP}/{DATABASE}"
