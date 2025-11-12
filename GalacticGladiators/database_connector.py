import mysql.connector
import logging
from config import config


def connect_to_database():
    try:
        cnx = mysql.connector.connect(**config)
        return cnx
    except mysql.connector.Error as err:
        logging.error(f"Database connection error: {err}")
        return None
