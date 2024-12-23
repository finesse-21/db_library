from psycopg2 import sql
from models.db_connection import connect_to_db

def fetch_clients():
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, first_name, last_name, father_name, passport_seria, passport_number FROM clients")
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()

def add_client(first_name, last_name, father_name, passport_seria, passport_number):
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO clients (first_name, last_name, father_name, passport_seria, passport_number)
            VALUES (%s, %s, %s, %s, %s)
        """, (first_name, last_name, father_name, passport_seria, passport_number))
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()

def update_client(client_id, first_name, last_name, father_name, passport_seria, passport_number):
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE clients
            SET first_name = %s, last_name = %s, father_name = %s, passport_seria = %s, passport_number = %s
            WHERE id = %s
        """, (first_name, last_name, father_name, passport_seria, passport_number, client_id))
        conn.commit()
    finally:
        cur.close()
        conn.close()

# models/library_operations.py
def delete_client(client_id):
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        # Delete related journal entries first
        cur.execute("DELETE FROM journal WHERE client_id = %s", (client_id,))
        # Then delete the client
        cur.execute("DELETE FROM clients WHERE id = %s", (client_id,))
        conn.commit()
    finally:
        cur.close()
        conn.close()

def fetch_books():
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, name, cnt, type_id FROM books")
        books = cur.fetchall()
        return books
    except psycopg2.Error as e:
        raise e
    finally:
        cur.close()
        conn.close()

def add_book(name, count, type_id):
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO books (name, cnt, type_id)
            VALUES (%s, %s, %s)
        """, (name, count, type_id))
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()

def update_book(book_id, name, count, type_id):
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE books
            SET name = %s, cnt = %s, type_id = %s
            WHERE id = %s
        """, (name, count, type_id, book_id))
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()

def delete_book(book_id):
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM books WHERE id = %s", (book_id,))
        conn.commit()
    finally:
        cur.close()
        conn.close()

# models/library_operations.py
def fetch_book_types():
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, type, fine, day_count FROM book_types")
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()

