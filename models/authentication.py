from psycopg2 import sql, errors
from werkzeug.security import generate_password_hash, check_password_hash
from models.db_connection import connect_to_db

def register_user(username, password):
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    role = "admin"
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute(
            sql.SQL("INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)"),
            [username, hashed_password, role]
        )
        conn.commit()
        return True, "Регистрация прошла успешно"
    except errors.UniqueViolation:
        return False, "Пользователь с таким логином уже существует"
    except Exception as e:
        return False, str(e)
    finally:
        cur.close()
        conn.close()

def authenticate_user(username, password):
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute(
            sql.SQL("SELECT password_hash, role FROM users WHERE username = %s"),
            [username]
        )
        result = cur.fetchone()
        if result and check_password_hash(result[0], password):
            return result[1], "Авторизация прошла успешно"
        else:
            return None, "Неверный логин или пароль"
    except Exception as e:
        return None, str(e)
    finally:
        cur.close()
        conn.close()