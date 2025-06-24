import configparser
import os

# Resolve path to secrets.ini
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "secrets.ini")

config = configparser.ConfigParser()
config.read(CONFIG_PATH)
