from os import getenv as env

TOKEN = env("TOKEN")
HOST = env("HOST")  # required when DEBUG=false (webhook mode)

# Must be consistent with the path part of the location in your front-end web server configuration.
NAME = env("NAME", "kozRandBot")

APP_HOST = env("APP_HOST", "0.0.0.0")
APP_PORT = int(env("APP_PORT", "8080"))
SERVER_PORT = int(env("SERVER_PORT", "443"))
UNIX_SOCKET = env("UNIX_SOCKET", f"/tmp/{NAME}.sock")
SOCKET_TYPE = env("SOCKET_TYPE", "TCP")

# Use a proxy server to reach Telegram servers if you live in an authoritarian country
PROXY = env("PROXY")

# Set to 'False' for production use.
# Besides the level of verbosity, determines whether polling or webhooks will be used.
DEBUG = env("DEBUG", "true").lower() in ("1", "true", "yes")


# Application specific

MIN_PASSWORD_LENGTH = int(env("MIN_PASSWORD_LENGTH", "8"))
MAX_PASSWORD_LENGTH = int(env("MAX_PASSWORD_LENGTH", "2048"))
DEFAULT_PASSWORD_LENGTH = int(env("DEFAULT_PASSWORD_LENGTH", "12"))
PASSWORD_EXTRA_CHARS = env("PASSWORD_EXTRA_CHARS", "")
MAX_PASSWORD_GENERATION_TRIES = int(env("MAX_PASSWORD_GENERATION_TRIES", "100"))

PREMIUM_USERS_UID = [int(x) for x in env("PREMIUM_USERS_UID", "").split(",") if x.strip()]
