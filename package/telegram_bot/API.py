import os
from dotenv import get_key

dotenv_path = os.getcwd() + "\\.env"
TOKEN_API = get_key(dotenv_path , "TOKEN_API" )


if __name__ == "__main__" :
    pass