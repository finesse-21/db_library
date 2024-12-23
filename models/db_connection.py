from configparser import ConfigParser
import psycopg2

def connect_to_db():
    try:
        parser = ConfigParser()
        parser.read("models/config.ini")

        if "DATABASE" not in parser:
            raise KeyError("DATABASE section is missing in config.ini")

        db_config = {
            "host": parser.get("DATABASE", "HOST", fallback=None),
            "port": parser.get("DATABASE", "PORT", fallback=None),
            "user": parser.get("DATABASE", "USER", fallback=None),
            "password": parser.get("DATABASE", "PASSWORD", fallback=None),
            "dbname": parser.get("DATABASE", "DB_NAME", fallback=None),
        }

        if not all(db_config.values()):
            raise ValueError("Some database configuration values are missing")

        return psycopg2.connect(**db_config)
    except KeyError as e:
        print(f"Configuration error: {e}")
        raise
    except ValueError as e:
        print(f"Configuration error: {e}")
        raise
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
        raise