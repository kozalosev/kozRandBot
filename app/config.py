from os import getenv as env

TOKEN = env("TOKEN")

MIN_PASSWORD_LENGTH = int(env("MIN_PASSWORD_LENGTH", "8"))
MAX_PASSWORD_LENGTH = int(env("MAX_PASSWORD_LENGTH", "2048"))
DEFAULT_PASSWORD_LENGTH = int(env("DEFAULT_PASSWORD_LENGTH", "12"))
PASSWORD_EXTRA_CHARS = env("PASSWORD_EXTRA_CHARS", "")
MAX_PASSWORD_GENERATION_TRIES = int(env("MAX_PASSWORD_GENERATION_TRIES", "100"))

PREMIUM_USERS_UID = [int(x) for x in env("PREMIUM_USERS_UID", "").split(",") if x.strip()]

NAME = env("NAME", "kozRandBot")
APP_HOST = env("APP_HOST", "0.0.0.0")
APP_PORT = int(env("APP_PORT", "8080"))
HOST = env("HOST")
SERVER_PORT = int(env("SERVER_PORT", "8443"))
METRICS_PORT = int(env("METRICS_PORT", "8000"))
UNIX_SOCKET = env("UNIX_SOCKET", f"/tmp/{NAME}.sock")
SOCKET_TYPE = env("SOCKET_TYPE", "TCP")

PROXY = env("PROXY")

DEBUG = env("DEBUG", "true").lower() in ("1", "true", "yes")