def add_book_type(type_name, fine, day_count):
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO book_types (type, fine, day_count)
            VALUES (%s, %s, %s)
        """, (type_name, fine, day_count))
        conn.commit()
    finally:
        cur.close()
        conn.close()

def update_book_type(type_id, type, fine, day_count):
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE book_types SET type = %s, fine = %s, day_count = %s  WHERE id = %s", (type, fine, day_count, type_id))
        conn.commit()
    finally:
        cur.close()
        conn.close()

def delete_book_type(type_id):
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM book_types WHERE id = %s", (type_id,))
        conn.commit()
    finally:
        cur.close()
        conn.close()

# models/library_operations.py
def fetch_journal_entries():
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, client_id, book_id, date_beg, date_end, date_ret FROM journal")
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()



def add_journal_entry(client_id, book_id, date_beg, date_end, date_ret):
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute(
            sql.SQL("INSERT INTO journal (client_id, book_id, date_beg, date_end, date_ret) VALUES (%s, %s, %s, %s, %s)"),
            [client_id, book_id, date_beg, date_end, date_ret]
        )
        cur.execute(
            sql.SQL("UPDATE books SET cnt = cnt - 1 WHERE id = %s"),
            [book_id]
        )
        conn.commit()
    except Exception as e:
        if "Client already has 10 or more books issued" in str(e):
            raise Exception("Client already has 10 or more books issued")
        else:
            raise Exception(f"Ошибка добавления записи журнала: {e}")
    finally:
        cur.close()
        conn.close()


def delete_journal_entry(entry_id):
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute("SELECT 1 FROM journal WHERE id = %s", (entry_id,))
        if cur.fetchone() is None:
            return "Запись с указанным ID не найдена"

        cur.execute("DELETE FROM journal WHERE id = %s", (entry_id,))
        conn.commit()
    except psycopg2.Error as e:
        if "Cannot delete journal entry if the book is not returned" in str(e):
            return "Невозможно удалить запись журнала, если книга не возвращена"
        else:
            return f"Ошибка удаления записи журнала: {e}"
    finally:
        cur.close()
        conn.close()
    return None

import psycopg2
from PyQt6.QtWidgets import QMessageBox

def update_journal_return(entry_id, date_ret):
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute("SELECT 1 FROM journal WHERE id = %s", (entry_id,))
        if cur.fetchone() is None:
            QMessageBox.critical(None, "Ошибка", "Запись с указанным ID не найдена")
            return

        cur.execute("UPDATE journal SET date_ret = %s WHERE id = %s", (date_ret, entry_id))
        conn.commit()
    except psycopg2.Error as e:
        if "Return date cannot be earlier than issue date" in str(e):
            QMessageBox.critical(None, "Ошибка", "Дата возврата не может быть раньше даты выдачи")
        else:
            print(f"Error updating journal entry: {e}")
    finally:
        cur.close()
        conn.close()

def update_journal_entry(entry_id, client_id, book_id, date_beg, date_end, date_ret):
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute("SELECT 1 FROM journal WHERE id = %s", (entry_id,))
        if cur.fetchone() is None:
            QMessageBox.critical(None, "Ошибка", "Запись с указанным ID не найдена")
            return

        cur.execute("""
            UPDATE journal
            SET client_id = %s, book_id = %s, date_beg = %s, date_end = %s, date_ret = %s
            WHERE id = %s
        """, (client_id, book_id, date_beg, date_end, date_ret, entry_id))
        conn.commit()
    except psycopg2.Error as e:
        if "Return date cannot be earlier than issue date" in str(e):
            QMessageBox.critical(None, "Ошибка", "Дата возврата не может быть раньше даты выдачи")
        else:
            print(f"Error updating journal entry: {e}")
    finally:
        cur.close()
        conn.close()

def fetch_user(nickname, role):
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute("SELECT username FROM users WHERE nickname = %s AND role = %s", (nickname, role))
        user = cur.fetchone()
        return user if user else None
    finally:
        cur.close()
        conn.close()

def get_book_type_and_count(book_id):
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute(
            sql.SQL("SELECT type_id, cnt FROM books WHERE id = %s"),
            [book_id]
        )
        result = cur.fetchone()
        if result:
            return result[0], result[1]
        else:
            return None, None
    except Exception as e:
        print(f"Error fetching book type and count: {e}")
        return None, None
    finally:
        cur.close()
        conn.close()

def get_client_ids():
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id FROM clients")
        return [row[0] for row in cur.fetchall()]
    except Exception as e:
        print(f"Error fetching client IDs: {e}")
        return []
    finally:
        cur.close()
        conn.close()

def get_book_ids():
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id FROM books")
        return [row[0] for row in cur.fetchall()]
    except Exception as e:
        print(f"Error fetching book IDs: {e}")
        return []
    finally:
        cur.close()
        conn.close()

def get_journal_entry_ids():
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id FROM journal where date_ret is NULL")
        return [row[0] for row in cur.fetchall()]
    finally:
        cur.close()
        conn.close()

def get_book_type_ids():
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id FROM book_types")
        return [row[0] for row in cur.fetchall()]
    finally:
        cur.close()
        conn.close()

def get_books_on_loan(client_id):
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute("CALL GetBooksOnLoan(%s, %s)", (client_id, 0))
        result = cur.fetchone()
        return result[0] if result else 0
    finally:
        cur.close()
        conn.close()


def get_largest_fine():
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute("CALL GetLargestFine(%s, %s)", (0, 0))
        result = cur.fetchone()
        return result if result else (None, 0)
    finally:
        cur.close()
        conn.close()

def get_client_fine(client_id):
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute("CALL GetClientFine(%s, %s)", (client_id, 0))
        result = cur.fetchone()
        return result[0] if result else 0
    finally:
        cur.close()
        conn.close()


def get_book_name_by_id(book_id):
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute("SELECT name FROM books WHERE id = %s", (book_id,))
        result = cur.fetchone()
        return result[0] if result else None
    finally:
        cur.close()
        conn.close()

def get_top_3_books_all_time():
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        # Define the parameters to pass to the procedure
        top1_id = top1_count = top2_id = top2_count = top3_id = top3_count = None
        cur.execute("CALL top_3_books(%s, %s, %s, %s, %s, %s)",
                    (top1_id, top1_count, top2_id, top2_count, top3_id, top3_count))
        result = cur.fetchone()
        if result:
            top1_id, top1_count, top2_id, top2_count, top3_id, top3_count = result
            top1_name = get_book_name_by_id(top1_id)
            top2_name = get_book_name_by_id(top2_id)
            top3_name = get_book_name_by_id(top3_id)
            return (top1_name, top1_count, top2_name, top2_count, top3_name, top3_count)
        return None
    finally:
        cur.close()
        conn.close()