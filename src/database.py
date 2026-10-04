import os
from sqlalchemy import create_engine
from urllib.parse import quote_plus


def get_database_connection():

    username = "root"
    password = os.getenv("SMARTNUTRI_DB_PASSWORD")    
    host = "localhost"
    port = 3306
    database = "smartnutri"

    if not password:
        raise ValueError(
            "SMARTNUTRI_DB_PASSWORD environment variable is not set."
        )

    encoded_password = quote_plus(password)

    connection_string = (
        f"mysql+pymysql://{username}:{encoded_password}"
        f"@{host}:{port}/{database}"
    )

    engine = create_engine(connection_string)

    return engine