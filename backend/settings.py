import os

from envparse import Env

env = Env()

ES_DATABASE_URL: str = env.str(
    "ES_DATABASE_URL",
    default=f"http://{os.environ.get('ES_DATABASE')}:{os.environ.get('ES_PORT')}",
)

SCROLL_TIME: str = env.str(
    "SCROLL_TIME",
    default="1h",
)
