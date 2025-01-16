import os
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), "token.env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

ID_WHATSAPP = os.getenv("ID_WHATSAPP")
TOKEN_WHATSAPP = os.getenv("TOKEN_WHATSAPP")

