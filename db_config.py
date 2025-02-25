import os
import dotenv


class DBConfig:
    def __init__(self):
        dotenv.load_dotenv()


        # path_to_env = os.path.join(os.getcwd(), '.env')
        # dotenv.load_dotenv(dotenv_path=path_to_env)
    def get_dbconfig(self):
        dbconfig = {
            'host': os.getenv("HOST"),
            'user': os.getenv("USER"),
            'password': os.getenv("PASSWORD"),
            'database': os.getenv("DATABASE"),
            'charset': os.getenv("CHARSET"),
        }
        return dbconfig
